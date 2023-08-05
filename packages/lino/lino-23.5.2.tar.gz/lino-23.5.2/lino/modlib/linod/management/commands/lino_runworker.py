# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import asyncio
import sys
import threading
from channels.layers import get_channel_layer
from django.core.management import BaseCommand, call_command
# from channels.management.commands.runworker import Command as BaseCommand
from django.conf import settings
from lino.modlib.linod.utils import LINOD


class Command(BaseCommand):
    def handle(self, *args, **options):

        def start_worker():
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            # super(Command, self).handle(*args, **options)
            call_command('runworker', LINOD)

        log_sock_file = settings.SITE.site_dir / 'log_sock'

        if log_sock_file.exists():
            raise Exception(
                f"log socket already exists: {log_sock_file}\n"
                "It's probable that a worker process is already running. "
                "Try: 'ps awx | grep lino_runworker' OR 'sudo supervisorctl status | grep worker'\n"
                "Or the last instance of the worker process did not finish properly. "
                "In that case remove the 'log_sock' file and run this command again.")


        worker_thread = threading.Thread(target=start_worker)
        worker_thread.start()

        async def initiate_linod():
            layer = get_channel_layer()
            await layer.send(LINOD, {'type': 'log.server'})
            await asyncio.sleep(1)
            await layer.send(LINOD, {'type': 'run.system.tasks'})

        loop = asyncio.get_event_loop()
        loop.run_until_complete(initiate_linod())

        try:
            worker_thread.join()
        except KeyboardInterrupt:
            worker_thread.join(0)
