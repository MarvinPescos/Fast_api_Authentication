from pathlib import Path
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from jinja2 import Environment, FileSystemLoader
import logging

from app.core import settings

logger = logging.getLogger(__name__)

class EmailService:

    """Email service using Brevo (Sendinblue) API with Jinja2 templates"""

    def __init__(self):
        # Configure Brevo API
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )
        
        logger.info(f"✅ Brevo API configured successfully")
      
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
        """Send email verification code using Brevo API"""
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

            # Create Brevo email
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email, "name": user_name}],
                sender={"name": settings.MAIL_FROM_NAME, "email": settings.MAIL_FROM},
                subject=f"Verify your {settings.APP_NAME} account",
                html_content=html_content,
                text_content=text_content
            )

            logger.info(f"Attempting to send verification email to {to_email}")

            # Send email via Brevo
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            
            logger.info(f"✅ Email sent successfully to {to_email} via Brevo (Message ID: {api_response.message_id})")
            return True
        
        except ApiException as e:
            logger.error(f"Brevo API error: {e}")
            print(f"🚨 EMAIL ERROR: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            print(f"🚨 EMAIL ERROR: {str(e)}")
            return False
        
    async def send_password_reset_email(self, to_email: str, reset_link: str, user_name:  str = "User") -> bool:
        """Send password reset email using Brevo API"""
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
            
            # Create Brevo email
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": to_email, "name": user_name}],
                sender={"name": settings.MAIL_FROM_NAME, "email": settings.MAIL_FROM},
                subject=f"Reset your {settings.APP_NAME} password",
                html_content=html_content,
                text_content=text_content
            )
            
            logger.info(f"Attempting to send password reset email to {to_email}")
            
            # Send email via Brevo
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            
            logger.info(f"✅ Password reset email sent successfully to {to_email} (Message ID: {api_response.message_id})")
            return True
                
        except ApiException as e:
            logger.error(f"Brevo API error: {e}")
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




