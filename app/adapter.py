import uuid
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        user.username = str(uuid.uuid4())

    def generate_unique_username(self, txts, regex=None):
        return str(uuid.uuid4()) 