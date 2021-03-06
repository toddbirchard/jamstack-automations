from datetime import datetime

from sqlalchemy.engine.result import ResultProxy
from sqlalchemy.orm import Session

from clients.log import LOGGER
from database.models import Comment, Donation, Account
from database.schemas import NewComment, NewDonation, NetlifyAccount


def get_donation(db: Session, donation_id: int) -> ResultProxy:
    """
    Fetch BuyMeACoffee donation by ID.

    :param db: ORM database session.
    :type db: Session
    :param donation_id: Primary key for donation record.
    :type donation_id: int
    :returns: ResultProxy
    """
    return db.query(Donation).filter(Donation.coffee_id == donation_id).first()


def create_donation(db: Session, donation: NewDonation) -> Donation:
    """
    Create new BuyMeACoffee donation record.

    :param db: ORM database session.
    :type db: Session
    :param donation: Donation schema object.
    :type donation: NewDonation
    :returns: Donation
    """
    db_item = Donation(
        email=donation.email,
        name=donation.name,
        count=donation.count,
        message=donation.message,
        link=donation.link,
        coffee_id=donation.coffee_id,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    return db_item


def get_comment(db: Session, comment_id: int) -> ResultProxy:
    """
    Fetch BuyMeACoffee donation by ID.

    :param db: ORM database session.
    :type db: Session
    :param comment_id: Primary key for user comment record.
    :type comment_id: int
    :returns: ResultProxy
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment: NewComment):
    """
    Create new BuyMeACoffee donation record.

    :param db: ORM database session.
    :type db: Session
    :param comment: User comment schema object.
    :type comment: NewComment
    :returns: NewComment
    """
    new_comment = Comment(
        user_name=comment.user_name,
        user_avatar=comment.user_avatar,
        user_id=comment.user_id,
        user_email=comment.user_email,
        user_role=comment.user_role,
        body=comment.body,
        created_at=datetime.now(),
        post_slug=comment.post_slug,
        post_id=comment.post_id,
    )
    db.add(new_comment)
    db.commit()
    LOGGER.success(
        f"New comment submitted by user `{new_comment.user_name}` on post `{new_comment.post_slug}`"
    )
    return new_comment


def get_account(db: Session, account_email: str) -> ResultProxy:
    """
    Fetch account by email address.

    :param db: ORM database session.
    :type db: Session
    :param account_email: Primary key for account record.
    :type account_email: str
    :returns: ResultProxy
    """
    return db.query(Account).filter(Account.email == account_email).first()


def create_account(db: Session, account: NetlifyAccount) -> NetlifyAccount:
    """
    Create new account record sourced from Netlify.

    :param db: ORM database session.
    :type db: Session
    :param account: User comment schema object.
    :type account: NetlifyAccount
    :returns: NetlifyAccount
    """
    new_account = Account(
        id=account.id,
        full_name=account.user_metadata.full_name,
        avatar_url=account.user_metadata.avatar_url,
        email=account.email,
        role=account.role,
        provider=account.app_metadata.provider,
        created_at=account.created_at,
        updated_at=account.updated_at,
    )
    db.add(new_account)
    db.commit()
    LOGGER.success(f"New account created `{account.user_metadata.full_name}`")
    return account
