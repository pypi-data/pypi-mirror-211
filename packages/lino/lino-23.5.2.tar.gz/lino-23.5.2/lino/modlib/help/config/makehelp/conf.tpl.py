# -*- coding: utf-8 -*-
from pathlib import Path
import synodal

docs_path = Path('../docs').resolve()

templates_path = []  # will be populated by lino.sphinxcontrib.configure()

intersphinx_mapping = {}
for r in synodal.REPOS_LIST:
    if r.public_url and r.nickname:
        # if r.nickname == "welfare": continue
        intersphinx_mapping[r.nickname] = (r.public_url, None)

{% if makehelp.language.index == 0 -%}

html_context = dict(public_url="{{settings.SITE.server_url}}media/cache/help")

from rstgen.sphinxconf import configure ; configure(globals())
from lino.sphinxcontrib import configure ; configure(globals())

# print("20230314", intersphinx_mapping)

project = "{{settings.SITE.title}}"
html_title = "{{settings.SITE.title}}"

{% if settings.SITE.site_config.site_company %}
import datetime
copyright = "{} {{settings.SITE.site_config.site_company}}".format(
    datetime.date.today())
{% endif %}
htmlhelp_basename = 'help'
extensions += ['lino.sphinxcontrib.logo']

{% else -%}{# elif makehelp.language.index == 0 -#}

fn = docs_path / 'conf.py'
with open(fn, "rb") as fd:
    exec(compile(fd.read(), fn, 'exec'))

{%- endif %}

language = '{{makehelp.language.django_code}}'

pth = docs_path / ".templates"
assert pth.exists()
templates_path.insert(0, str(pth.resolve()))

# print("20230314 intersphinx_mapping is", intersphinx_mapping)
