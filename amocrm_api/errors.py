_SECRET_KEYS = {
    "access_token",
    "refresh_token",
    "client_secret",
    "api_key",
    "password",
    "secret",
    "authorization",
}


def _mask(value):
    if isinstance(value, dict):
        return {
            k: ("***" if str(k).lower() in _SECRET_KEYS else _mask(v))
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_mask(item) for item in value]
    return value


class AmoException(Exception):
    def __init__(self, error_data: dict, code: int = 500, *args):
        self.error_data = error_data
        self.code = code
        super().__init__(args)

    def __str__(self):
        error_message = ''.join(
            f'{k}: {v}' for k, v in _mask(self.error_data).items()
        )
        return f'Code: {self.code}, Detail: {error_message}'
