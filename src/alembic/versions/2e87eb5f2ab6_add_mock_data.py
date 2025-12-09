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
        INSERT INTO users (id, email, password_hash, nickname, name, surname, playing_class)
        VALUES
        (1, 'admin@example.com', 'hashed_password', 'AdminGuy', 'Admin', 'User', 'Knight'),
        (2, 'player1@example.com', 'hashed_pw1', 'Sunbro42', 'Solaire', 'Astora', 'Warrior'),
        (3, 'player2@example.com', 'hashed_pw2', 'TarnishedMage', 'Ranni', 'Carian', 'Mage');
        SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
    """)

    # --- Insert User Relations ---
    op.execute("""
        INSERT INTO user_relations (id, status, type, user_a_id, user_b_id)
        VALUES
        (1, 'accepted', 'friend', 1, 2),
        (2, 'pending', 'friend', 2, 3),
        (3, 'declined', 'blocked', 3, 1);
        SELECT setval('user_relations_id_seq', (SELECT MAX(id) FROM user_relations));
    """)

    # --- Insert Topics ---
    op.execute("""
        INSERT INTO topics (id, title, image, author_id)
        VALUES
        (1, 'Best Dark Souls Builds', '/img/builds.png', 1),
        (2, 'Boss Strategies Megathread', '/img/bosses.png', 2);
        SELECT setval('topics_id_seq', (SELECT MAX(id) FROM topics));
    """)

    # --- Insert Posts ---
    op.execute("""
        INSERT INTO posts (id, title, content, summary, author_id, topic_id)
        VALUES
        (1, 'My favorite STR build', 'Go full strength...', 'STR build guide', 1, 1),
        (2, 'How to defeat Ornstein & Smough', 'Use pillars...', 'Boss tips', 2, 2),
        (3, 'Mage starter tips', 'Use early spells...', 'Mage guide', 3, 1);
        SELECT setval('posts_id_seq', (SELECT MAX(id) FROM posts));
    """)

    # --- Insert Comments ---
    op.execute("""
        INSERT INTO comments (id, content, author_ip_address, author_id, post_id)
        VALUES
        (1, 'Great build, thanks!', '192.168.1.10', 2, 1),
        (2, 'These tips helped a lot.', '10.0.0.20', 3, 2),
        (3, 'I prefer dexterity builds!', '192.168.1.15', 1, 1);
        SELECT setval('comments_id_seq', (SELECT MAX(id) FROM comments));
    """)

    # --- Insert Favorite Posts ---
    op.execute("""
        INSERT INTO favorite_posts (id, user_id, post_id)
        VALUES
        (1, 1, 2),
        (2, 2, 1);
        SELECT setval('favorite_posts_id_seq', (SELECT MAX(id) FROM favorite_posts));
    """)

    # --- Insert Comment Ratings ---
    op.execute("""
        INSERT INTO comment_ratings (id, rating, user_id, comment_id)
        VALUES
        (1, 'positive', 1, 1),
        (2, 'positive', 2, 2),
        (3, 'negative', 3, 3);
        SELECT setval('comment_ratings_id_seq', (SELECT MAX(id) FROM comment_ratings));
    """)

    # --- Insert Games ---
    op.execute("""
        INSERT INTO games (id, name, hours_played, user_id)
        VALUES
        (1, 'Dark Souls Remastered', 120, 1),
        (2, 'Elden Ring', 200, 2),
        (3, 'Dark Souls 3', 80, 3);
        SELECT setval('games_id_seq', (SELECT MAX(id) FROM games));
    """)

    # --- Insert Steam Accounts ---
    op.execute("""
        INSERT INTO steam_accounts (id, steam_id, user_id)
        VALUES
        (1, 'STEAM_0001', 1),
        (2, 'STEAM_0002', 2),
        (3, 'STEAM_0003', 3);
        SELECT setval('steam_accounts_id_seq', (SELECT MAX(id) FROM steam_accounts));
    """)
