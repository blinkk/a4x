import airlock
import logging
import os
import jinja2
from google.appengine.ext.webapp import mail_handlers

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'build'))
_loader = jinja2.FileSystemLoader(_path)
_env = jinja2.Environment(loader=_loader, autoescape=True, trim_blocks=True)


class EmailHandler(mail_handlers.InboundMailHandler):

    def receive(self, message):
        logging.info(message)


class FrontendHandler(airlock.Handler):

    def get(self):
        if not self.me.registered:
            url = self.urls.sign_in()
            self.redirect(url)
            return
        template_name = 'index.html'
        template = _env.get_template(template_name)
        params = {}
        params.update({
            'me': self.me,
            'version': os.getenv('CURRENT_VERSION_ID', 'xxx'),
        })
        self.response.write(template.render(params))
