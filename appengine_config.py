import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'lib'))

import stripe

# TODO: Rotate this key.
stripe.api_key = 'sk_test_0ElQNoeAKMENHTBhV6qcikzw'
