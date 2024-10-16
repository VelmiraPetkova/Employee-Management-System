"""change user model

Revision ID: 61157b325cf5
Revises: 36aed04b07a3
Create Date: 2024-10-13 19:12:03.022399

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61157b325cf5'
down_revision = '36aed04b07a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('contract_id', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'contracts', ['contract_id'], ['id'])
    op.create_foreign_key(None, 'users', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'company_id')
    op.drop_column('users', 'contract_id')
    # ### end Alembic commands ###