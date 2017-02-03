import appengine_config as config
#from . import handlers
from . import services
from protorpc.wsgi import service
import appengine_config
import webapp2

#airlock.set_config(appengine_config.AIRLOCK_CONFIG)


app = webapp2.WSGIApplication([
#    ('.*', handlers.FrontendHandler),
])


api_app = service.service_mappings((
    ('/_api/orders.*', services.OrderService),
))


#email_app = webapp2.WSGIApplication([
#    handlers.EmailHandler.mapping(),
#])


def seed_test_data(skip=False):
    pass


#if appengine_config.IS_DEV:
#    seed_test_data()
