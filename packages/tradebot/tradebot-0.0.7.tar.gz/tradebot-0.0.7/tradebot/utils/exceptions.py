
class BadResponseException(Exception):
    def __init__(self, msg:str, res) -> None:
        msg = f"Bad response: {res.status_code}. {msg}"
        super().__init__(msg)