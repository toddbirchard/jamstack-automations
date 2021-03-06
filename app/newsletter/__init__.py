"""Newsletter subscription management."""
from fastapi import APIRouter

from clients import mailgun
from clients.log import LOGGER
from config import settings
from database.schemas import Subscription, SubscriptionWelcomeEmail

router = APIRouter(prefix="/subscription", tags=["newsletter"])


@router.post(
    "/",
    summary="Welcome newsletter subscriber.",
    description="Send a welcome email to new subscribers to Ghost newsletter.",
    response_model=SubscriptionWelcomeEmail,
)
async def newsletter_subscribe(subscription: Subscription):
    """Send welcome email to newsletter subscriber."""
    body = {
        "from": "todd@hackersandslackers.com",
        "to": subscription.member.current.email,
        "subject": settings.MAILGUN_SUBJECT_LINE,
        "template": settings.MAILGUN_EMAIL_TEMPLATE,
        "h:X-Mailgun-Variables": {"name": subscription.member.current.name},
        "o:tracking": True,
    }
    response = mailgun.send_email(body)
    if bool(response):
        return SubscriptionWelcomeEmail(
            from_email=settings.MAILGUN_PERSONAL_EMAIL,
            to_email=subscription.member.current.email,
            subject=settings.MAILGUN_SUBJECT_LINE,
            template=settings.MAILGUN_EMAIL_TEMPLATE,
        ).dict()


@router.delete("/")
async def newsletter_unsubscribe(subscription: Subscription):
    """Track user unsubscribe events and spam complaints."""
    LOGGER.info(f"`{subscription.member.previous.name}` unsubscribed from newsletter.")
    return subscription.member.previous.dict()
