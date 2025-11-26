from alembic import op
import sqlalchemy as sa

revision = 'db1a61ae1c46'
down_revision = 'be4a35e14cc8'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('purchase_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)


def downgrade():
    with op.batch_alter_table('purchases', schema=None) as batch_op:
        batch_op.alter_column('purchase_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
