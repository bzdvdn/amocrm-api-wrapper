class AmoException(Exception):
    def __init__(self, error_data: dict, code: int, *args):
        self.error_data = error_data
        self.code = code
        super().__init__(args)

    def __str__(self):
        error_message = ''.join(f'{k}: {v}' for k, v in self.error_data.items())
        return f'Code: {self.code}, Detail: {error_message}'
