class InferenceFailedException(Exception):

    def __init__(self, reason: str = 'Text inference has failed.', *, status_code: int = None):
        if status_code and status_code == 500:
            self.message = f'Empty prompt or wrong conversation id was given.'
        else:
            self.message = f'{reason}. {f"Status code: {status_code}" if status_code else ""}.'
        super().__init__(self.message)
