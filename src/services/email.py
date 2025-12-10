from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=587,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False
)

async def send_friend_request_email(to_email: str, from_username: str):
    html = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #0d0d0d; padding: 30px;">
        <table width="100%" style="max-width: 600px; margin: auto; background-color: #1b1b1b; border-radius: 8px; padding: 20px; color: #f5f5f5;">
            <tr>
                <td style="text-align: center; padding-bottom: 20px;">
                    <h2 style="color: #e0e0e0;">🔥 Dark Souls Forum</h2>
                </td>
            </tr>
            <tr>
                <td>
                    <p style="font-size: 16px; line-height: 1.5;">
                        <strong style="color: #d18400;">{from_username}</strong> has sent you a friend request!
                    </p>

                    <p style="font-size: 15px; line-height: 1.5; color: #bbbbbb;">
                        Connect with them in the bonfires of the Dark Souls community.
                    </p>

                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:5173"
                           style="background-color: #d18400; 
                                  color: white; 
                                  padding: 12px 25px; 
                                  text-decoration: none; 
                                  border-radius: 6px;
                                  font-size: 15px;">
                            View Friend Request
                        </a>
                    </div>

                    <p style="font-size: 14px; color: #777; text-align: center;">
                        If you did not expect this request, feel free to ignore this message.
                    </p>

                    <hr style="border: 0; border-top: 1px solid #333; margin: 25px 0;">

                    <p style="font-size: 12px; color: #666; text-align: center;">
                        © 2025 Dark Souls Forum. Not affiliated with FromSoftware.
                    </p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    message = MessageSchema(
        subject=f"{from_username} sent you a friend request",
        recipients=[to_email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)
