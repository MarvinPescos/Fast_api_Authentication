from app.errors import BalanceHubException

class ValidationError(BalanceHubException):
    """Base validation exception"""
    pass

class InvalidEmailError(ValidationError):
    """Email format is invalid"""
    pass

class InvalidPhoneError(ValidationError):
    """Phone number format is invalid"""
    pass

class InvalidPasswordError(ValidationError):
    """Password does not meet requirements"""
    pass

class InvalidDateError(ValidationError):
    """Date format or value is invalid"""
    pass

class RequiredFieldError(ValidationError):
    """Required field is missing"""
    pass

class FieldTooLongError(ValidationError):
    """Field exceeds maximum length"""
    pass

class FieldTooShortError(ValidationError):
    """Field is below minimum length"""
    pass

class InvalidFormatError(ValidationError):
    """Data format is invalid"""
    pass

class InvalidRangeError(ValidationError):
    """Value is outside allowed range"""
    pass
