import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, Text, DateTime, PrimaryKeyConstraint, Index, text

from internal.extension.database_extension import db


# class App(db.Model):
#     """AI应用基础模型类"""
#     __tablename__ = 'app'
#     __table_args__ = (
#         PrimaryKeyConstraint('id', name='pk_app_id'),
#         Index('idx_app_account_id', 'account_id'),
#     )
#
#     id = Column(UUID, default=uuid.uuid4(), primary_key=True, nullable=False)
#     account_id = Column(UUID, nullable=False)
#     name = Column(String(200), default="", nullable=False)
#     icon = Column(String(200), default="", nullable=False)
#     description = Column(Text, default="", nullable=False)
#     update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
#     create_time = Column(DateTime, default=datetime.now, nullable=False)


class App(db.Model):
    """AI应用基础模型类"""
    __tablename__ = 'app'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_app_id'),
        Index('idx_app_account_id', 'account_id'),
    )

    id = Column(UUID, default=uuid.uuid4(), primary_key=True, nullable=False, server_default=text("uuid_generate_v4()"))
    account_id = Column(UUID, nullable=False, server_default=text("''::character varying"))
    name = Column(String(200), default="", nullable=False, server_default=text("''::character varying"))
    icon = Column(String(200), default="", nullable=False, server_default=text("''::character varying"))
    description = Column(Text, default="", nullable=False, server_default=text("''::text"))
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False,
                         server_default=text('CURRENT_TIMESTAMP(0)'), server_onupdate=text('CURRENT_TIMESTAMP(0)'))
    create_time = Column(DateTime, default=datetime.now, nullable=False, server_default=text('CURRENT_TIMESTAMP(0)'),
                         server_onupdate=text('CURRENT_TIMESTAMP(0)'))
