"""Update inserted data

Revision ID: e96f6f7f9f03
Revises: 9bd5f73a4117
Create Date: 2025-12-09 19:54:22.328177+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e96f6f7f9f03'
down_revision: Union[str, Sequence[str], None] = '9bd5f73a4117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        UPDATE public.topics SET image='/static/uploads/builds.png' WHERE image='/img/builds.png';
        UPDATE public.topics SET image='/static/uploads/bosses.png' WHERE image='/img/bosses.png';
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        UPDATE public.topics SET image='/img/builds.png' WHERE image='/static/uploads/builds.png';
        UPDATE public.topics SET image='/img/bosses.png' WHERE image='/static/uploads/bosses.png';
    """)
