"""
This file contains settings that are specific to CryptoToken Converter, and do not affect the core Django
framework.

User specifiable environment variables:

- ``STEEM_RPC_NODES`` - Comma-separated list of one/more Steem RPC nodes. If not set, will use the default beem nodes.

- ``BITSHARES_RPC_NODE`` - Node to use to connect to Bitshares network if Bitshares coin handler is enabled. If not
  set, will default to wss://eu.nodes.bitshares.ws

- ``EX_FEE`` - Conversion fee taken by us, in percentage (i.e. "1" = 1%) **Default:** 0 (no fee)

- ``COIN_HANDLERS`` - A comma separated list of Coin Handler modules to load. **Default:** SteemEngine,Bitcoin

- ``COIN_HANDLERS_BASE`` - If your coin handlers are not located in ``payments.coin_handlers`` then you may change this
  to point to the base module where your coin handlers are located.

- ``LOWFUNDS_NOTIFY`` - If you're using the low wallet balance notifications, you can change how often it re-notifies
  the admin emails ``ADMINS`` if the balance is still too low to fulfill a conversion. (in hours).
  **Default:** ``12``   (hours)

Copyright::

    +===================================================+
    |                 © 2019 Privex Inc.                |
    |               https://www.privex.io               |
    +===================================================+
    |                                                   |
    |        CryptoToken Converter                      |
    |                                                   |
    |        Core Developer(s):                         |
    |                                                   |
    |          (+)  Chris (@someguy123) [Privex]        |
    |                                                   |
    +===================================================+
"""
from decimal import Decimal
from beem.steem import Steem
from beem.instance import set_shared_steem_instance
from getenv import env

#########
# Steem Network related settings
####

STEEM_RPC_NODES = env('STEEM_RPC_NODES', None)
# Supply a list of one or more comma-separated Steem RPC nodes. If not set, will use the default beem nodes.
STEEM_RPC_NODES = STEEM_RPC_NODES.split(',') if STEEM_RPC_NODES is not None else None
# Set the shared Beem RPC instance to use the specified nodes
steem_ins = Steem(node=STEEM_RPC_NODES, num_retries=5, num_retries_call=3, timeout=20)
steem_ins.set_password_storage('environment')  # Get Beem wallet pass from env var ``UNLOCK``
set_shared_steem_instance(steem_ins)

#########
# Bitshares Network related settings
####

BITSHARES_RPC_NODE = env('BITSHARES_RPC_NODE', 'wss://eu.nodes.bitshares.ws')

#########
# General CryptoToken Converter settings
####

# Used for encrypting and decrypting private keys so they cannot be displayed in plain text by the admin panel,
# or external applications accessing the DB.
# Generate an encryption key using ./manage.py generate_key.
# To print just the key, use ``./manage.py generate_key 2> /dev/null``
ENCRYPT_KEY = env('ENCRYPT_KEY')

EX_FEE = Decimal(env('EX_FEE', '0'))  # Conversion fee taken by us, in percentage (i.e. "1" = 1%)


# This is used for the dropdown "Coin Type" selection in the Django admin panel. Coin handlers may add to this list.
COIN_TYPES = (
    ('crypto', 'Generic Cryptocurrency',),
    ('token', 'Generic Token'),
)

# Load coin handlers from this absolute module path
COIN_HANDLERS_BASE = env('COIN_HANDLERS_BASE', 'payments.coin_handlers')
# A comma separated list of modules to load
COIN_HANDLERS = env('COIN_HANDLERS', 'SteemEngine,Bitcoin,Steem,EOS,Bitshares').split(',')

# After the first email to inform admins a wallet is low, how long before we send out a second notification?
# (in hours) (Default: 12 hrs)
LOWFUNDS_RENOTIFY = int(env('LOWFUNDS_RENOTIFY', 12))

#########
# Defaults for pre-installed Coin Handlers, to avoid potential exceptions when accessing their settings.
####

COIND_RPC = {}  # Used by coin_handlers.Bitcoin if you don't want to store connection details in DB.
