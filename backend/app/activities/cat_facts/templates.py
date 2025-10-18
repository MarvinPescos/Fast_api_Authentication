"""
Email templates for Cat Facts feature
Adapted for Brevo email service
"""
from app.core import settings

def get_cat_fact_html_template(cat_fact: str, current_date: str, user_name: str = "Friend") -> str:
    """Generate HTML email template for cat fact"""
    unsubscribe_link = f"{settings.FRONTEND_URL}/dashboard"  # Link to dashboard to unsubscribe

    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #ff6b6b; margin-bottom: 10px;">🐱 Daily Cat Fact!</h1>
                <p style="color: #666; font-size: 18px;">{current_date}</p>
                <p style="color: #888; font-size: 14px;">Hello, {user_name}! 👋</p>
            </div>

            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.95); padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; margin-bottom: 20px; font-size: 24px;">🐾 Did You Know?</h2>
                    <p style="font-size: 18px; color: #555; line-height: 1.8; margin: 0; font-style: italic;">
                        "{cat_fact}"
                    </p>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <div style="display: inline-block; padding: 15px 30px; background: #ff6b6b; color: white; border-radius: 25px; font-weight: bold; font-size: 16px;">
                    🌟 Have a purrfect day! 🌟
                </div>
            </div>

            <div style="text-align: center; margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 10px; border-top: 3px solid #ff6b6b;">
                <p style="color: #666; font-size: 14px; margin: 0 0 10px 0;">
                    Daily cat facts delivered with ❤️ from BalanceHub
                </p>
                <p style="color: #999; font-size: 12px; margin: 0;">
                    Don't want daily cat facts? <a href="{unsubscribe_link}" style="color: #ff6b6b; text-decoration: none;">Unsubscribe here</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """


def get_cat_fact_text_template(cat_fact: str, current_date: str, user_name: str = "Friend") -> str:
    """Generate plain text email template for cat fact"""
    return f"""
🐱 DAILY CAT FACT 🐱
{current_date}

Hello, {user_name}! 👋

🐾 Did You Know?
"{cat_fact}"

🌟 Have a purrfect day! 🌟

---
Daily cat facts delivered with ❤️ from BalanceHub

Don't want daily cat facts? Visit your dashboard to unsubscribe.
    """.strip()


def get_welcome_subscription_html(user_name: str) -> str:
    """Welcome email when user subscribes to cat facts"""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #ff6b6b; margin-bottom: 10px;">🎉 Welcome to Daily Cat Facts!</h1>
            </div>

            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">
                <p style="font-size: 16px; color: #333; margin-bottom: 15px;">
                    Hi {user_name},
                </p>
                <p style="font-size: 16px; color: #555; line-height: 1.8;">
                    Thank you for subscribing to Daily Cat Facts! 🐱
                </p>
                <p style="font-size: 16px; color: #555; line-height: 1.8;">
                    You'll receive a fascinating cat fact every day at your preferred time.
                    Get ready to become a cat expert! 😺
                </p>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #666; font-size: 14px;">
                    Your first cat fact is on its way!
                </p>
            </div>
        </div>
    </body>
    </html>
    """


def get_welcome_subscription_text(user_name: str) -> str:
    """Welcome text email when user subscribes"""
    return f"""
🎉 WELCOME TO DAILY CAT FACTS! 🎉

Hi {user_name},

Thank you for subscribing to Daily Cat Facts! 🐱

You'll receive a fascinating cat fact every day at your preferred time.
Get ready to become a cat expert! 😺

Your first cat fact is on its way!

---
BalanceHub Team
    """.strip()
