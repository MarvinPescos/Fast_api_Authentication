from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from jinja2 import Environment, FileSystemLoader
import logging

from app.core import settings

logger = logging.getLogger(__name__)

class EmailService:

    """Email service using fastapi-mail with SendGrid and Jinja2 templates"""

    def __init__(self):
        #Configure fastapi-mail with SendGrid
        self.conf = ConnectionConfig(
            MAIL_USERNAME="apikey",
            MAIL_PASSWORD=settings.SENDGRID_API_KEY,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.sendgrid.net",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.conf)
        
        # Configure Jinja2 templates - Industry Standard Pattern
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.template_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,  # Security: Auto-escape HTML
            trim_blocks=True,
            lstrip_blocks=True
        )

    async def send_verification_email(
            self,
            to_email: str,
            verification_code: str,
            user_name: str ="User"
    )-> bool:
        """Send email verification code using templatee"""
        try:
            context = {
                'app_name': settings.APP_NAME,
                'user_name': user_name,
                'verification_code': verification_code,
                'expiry_minutes': settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
            }

            html_template = self.template_env.get_template('verification.html')
            text_template = self.template_env.get_template('verification.txt')

            html_context = html_template.render(**context)
            text_context = text_template.render(**context)

            message = MessageSchema(
                subject=f"Verify your {settings.APP_NAME} account ",
                recipients=[to_email],
                body=text_context,
                html=html_context,
                subtype=MessageType.html
            )

            logger.info(f"Attempting to send verification email to {to_email}")

            await self.fastmail.send_message(message)

            logger.info(f"Email sent to succesfully to {to_email} via SendGrid")

            return True
        
        except ConnectionErrors as e:
            logger.error(f"SendGrid connection error for {to_email}: {str(e)}")
            print(f"🚨 CONNECTION ERROR: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            if settings.DEBUG:
                print(f"🚨 EMAIL ERROR: {str(e)}")
                print(f"📧 FROM: {settings.MAIL_FROM}")
            return False
        
    async def send_password_reset_email(self, to_email: str, reset_link: str, user_name:  str = "User") -> bool:
        try:
            context = {
                'app_name': settings.APP_NAME,
                'user_name': user_name,
                "reset_link": reset_link,
                'expiry_minutes': settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
            }

            html_template = self.template_env.get_template('reset_password.html')
            text_template = self.template_env.get_template('reset_password.txt')
            html_context = html_template.render(**context)
            text_context = text_template.render(**context)
            message = MessageSchema(
                subject=f"Reset your {settings.APP_NAME} password",
                recipients=[to_email],
                body=text_context,
                html=html_context,
                subtype=MessageType.html
            )
            await self.fastmail.send_message(message)
            return True
        except Exception as e:
            logger.error(f"Failed to send password reset email to {to_email}: {str(e)}")
            return False
        
email_service = EmailService()

async def send_verification_email(
        to_email: str,
        verification_code: str,
        user_name: str = "User"
) -> bool:
    """Convenience Function to send verification email"""
    return await email_service.send_verification_email(to_email, verification_code, user_name)

async def send_password_reset_email(to_email: str, reset_link: str, user_name: str = "User") -> bool:
    return await email_service.send_password_reset_email(to_email, reset_link, user_name)




