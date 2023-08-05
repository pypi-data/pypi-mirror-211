# -*- coding: UTF-8 -*-
# Copyright 2011-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import logging ; logger = logging.getLogger(__name__)
import json
from io import StringIO
from lxml import etree
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils import translation
from etgen.html import E, tostring

from lino.api import dd, rt, _

from lino.core import constants
# from lino.core.roles import SiteStaff
from lino.core.gfks import gfk2lookup
# from lino.core.requests import BaseRequest
from lino.core.site import html2text

from lino.mixins import Created, ObservedDateRange
from lino.modlib.gfks.mixins import Controllable
# from lino.modlib.notify.consumers import PUBLIC_GROUP
from lino.modlib.users.mixins import UserAuthored, My
from lino.modlib.office.roles import OfficeUser

from lino.utils.format_date import fds

from .mixins import PUBLIC_GROUP
from .choicelists import MessageTypes, MailModes
from .api import send_notification, NOTIFICATION

html_parser = etree.HTMLParser()

def groupname(s):
    # Remove any invalid characters from the given string so that it can
    # be used as a Redis group name.
    # "Group name must be a valid unicode string containing only
    # alphanumerics, hyphens, or periods."

    s = s.replace('@', '-')
    return s.encode('ascii', 'ignore')


class MarkAllSeen(dd.Action):
    select_rows = False
    http_method = 'POST'
    show_in_plain = True

    label = _("Mark all as seen")
    button_text = "✓"  # u"\u2713"

    def run_from_ui(self, ar, **kwargs):
        qs = rt.models.notify.Message.objects.filter(
            user=ar.get_user(), seen__isnull=True)
        for obj in qs:
            obj.seen = timezone.now()
            obj.save()
        ar.success(eval_js='window.top.document.querySelectorAll(".' + ar.actor.actor_id.replace(".","-") + '")[0].classList.add("dashboard-item-closed"); console.log("lel")')



