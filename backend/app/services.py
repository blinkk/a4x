from . import messages



class Service(remote.Service):

    @remote.method(messages.DonationRequest
                   messages.DonationResponse)
    def donate(self, request):
        pass
