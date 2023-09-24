import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.model_channels import (GroupChannel, GroupChannelSchema,
                                           MailDropChannel,
                                           MailDropChannelSchema)

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
