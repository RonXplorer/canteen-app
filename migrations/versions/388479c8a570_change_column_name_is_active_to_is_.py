"""change column name is_active to is_validated from User table

Revision ID: 388479c8a570
Revises: 86d9ffdad534
Create Date: 2024-12-10 12:44:27.345585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '388479c8a570'
down_revision = '86d9ffdad534'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Crear la nueva columna
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_validated', sa.Boolean(), nullable=True))
    
    # Transferir datos de 'is_active' a 'is_validated'
    op.execute("""
        UPDATE users
        SET is_validated = is_active
    """)

    # Eliminar la columna antigua
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), nullable=True))
        batch_op.drop_column('is_validated')

    # ### end Alembic commands ###