class MarkSeen(dd.Action):
    label = _("Mark as seen")
    show_in_toolbar = False
    show_in_workflow = True
    button_text = "✓"  # u"\u2713"

    # button_text = u"\u2611"  # BALLOT BOX WITH CHECK

    def get_action_permission(self, ar, obj, state):
        if obj.seen:
            return False
        return super(MarkSeen, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            obj.seen = timezone.now()
            obj.save()
        ar.success(refresh_all=True)


class ClearSeen(dd.Action):
    label = _("Clear seen")
    show_in_toolbar = False
    show_in_workflow = True

    # button_text = u"\u2610"  # BALLOT BOX

    def get_action_permission(self, ar, obj, state):
        if not obj.seen:
            return False
        return super(ClearSeen, self).get_action_permission(ar, obj, state)

    def run_from_ui(self, ar):
        for obj in ar.selected_rows:
            obj.seen = None
            obj.save()
        ar.success(refresh_all=True)

if dd.plugins.notify.use_push_api and settings.SITE.use_linod:

    class Subscription(UserAuthored):
        allow_cascaded_delete = ['user']
        lang = models.CharField(max_length=30, null=True, blank=True)
        userAgent = models.CharField(max_length=200, null=True, blank=True)
        endpoint = models.URLField(max_length=500)
        p256dh = models.CharField(max_length=300)
        auth = models.CharField(max_length=150)


class Message(UserAuthored, Controllable, Created):

    show_in_site_search = False

    class Meta(object):
        app_label = 'notify'
        verbose_name = _("Notification message")
        verbose_name_plural = _("Notification messages")
        ordering = ['created', 'id']

    message_type = MessageTypes.field(default="change")
    seen = models.DateTimeField(_("seen"), null=True, editable=False)
    sent = models.DateTimeField(_("sent"), null=True, editable=False)
    body = dd.RichTextField(_("Body"), editable=False, format='html', default='')
    mail_mode = MailModes.field(default=MailModes.as_callable('often'))
    subject = models.CharField(
        _("Subject"), max_length=250, editable=False)

    def __str__(self):
        return "{} #{}".format(self.message_type, self.id)

        # return _("About {0}").format(self.owner)

    # return self.message
    # return _("Notify {0} about change on {1}").format(
    #     self.user, self.owner)

    @classmethod
    def emit_broadcast_notification(cls,
        msg, owner=None, message_type=None, push_options={},
        **msgdata):
        cls.create_message(
            None, owner, push_options=push_options,
            body=msg, subject="Broadcast message",
            message_type=message_type, **msgdata)

    @classmethod
    def emit_notification(
            cls, ar, owner, message_type, msg_func, recipients):
        """
        ATM the action_url is computed using the permissions of the sending user.
        That's maybe not exactly what we want (the url should depend on the recipient).
        But until now we cannot imagine any case where this would become important.
        """
        push_options = {}
        # remove recipients without user:
        if ar is None:
            me = None
        else:
            if owner is not None:
                ba = owner.get_detail_action(ar)
                if ba is not None:
                    push_options.update(action_url=ar.renderer.get_detail_url(ar, ba.actor, owner.pk))
                # push_options.update(action_url=ar.renderer.obj2url(ar, owner))
            me = ar.get_user()
        others = set()
        for user, mm in recipients:
            if user is not None and mm != MailModes.silent:
                if user.user_type is None:
                    continue
                if me is None or me.notify_myself or user != me:
                    others.add((user, mm))

        # dd.logger.info("20211121 Notify other users: %s", others)
        if len(others):
            # rr = message_type.required_roles
            # subject = "{} by {}".format(message_type, me)
            for user, mm in sorted(others, key=lambda x: x[0].username):
                # if not user.user_type.has_required_roles(rr):
                if message_type in user.user_type.mask_message_types:
                    continue
                if mm is None:
                    mm = MailModes.often
                with dd.translation.override(user.language):
                    subject_body = msg_func(user, mm)
                    if subject_body is not None:
                        subject, body = subject_body
                        cls.create_message(
                            user, owner, push_options=push_options,
                            body=body, subject=subject,
                            mail_mode=mm, message_type=message_type)

    @classmethod
    def create_message(cls, user, owner=None, push_options={}, **msgdata):
        # if owner is not None and user is not None:
        #     fltkw = gfk2lookup(cls.owner, owner)
        #     qs = cls.objects.filter(
        #         user=user, seen__isnull=True, **fltkw)
        #     if qs.exists():
        #         return
        obj = cls(user=user, owner=owner, **msgdata)
        obj.full_clean()
        obj.save()
        # Encode and send that message to the whole channels Group for our
        # Websocket. Note how you can send to a channel or Group from any part
        # of Django, not just inside a consumer.
        # logger.info("Sending browser notification to %s", user or "everyone")
        push_options.update(
            primary_key=obj.id,  # needed for websockets
            # subject=str(self.subject),
            subject=settings.SITE.title,
            # body=settings.SITE.plugins.memo.parser.parse(obj.body),
            body=html2text(obj.body),
            created=obj.created)
        send_notification(user, **push_options)


    mark_all_seen = MarkAllSeen()
    mark_seen = MarkSeen()
    clear_seen = ClearSeen()

    @classmethod
    def send_summary_emails(cls, mm):
        qs = cls.objects.filter(sent__isnull=True)
        qs = qs.exclude(user__email='')
        qs = qs.filter(mail_mode=mm).order_by('user')
        if qs.count() == 0:
            return
        # from lino.core.renderer import MailRenderer
        # ar = rt.login(renderer=MailRenderer())
        ar = rt.login(renderer=dd.plugins.memo.front_end.renderer, permalink_uris=True)
        # ar = rt.login()
        # ar = rt.login(renderer=settings.SITE.kernel.default_ui.renderer)
        context = ar.get_printable_context()
        sender = settings.SERVER_EMAIL
        template = rt.get_template('notify/summary.eml')
        users = dict()
        for obj in qs:
            if obj.user is not None:
                lst = users.setdefault(obj.user, [])
                lst.append(obj)
        dd.logger.debug(
            "Send out %s summaries for %d users.", mm, len(users))
        for user, messages in users.items():
            with translation.override(user.language):
                if len(messages) == 1:
                    subject = messages[0].subject
                else:
                    subject = _("{} notifications").format(len(messages))
                subject = settings.EMAIL_SUBJECT_PREFIX + subject
                context.update(user=user, messages=messages)
                body = template.render(**context)
                # dd.logger.debug("20170112 %s", body)
                rt.send_email(subject, sender, body, [user.email])
                for msg in messages:
                    msg.sent = timezone.now()
                    if dd.plugins.notify.mark_seen_when_sent:
                        msg.seen = timezone.now()
                    msg.save()

    # def send_browser_message_for_all_users(self, user):
    #     # not maintained. appearently not used.
    #     message = {
    #         "id": self.id,
    #         "subject": self.subject,
    #         "body": html2text(self.body),
    #         "created": self.created.strftime("%a %d %b %Y %H:%M"),
    #     }
    #
    #     # Encode and send that message to the whole channels Group for our
    #     # liveblog. Note how you can send to a channel or Group from any part
    #     # of Django, not just inside a consumer.
    #     from channels.layers import get_channel_layer
    #     channel_layer = get_channel_layer()
    #     from asgiref.sync import async_to_sync
    #     async_to_sync(channel_layer.group_send)(PUBLIC_GROUP, {"text": json.dumps(message)})


dd.update_field(Message, 'user',
                verbose_name=_("Recipient"), editable=False)
# Message.update_controller_field(
#     null=True, blank=True, verbose_name=_("About"))

dd.inject_field(
    'users.User', 'notify_myself',
    models.BooleanField(_('Notify myself'), default=False))

dd.inject_field(
    'users.User', 'mail_mode',
    MailModes.field(default=MailModes.as_callable('often')))


class Messages(dd.Table):
    model = 'notify.Message'
    column_names = "created subject user seen sent *"
    # cell_edit = False

    card_layout = """
    user seen
    subject
    workflow_buttons
    """


    # detail_layout = dd.DetailLayout("""
    # created user seen sent owner
    # overview
    # """, window_size=(50, 15))

    parameters = ObservedDateRange(
        # user=dd.ForeignKey(
        #     settings.SITE.user_model,
        #     blank=True, null=True),
        show_seen=dd.YesNo.field(_("Seen"), blank=True),
    )

    params_layout = "user show_seen start_date end_date"

    # @classmethod
    # def get_simple_parameters(cls):
    #     for p in super(Messages, cls).get_simple_parameters():
    #         yield p
    #     yield 'user'

    @classmethod
    def get_request_queryset(self, ar, **filter):
        qs = super(Messages, self).get_request_queryset(ar, **filter)
        pv = ar.param_values

        if pv.show_seen == dd.YesNo.yes:
            qs = qs.filter(seen__isnull=False)
        elif pv.show_seen == dd.YesNo.no:
            qs = qs.filter(seen__isnull=True)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Messages, self).get_title_tags(ar):
            yield t
        pv = ar.param_values
        if pv.show_seen:
            yield str(pv.show_seen)

    @classmethod
    def unused_get_detail_title(self, ar, obj):
        """This was used to set `seen` automatically when a detail was
        shown.

        """
        if obj.seen is None and obj.user == ar.get_user():
            obj.seen = timezone.now()
            obj.save()
            # dd.logger.info("20151115 Marked %s as seen", obj)
        return super(Messages, self).get_detail_title(ar, obj)


