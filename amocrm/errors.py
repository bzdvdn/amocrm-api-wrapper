class AmoException(Exception):
    def __init__(self, error_data: dict, *args):
        self.error_data = error_data
        super().__init__(args)

    def __str__(self):
        return ''.join(f'{k}: {v}' for k, v in self.error_data.items())
