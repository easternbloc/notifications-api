"""empty message

Revision ID: 0006_add_user_details
Revises: 0005_add_job_details
Create Date: 2016-01-19 11:16:06.518285

"""

# revision identifiers, used by Alembic.
revision = '0006_add_user_details'
down_revision = '0005_add_job_details'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('_password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('failed_login_count', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('logged_in_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('mobile_number', sa.String(), nullable=False))
    op.add_column('users', sa.Column('name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('password_changed_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('state', sa.String(), nullable=False))
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_column('users', 'state')
    op.drop_column('users', 'password_changed_at')
    op.drop_column('users', 'name')
    op.drop_column('users', 'mobile_number')
    op.drop_column('users', 'logged_in_at')
    op.drop_column('users', 'failed_login_count')
    op.drop_column('users', '_password')
    ### end Alembic commands ###
