from protorpc import messages


class AmountMessage(messages.Message):
    cause = messages.IntegerField(1)
    artist = messages.IntegerField(2)


class SizeMessage(messages.Message):
    width = messages.IntegerField(1)
    height = messages.IntegerField(2)
    quantity = messages.IntegerField(3)


class FormatMessage(messages.Message):
    size = messages.MessageField(SizeMessage, 1)


class DonationMessage(messages.Message):
    amount = messages.MessageField(AmountMessage, 1)
    size = messages.MessageField(AmountMessage, 2)


class DonationRequest(messages.Message):
    donation = messages.MessageField(DonationMessage, 1)


class DonationResponse(messages.Message):
    donation = messages.MessageField(DonationMessage, 1)
