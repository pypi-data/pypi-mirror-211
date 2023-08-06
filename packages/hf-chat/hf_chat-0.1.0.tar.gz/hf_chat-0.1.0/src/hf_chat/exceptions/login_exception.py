class LoginException(Exception):

    def __init__(self, reason: str = 'Failed to sign in into account.', *, status_code: int = None):
        self.message = f'{reason}. {f"Status code: {status_code}" if status_code else ""}.'
        super().__init__(self.message)
