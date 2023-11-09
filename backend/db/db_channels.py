"""БД, каналы групповые и новостные"""
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
    """Все групповые каналы"""
    result = session.execute(
        select(GroupChannel)
    )
    channels = result.scalars().all()
    return channels


def get_group_channel(
        session: Session,
        id_transmitter: int,
        capcode: int,
        id_fbit: int
) -> GroupChannel | None:
    """Групповой канал по id"""
    channel = session.get(GroupChannel, (id_transmitter, capcode, id_fbit))
    return channel


def create_group_channel(
        session: Session,
        group_channel_schema_item: GroupChannelSchema
) -> GroupChannel:
    """Создать групповой канал"""
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
    """Удалить групповой канал"""
    channel = session.get(GroupChannel, (id_transmitter, capcode, id_fbit))
    if channel:
        session.delete(channel)
        session.commit()
        return True
    return False


def get_maildrop_channels(session: Session):
    """Все новостные каналы"""
    result = session.execute(
        select(MailDropChannel)
    )
    channels = result.scalars().all()
    return channels


def get_maildrop_channel(
        session: Session,
        id_transmitter: int,
        capcode: int,
        id_fbit: int
) -> MailDropChannel | None:
    """Новостной канал по id"""
    channel = session.get(MailDropChannel, (id_transmitter, capcode, id_fbit))
    return channel


def create_maildrop_channel(
        session: Session,
        maildrop_channel_schema_item: MailDropChannelSchema
) -> MailDropChannel:
    """Создать новостной канал"""
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


def delete_maildrop_channel(
        session: Session,
        id_transmitter: int,
        capcode: int,
        id_fbit: int
) -> bool:
    """Удалить новостной канал"""
    channel = session.get(MailDropChannel, (id_transmitter, capcode, id_fbit))
    if channel:
        session.delete(channel)
        session.commit()
        return True
    return False


def get_group_channels_by_type(session: Session, id_group_type: int):
    """Групповые каналы по конкретному типу"""
    result = session.execute(
        select(GroupChannel)
        .where(
            GroupChannel.id_group_type == id_group_type
        )
    )
    channels = result.scalars().all()
    return channels


def get_maildrop_channels_by_type(session: Session, id_maildrop_type: int):
    """Новостные каналы по конкретному типу"""
    result = session.execute(
        select(MailDropChannel)
        .where(
            MailDropChannel.id_maildrop_type == id_maildrop_type
        )
    )
    channels = result.scalars().all()
    return channels


def get_rss_feeds(session: Session):
    """Все RSS-ленты"""
    result = session.execute(
        select(MaildropRssFeed)
    )
    feeds = result.scalars().all()
    return feeds


def get_rss_feed(session: Session, id_feed: int) -> MaildropRssFeed | None:
    """RSS-лента по id"""
    feed = session.get(MaildropRssFeed, id_feed)
    return feed


def create_rss_feed(
        session: Session,
        maildrop_rss_feed_schema_item: MaildropRssFeedSchema
) -> MailDropChannel:
    """Создать RSS-ленту"""
    feed = MaildropRssFeed(
        id_maildrop_type=maildrop_rss_feed_schema_item.id_maildrop_type.value,
        feed_link=maildrop_rss_feed_schema_item.feed_link,
    )
    session.add(feed)
    session.commit()
    session.refresh(feed)
    return feed


def delete_rss_feed(session: Session, id_feed: int) -> bool:
    """Удалить RSS-ленту"""
    feed = session.get(MaildropRssFeed, id_feed)
    if feed:
        session.delete(feed)
        session.commit()
        return True
    return False


def get_rss_feed_by_maildrop_type(
        session: Session,
        id_maildrop_type: int
) -> MaildropRssFeed | None:
    """Возвращает RSS-ленту, связанную с этим id_maildrop_type """
    result = session.execute(
        select(MaildropRssFeed)
        .where(
            MaildropRssFeed.id_maildrop_type == id_maildrop_type
        )
    )
    return result.scalar()
