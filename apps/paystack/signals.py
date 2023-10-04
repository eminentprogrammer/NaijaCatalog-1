from django.dispatch import Signal

payment_verified = Signal(["ref","amount", "order"])

event_signal = Signal(['event', "data"])