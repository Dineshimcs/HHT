class AuraException(Exception):
    """Base exception for domain business logic errors."""
    def __init__(self, message, code="BAD_REQUEST", details=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}

class BookingStateError(AuraException):
    """Raised when an invalid state transition is attempted."""
    pass

class DriverNotAvailableError(AuraException):
    """Raised when no qualified drivers are found in dispatch."""
    pass

class InsufficientWalletBalanceError(AuraException):
    """Raised when payment via wallet fails due to low funds."""
    pass

class DocumentVerificationRequiredError(AuraException):
    """Raised when driver attempts to go online without valid KYC."""
    pass
