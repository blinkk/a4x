import appengine_config

from . import services
from protorpc.wsgi import service



api_app = service.service_mappings((
    ('/_api/campaigns.*', services.CampaignService),
    ('/_api/orders.*', services.OrderService),
))
