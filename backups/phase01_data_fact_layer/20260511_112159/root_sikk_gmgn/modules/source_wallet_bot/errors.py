class SourceWalletBotError(Exception):
    """Base error for Source Wallet Bot."""


class MissingFieldError(SourceWalletBotError):
    """Raised when a required field is absent in strict validation mode."""


class SourceLevelError(SourceWalletBotError):
    """Raised when data source level violates contract boundaries."""


class ForbiddenFieldError(SourceWalletBotError):
    """Raised when handoff or decision payload contains forbidden trading fields."""


class SchemaValidationError(SourceWalletBotError):
    """Raised when schema validation fails."""
