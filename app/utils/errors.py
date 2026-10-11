class ApiError(Exception):
    """Error di sini sengaja kita lempar dari route/helper.
    Akan ditangkap oleh error handler dan diubah menjadi respons JSON."""

    def __init__(self, message: str, status: int = 400, errors: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.errors = errors
