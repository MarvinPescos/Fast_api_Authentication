# from fastapi import Request, HTTPException
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from datetime import datetime
# from typing import Dict, Any
# import logging
# import traceback

# from app.errors import (
#     BalanceHubException,
#     AuthenticationError,
#     DatabaseError,
#     ValidationError
# )

# logger = logging.getLogger(__name__)

# class ErrorResponse:
#     """
#     Standardized error response format
#     """

#     @staticmethod
#     def format_error(
#         error_type: str,
#         message: str,
#         details: Dict[str, Any] = None,
#         error_code: str = None
#     ) -> Dict[str, Any]:
#         """Format error response consistently across the API"""
#         return {
#             "error": {
#                 "type": error_type,
#                 "message": message,
#                 "code": error_code,
#                 "details": details or {},
#                 "timestamp": datetime.utcnow().isoformat()
#             }
#         }
    
# async def custom_exception_handler(request: Request,  exc:BalanceHubException) -> JSONResponse:
#     """Handle custom application exceptions"""

#     logger.error(
#         f"Custom exception: {exc.__class__.__name__}",
#         extra={
#             "error_code": exc.error_code,
#             "context": getattr(exc, 'context', {}) ,
#             "path": str(request.url),
#             "method": request.method
#         }
#     )

#     status_code_map = {
#         'AuthenticationError': 401,
#         'ValidationError': 400,
#         'DatabaseError': 500,
#         'BalanceHubException': 400,
#     }

#     status_code = status_code_map.get(exc.__class__.__name__, 500)

#     return JSONResponse(
#         status_code=status_code,
#         content=ErrorResponse.format_error(
#             error_type=exc.__class__.__name__,
#             message=str(exc),
#             error_code=exc.error_code,
#             details=getattr(exc, 'context', {})
#         )
#     )

# async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
#     """Handle Pydantic validation error"""
#     logger.warning(
#         "Validation error",
#         extra={
#             "errors": exc.errors()
#         }
#     )
    
#     return JSONResponse(
#         status_code=422,
#         content=ErrorResponse.format_error(
#             error_type="ValidationError",
#             message="Request validation failed",
#             details={"validation_errors": exc.errors()}
#         )
#     )
    

