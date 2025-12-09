"""mock data 
Revision ID: seed_mock_data 
Revises: d3eb6750106c 
Create Date: 2025-12-08 
""" 
from typing import Sequence, Union 
from alembic import op 
import sqlalchemy as sa 

revision: str = "seed_mock_data" 
down_revision: Union[str, Sequence[str], None] = "4301a7eb3cf0" 
branch_labels = None 
depends_on = None

def upgrade() -> None:
    # --- Insert Users ---
    op.execute("""
        INSERT INTO users (email, password_hash, nickname, name, surname, playing_class)
        VALUES
        ('admin@example.com', 'hashed_password', 'AdminGuy', 'Admin', 'User', 'Knight'),
        ('player1@example.com', 'hashed_pw1', 'Sunbro42', 'Solaire', 'Astora', 'Warrior'),
        ('player2@example.com', 'hashed_pw2', 'TarnishedMage', 'Ranni', 'Carian', 'Mage');
    """)

    # --- Insert User Relations ---
    op.execute("""
        INSERT INTO user_relations (status, type, user_a_id, user_b_id)
        VALUES
        ('accepted', 'friend', 1, 2),
        ('pending', 'friend', 2, 3),
        ('declined', 'blocked', 3, 1);
    """)

    # --- Insert Topics ---
    op.execute("""
        INSERT INTO topics (title, image, author_id)
        VALUES
        ('Best Dark Souls Builds', '/img/builds.png', 1),
        ('Boss Strategies Megathread', '/img/bosses.png', 2);
    """)

    # --- Insert Posts ---
    op.execute("""
        INSERT INTO posts (title, content, summary, author_id, topic_id)
        VALUES
        ('My favorite STR build', 'Go full strength...', 'STR build guide', 1, 1),
        ('How to defeat Ornstein & Smough', 'Use pillars...', 'Boss tips', 2, 2),
        ('Mage starter tips', 'Use early spells...', 'Mage guide', 3, 1);
    """)

    # --- Insert Comments ---
    op.execute("""
        INSERT INTO comments (content, author_ip_address, author_id, post_id)
        VALUES
        ('Great build, thanks!', '192.168.1.10', 2, 1),
        ('These tips helped a lot.', '10.0.0.20', 3, 2),
        ('I prefer dexterity builds!', '192.168.1.15', 1, 1);
    """)

    # --- Insert Favorite Posts ---
    op.execute("""
        INSERT INTO favorite_posts (user_id, post_id)
        VALUES
        (1, 2),
        (2, 1);
    """)

    # --- Insert Comment Ratings ---
    op.execute("""
        INSERT INTO comment_ratings (rating, user_id, comment_id)
        VALUES
        ('positive', 1, 1),
        ('positive', 2, 2),
        ('negative', 3, 3);
    """)

    # --- Insert Games ---
    op.execute("""
        INSERT INTO games (name, hours_played, user_id)
        VALUES
        ('Dark Souls Remastered', 120, 1),
        ('Elden Ring', 200, 2),
        ('Dark Souls 3', 80, 3);
    """)

    # --- Insert Steam Accounts ---
    op.execute("""
        INSERT INTO steam_accounts (steam_id, user_id)
        VALUES
        ('STEAM_0001', 1),
        ('STEAM_0002', 2),
        ('STEAM_0003', 3);
    """)
