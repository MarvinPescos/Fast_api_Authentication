from app.errors import BalanceHubException

class SystemError(BalanceHubException):
    """Base system exception"""
    pass

class ConfigurationError(SystemError):
    """System configuration error"""
    pass

class FileSystemError(SystemError):
    """File system operation error"""
    pass

class CacheError(SystemError):
    """Cache operation error"""
    pass

class QueueError(SystemError):
    """Message queue error"""
    pass

class RateLimitError(SystemError):
    """Rate limit exceeded"""
    pass

class MaintenanceModeError(SystemError):
    """System is in maintenance mode"""
    pass

class ServiceUnavailableError(SystemError):
    """Service temporarily unavailable"""
    pass
