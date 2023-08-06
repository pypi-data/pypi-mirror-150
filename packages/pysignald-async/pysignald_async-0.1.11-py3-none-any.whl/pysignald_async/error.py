class SignaldException(Exception):
    """
    Base class to translate signald's response payloads into python exceptions
    """

    def __init__(self, type_, payload):
        self.type = type_
        self.payload = payload

    def __str__(self):
        return f"{self.type}: {self.payload}"


def raise_error(response: dict):
    """
    Raise a python exception using a signald response payload
    """
    if "error_type" in response:
        raise SignaldException(response["error_type"], response["error"])
