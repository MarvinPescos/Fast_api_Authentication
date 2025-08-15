from app.errors import BalanceHubException

class DatabaseError(BalanceHubException):
    """Base database exception"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Database connection Failed"""
    pass

class DatabaseTimeoutError(DatabaseError):
    """Database operation timed out"""
    pass

class DatabaseTransactionError(DatabaseError):
    """Database transaction failed"""
    pass

class DuplicateKeyError(DatabaseError):
    """Duplicate key constraint violation"""
    pass

class ForeignKeyError(DatabaseError):
    """Foreign key constraint violation"""
    pass

class DatabaseIntegrityError(DatabaseError):
    """Database integrity constraint violation"""
    pass

class RecordNotFound(DatabaseError):
    """Database record not found"""
    pass

class DatabaseMigrationFailed(DatabaseError):
    """Database migration failed"""
    pass

    