"""Initial schema with pgvector support

Revision ID: 001
Revises:
Create Date: 2026-05-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    op.create_table(
        'travel_goals',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_wallet', sa.String(), nullable=False),
        sa.Column('destination', sa.String(), nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.Column('travel_date', sa.String(), nullable=False),
        sa.Column('budget_usd', sa.Float(), nullable=False),
        sa.Column('status', sa.String(), nullable=False, server_default='pending'),
        sa.Column('final_report_md', sa.Text(), nullable=True),
        sa.Column('solana_goal_pda', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_travel_goals_user_wallet', 'user_wallet')
    )

    op.create_table(
        'sponsorships',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('sponsor_wallet', sa.String(), nullable=False),
        sa.Column('amount_sol', sa.Float(), nullable=False),
        sa.Column('tx_signature', sa.String(), nullable=True),
        sa.Column('refunded', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'agent_logs',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('agent_name', sa.String(), nullable=False),
        sa.Column('input_json', sa.Text(), nullable=False),
        sa.Column('output_json', sa.Text(), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'routes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.Column('destination', sa.String(), nullable=False),
        sa.Column('description_md', sa.Text(), nullable=False),
        sa.Column('tags', sa.String(), nullable=False),
        sa.Column('copy_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('embedding', Vector(1536), nullable=True),
        sa.Column('creator_wallet', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'price_history',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('flight_price_usd', sa.Float(), nullable=True),
        sa.Column('hotel_price_usd', sa.Float(), nullable=True),
        sa.Column('is_buy_signal', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('recorded_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('price_history')
    op.drop_table('routes')
    op.drop_table('agent_logs')
    op.drop_table('sponsorships')
    op.drop_table('travel_goals')
    op.execute('DROP EXTENSION IF EXISTS vector')
