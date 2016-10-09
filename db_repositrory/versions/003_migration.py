from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mcq_results = Table('mcq_results', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('result', String),
    Column('mcq_id', Integer),
    Column('result_level', Integer),
)

gk_question = Table('gk_question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String),
    Column('image_uri', String),
    Column('level_id', Integer),
    Column('stage', Integer),
)

mcq = Table('mcq', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('question', String),
    Column('level_id', Integer),
    Column('stage', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mcq_results'].create()
    post_meta.tables['gk_question'].columns['image_uri'].create()
    post_meta.tables['gk_question'].columns['level_id'].create()
    post_meta.tables['gk_question'].columns['stage'].create()
    post_meta.tables['mcq'].columns['level_id'].create()
    post_meta.tables['mcq'].columns['stage'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mcq_results'].drop()
    post_meta.tables['gk_question'].columns['image_uri'].drop()
    post_meta.tables['gk_question'].columns['level_id'].drop()
    post_meta.tables['gk_question'].columns['stage'].drop()
    post_meta.tables['mcq'].columns['level_id'].drop()
    post_meta.tables['mcq'].columns['stage'].drop()
