from pathlib import Path
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To, From, Content
from jinja2 import Environment, FileSystemLoader
import logging

from app.core import settings

logger = logging.getLogger(__name__)

class EmailService:

    """Email service using SendGrid official SDK with Jinja2 templates"""

    def __init__(self):
        # Debug: Check if API key is loaded
        api_key = settings.SENDGRID_API_KEY
        
        if not api_key or api_key == "SG.your_sendgrid_api_key":
            logger.error(f"⚠️ SENDGRID_API_KEY not configured properly!")
        else:
            logger.info(f"✅ SendGrid API Key loaded: {api_key[:10]}... (length: {len(api_key)})")
        
        self.sg_client = SendGridAPIClient(api_key)
      
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.template_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,  
            trim_blocks=True,
            lstrip_blocks=True
        )

    async def send_verification_email(
            self,
            to_email: str,
            verification_code: str,
            user_name: str ="User"
    )-> bool:
        """Send email verification code using SendGrid SDK"""
        try:
            context = {
                'app_name': settings.APP_NAME,
                'user_name': user_name,
                'verification_code': verification_code,
                'expiry_minutes': settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
            }

            html_template = self.template_env.get_template('verification.html')
            text_template = self.template_env.get_template('verification.txt')

            html_content = html_template.render(**context)
            text_content = text_template.render(**context)

            # Create SendGrid message
            message = Mail(
                from_email=From(settings.MAIL_FROM, settings.MAIL_FROM_NAME),
                to_emails=To(to_email),
                subject=f"Verify your {settings.APP_NAME} account",
                plain_text_content=Content("text/plain", text_content),
                html_content=Content("text/html", html_content)
            )

            logger.info(f"Attempting to send verification email to {to_email}")

            # Send email via SendGrid
            response = self.sg_client.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email} via SendGrid")
                return True
            else:
                logger.error(f"SendGrid returned status {response.status_code}")
                return False
        
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            
            # Enhanced debug output
            print(f"🚨 EMAIL ERROR: {str(e)}")
            print(f"📧 FROM: {settings.MAIL_FROM}")
            print(f"📧 TO: {to_email}")
            print(f"🔑 API Key (first 10 chars): {settings.SENDGRID_API_KEY[:10] if settings.SENDGRID_API_KEY else 'NONE'}")
            
            # Check if it's an auth error
            if "401" in str(e) or "Unauthorized" in str(e):
                print("❌ 401 ERROR MEANS:")
                print("   1. API Key is wrong/expired")
                print("   2. API Key doesn't have 'Mail Send' permission")
                print("   3. .env file not loaded correctly")
            
            return False
        
    async def send_password_reset_email(self, to_email: str, reset_link: str, user_name:  str = "User") -> bool:
        """Send password reset email using SendGrid SDK"""
        try:
            context = {
                'app_name': settings.APP_NAME,
                'user_name': user_name,
                "reset_link": reset_link,
                'expiry_minutes': settings.EMAIL_VERIFICATION_CODE_EXPIRY_MINUTES
            }

            html_template = self.template_env.get_template('reset_password.html')
            text_template = self.template_env.get_template('reset_password.txt')
            html_content = html_template.render(**context)
            text_content = text_template.render(**context)
            
            # Create SendGrid message
            message = Mail(
                from_email=From(settings.MAIL_FROM, settings.MAIL_FROM_NAME),
                to_emails=To(to_email),
                subject=f"Reset your {settings.APP_NAME} password",
                plain_text_content=Content("text/plain", text_content),
                html_content=Content("text/html", html_content)
            )
            
            logger.info(f"Attempting to send password reset email to {to_email}")
            
            # Send email via SendGrid
            response = self.sg_client.send(message)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Password reset email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"SendGrid returned status {response.status_code}")
                return False
                
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




