"""empty message

Revision ID: 7333d3464682
Revises: 7af4a439bbbe
Create Date: 2021-10-12 17:46:10.815821

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7333d3464682'
down_revision = '7af4a439bbbe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flights', sa.Column('rampagent_id', sa.Integer(), nullable=True))
    op.drop_constraint('flights_ibfk_1', 'flights', type_='foreignkey')
    op.create_foreign_key(None, 'flights', 'rampagents', ['rampagent_id'], ['id'])
    op.drop_column('flights', 'rampagent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('flights', sa.Column('rampagent', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'flights', type_='foreignkey')
    op.create_foreign_key('flights_ibfk_1', 'flights', 'rampagents', ['rampagent'], ['id'])
    op.drop_column('flights', 'rampagent_id')
    # ### end Alembic commands ###