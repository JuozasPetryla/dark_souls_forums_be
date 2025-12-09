"""Add created_at and updated_at to user_relations"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'add_user_relations_timestamps'
down_revision = 'e96f6f7f9f03'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "user_relations",
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("NOW()")
        )
    )

    op.alter_column(
        "user_relations",
        "updated_at",
        server_default=sa.text("NOW()"),
        existing_type=sa.DateTime(),
        nullable=False
    )


def downgrade() -> None:
    op.drop_column("user_relations", "created_at")
