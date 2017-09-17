import keyring
from test.fake_keyring import FakeKeyring

keyring.set_keyring(FakeKeyring())
