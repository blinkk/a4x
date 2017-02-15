from . import messages
from google.appengine.api import mail
from google.appengine.ext import ndb
import appengine_config
import jinja2
import os
import webapp2


import jinja2

@jinja2.evalcontextfilter
def nl2br(eval_ctx, value):
    result = jinja2.escape(value).unescape().replace('\n', '<br>')
    if eval_ctx.autoescape:
        result = jinja2.Markup(result)
    return result


class Emailer(object):

    def __init__(self, sender_name):
        self.sender = '{} via Art for X <{}>'.format(sender_name, appengine_config.EMAIL_SENDER)

    def send(self, to, subject, template, kwargs):
        html = self._render(template, kwargs)
        self._send(subject, to, html)

    def _render(self, template, kwargs):
        jinja_template = self.env.get_template(template)
        return jinja_template.render(kwargs)

    def _send(self, subject, to, html):
        message = mail.EmailMessage(sender=self.sender, subject=subject)
        message.to = to
        message.html = html
        message.send()

    @webapp2.cached_property
    def env(self):
        here = os.path.dirname(__file__)
        path = os.path.join(os.path.dirname(__file__), 'templates')
        loader = jinja2.FileSystemLoader([path])
        env = jinja2.Environment(
            loader=loader,
            autoescape=True,
            trim_blocks=True)
        env.filters['nl2br'] = nl2br
        return env
