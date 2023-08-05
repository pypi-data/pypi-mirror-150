class AccountError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AccountIsPrivate(AccountError):
    pass


class AccountIsNotExist(AccountError):
    pass
