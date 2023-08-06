from .. import types, functions


class User:
    def __init__(self,
        id:int=None,
        is_self:bool=None,
        mutual_contact:bool=None,
        deleted:bool=None,
        bot:bool=None,
        bot_chat_history:bool=None,
        bot_nochats:bool=None,
        verified:bool=None,
        restricted:bool=None,
        min:bool=None,
        bot_inline_geo=None,
        support=None, fake=None, access_hash=None,
        first_name=None, last_name=None, username=None,
        phone=None, photo=None, status=None, bot_info_version=None, restriction_reason=[],
        bot_inline_placeholder=None, lang_code=None):
        self._client = None
        self.id = id
        self.is_self = is_self
        self.mutual_contact = mutual_contact
        self.deleted = deleted
        self.bot = bot
        self.bot_chat_nohistory = None
        self.bot_nochats = bot_nochats
        self.verified = verified
        self.restricted = restricted
        self.min = min
        self.bot_inline_geo = bot_inline_geo
        self.support = support
        self.fake = fake
        self.access_hash = access_hash
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.phone = phone
        if self.is_self:
            self.phone = "**********"
        self.photo = photo
        self.status = status
        self.bot_info_version = bot_info_version
        self.bot_inline_placeholder = bot_inline_placeholder
        self.lang_code = self.lang_code


    def _set_client(self, client):
        self._client = client

    async def block():
        pass