class AllMessages(Messages):
    required_roles = dd.login_required(dd.SiteAdmin)


class MyMessages(My, Messages):
    # label = _("My messages")
    required_roles = dd.login_required(OfficeUser)
    # column_names = "created subject owner sent workflow_buttons *"
    column_names = "created subject message_type workflow_buttons *"
    created_order = "-created"
    order_by = [created_order]
    # hide_headers = True
    display_mode = ((None, constants.DISPLAY_MODE_SUMMARY), )

    @classmethod
    def get_table_summary(cls, mi, ar):
        u = ar.get_user()
        if u.is_authenticated:
            qs = rt.models.notify.Message.objects.filter(
                user=u).order_by(cls.created_order)
            qs = qs.filter(seen__isnull=True)
        else:
            qs = rt.models.notify.Message.objects.filter(
                user__isnull=True).order_by(cls.created_order)
        # mark_all = rt.models.notify.MyMessages.get_action_by_name(
        #     'mark_all_seen')
        # html = tostring(ar.action_button(mark_all, None))
        # TODO: make action_button() work with list actions
        # html = ''
        ba = rt.models.notify.MyMessages.get_action_by_name('mark_seen')

        def fmt(obj):
            s = tostring(ar.action_button(ba, obj))
            s += fds(obj.created) + " " + obj.created.strftime(
                settings.SITE.time_format_strftime) + " "
            if obj.body:
                s += ar.parse_memo(obj.body)
            else:
                s += ar.parse_memo(obj.subject)
            e = etree.parse(StringIO(s), html_parser)
            return E.li(E.div(*e.iter()))
            # s += obj.body
            # return "<li>{}</li>".format(s)

        items = []
        for obj in qs:
            items.append(fmt(obj))
        return E.ul(*items)
        # return html + "<ul>{}</ul>".format(''.join(items))

    # filter = models.Q(seen__isnull=True)

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(MyMessages, self).param_defaults(ar, **kw)
        kw.update(show_seen=dd.YesNo.no)
        return kw


# h = settings.EMAIL_HOST
# if not h or h.endswith('example.com'):
#     dd.logger.debug(
#         "Won't send pending messages because EMAIL_HOST is %r",
#         h)

@dd.schedule_often(every=10)
def send_pending_emails_often(ar):
    rt.models.notify.Message.send_summary_emails(MailModes.often)


@dd.schedule_daily()
def send_pending_emails_daily(ar):
    rt.models.notify.Message.send_summary_emails(MailModes.daily)


# @dd.schedule_often(every=10)
# def send_pending_emails_often(ar):
#     Message = rt.models.notify.Message
#     qs = Message.objects.filter(sent__isnull=True)
#     qs = qs.filter(user__mail_mode=MailModes.immediately)
#     if qs.count() > 0:
#         dd.logger.debug(
#             "Send out emails for %d messages.", qs.count())
#         for obj in qs:
#             obj.send_individual_email()
#     else:
#         dd.logger.debug("No messages to send.")


remove_after = dd.plugins.notify.remove_after

if remove_after:

    @dd.schedule_daily()
    def clear_seen_messages(ar):

        Message = rt.models.notify.Message
        qs = Message.objects.filter(
            created__lt=timezone.now() - timedelta(days=remove_after))
        if dd.plugins.notify.keep_unseen:
            qs = qs.filter(seen__isnull=False)
        if qs.count() > 0:
            dd.logger.info(
                "Removing %d messages older than %d hours.",
                qs.count(), remove_after)
            qs.delete()

import warnings

warnings.filterwarnings(
    "ignore",
    "You do not have a working installation of the service_identity module: .* Many valid certificate/hostname mappings may be rejected.",
    UserWarning)
