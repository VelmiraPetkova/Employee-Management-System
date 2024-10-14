"""change user model

Revision ID: 36aed04b07a3
Revises: a75f553f54a4
Create Date: 2024-10-13 19:10:43.248572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36aed04b07a3'
down_revision = 'a75f553f54a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=200),
               existing_nullable=False)
    op.drop_constraint('users_contract_id_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_company_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'company_id')
    op.drop_column('users', 'contract_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('contract_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('company_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_company_id_fkey', 'users', 'company', ['company_id'], ['id'])
    op.create_foreign_key('users_contract_id_fkey', 'users', 'contracts', ['contract_id'], ['id'])
    op.alter_column('users', 'password',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###
