import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.model_channels import (GroupChannel, GroupChannelSchema,
                                           MailDropChannel,
                                           MailDropChannelSchema,
                                           MaildropRssFeed,
                                           MaildropRssFeedSchema)

LOGGER = logging.getLogger()


def get_group_channels(session: Session):
    result = session.execute(
        select(GroupChannel)
    )
    channels = result.scalars().all()
    return channels


def get_group_channel(session: Session, id_transmitter: int, capcode: int, id_fbit: int) -> GroupChannel:
    channel = session.get(GroupChannel, (id_transmitter, capcode, id_fbit))
    return channel


def create_group_channel(session: Session, group_channel_schema_item: GroupChannelSchema) -> GroupChannel:
    channel = GroupChannel(
        id_transmitter=group_channel_schema_item.id_transmitter,
        capcode=group_channel_schema_item.capcode,
        id_fbit=group_channel_schema_item.id_fbit.value,
        id_group_type=group_channel_schema_item.id_group_type.value,
        id_codepage=group_channel_schema_item.id_codepage.value,
    )
    session.add(channel)
    session.commit()
    session.refresh(channel)
    return channel


def delete_group_channel(session: Session, id_transmitter: int, capcode: int, id_fbit: int) -> bool:
    result = False
    channel = session.get(GroupChannel, (id_transmitter, capcode, id_fbit))
    if channel:
        session.delete(channel)
        session.commit()
        result = True
    return result


def get_maildrop_channels(session: Session):
    result = session.execute(
        select(MailDropChannel)
    )
    channels = result.scalars().all()
    return channels


def get_maildrop_channel(session: Session, id_transmitter: int, capcode: int, id_fbit: int) -> MailDropChannel:
    channel = session.get(MailDropChannel, (id_transmitter, capcode, id_fbit))
    return channel


def create_maildrop_channel(session: Session, maildrop_channel_schema_item: MailDropChannelSchema) -> MailDropChannel:
    channel = MailDropChannel(
        id_transmitter=maildrop_channel_schema_item.id_transmitter,
        capcode=maildrop_channel_schema_item.capcode,
        id_fbit=maildrop_channel_schema_item.id_fbit.value,
        id_maildrop_type=maildrop_channel_schema_item.id_maildrop_type.value,
        id_codepage=maildrop_channel_schema_item.id_codepage.value,
    )
    session.add(channel)
    session.commit()
    session.refresh(channel)
    return channel


def delete_maildrop_channel(session: Session, id_transmitter: int, capcode: int, id_fbit: int) -> bool:
    result = False
    channel = session.get(MailDropChannel, (id_transmitter, capcode, id_fbit))
    if channel:
        session.delete(channel)
        session.commit()
        result = True
    return result


def get_group_channels_by_type(session: Session, id_group_type: int):
    result = session.execute(
        select(GroupChannel)
        .where(
            GroupChannel.id_group_type == id_group_type
        )
    )
    channels = result.scalars().all()
    return channels


def get_maildrop_channels_by_type(session: Session, id_maildrop_type: int):
    result = session.execute(
        select(MailDropChannel)
        .where(
            MailDropChannel.id_maildrop_type == id_maildrop_type
        )
    )
    channels = result.scalars().all()
    return channels


def get_rss_feeds(session: Session):
    result = session.execute(
        select(MaildropRssFeed)
    )
    feeds = result.scalars().all()
    return feeds


def get_rss_feed(session: Session, id_feed: int) -> MaildropRssFeed:
    feed = session.get(MaildropRssFeed, id_feed)
    return feed


def create_rss_feed(session: Session, maildrop_rss_feed_schema_item: MaildropRssFeedSchema) -> MailDropChannel:
    feed = MaildropRssFeed(
        id_maildrop_type=maildrop_rss_feed_schema_item.id_maildrop_type.value,
        feed_link=maildrop_rss_feed_schema_item.feed_link,
    )
    session.add(feed)
    session.commit()
    session.refresh(feed)
    return feed


def delete_rss_feed(session: Session, id_feed: int) -> bool:
    result = False
    feed = session.get(MaildropRssFeed, id_feed)
    if feed:
        session.delete(feed)
        session.commit()
        result = True
    return result


def get_rss_feed_by_maildrop_type(session: Session, id_maildrop_type: int) -> MaildropRssFeed:
    """Возвращает RSS-ленту, связанную с этим id_maildrop_type """
    result = session.execute(
        select(MaildropRssFeed)
        .where(
            MaildropRssFeed.id_maildrop_type == id_maildrop_type
        )
    )
    return result.scalar()
