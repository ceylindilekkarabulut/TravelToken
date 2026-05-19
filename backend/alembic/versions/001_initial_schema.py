"""Initial schema with all tables and pgvector extension.

Revision ID: 001
Revises:
Create Date: 2026-05-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Create users table
    op.create_table(
        'users',
        sa.Column('wallet_address', sa.String(), nullable=False),
        sa.Column('display_name', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('total_sponsored_sol', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('wallet_address')
    )

    # Create travel_goals table
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
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_travel_goals_user_wallet', 'user_wallet')
    )

    # Create sponsorships table
    op.create_table(
        'sponsorships',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('sponsor_wallet', sa.String(), nullable=False),
        sa.Column('amount_sol', sa.Float(), nullable=False),
        sa.Column('tx_signature', sa.String(), nullable=True),
        sa.Column('refunded', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create agent_logs table
    op.create_table(
        'agent_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('agent_name', sa.String(), nullable=False),
        sa.Column('input_json', sa.Text(), nullable=False),
        sa.Column('output_json', sa.Text(), nullable=False),
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_logs_goal_id'), 'agent_logs', ['goal_id'], unique=False)

    # Create routes table
    op.create_table(
        'routes',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('origin', sa.String(), nullable=False),
        sa.Column('destination', sa.String(), nullable=False),
        sa.Column('description_md', sa.Text(), nullable=False),
        sa.Column('tags', sa.String(), nullable=False),
        sa.Column('copy_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('embedding', Vector(768), nullable=True),
        sa.Column('creator_wallet', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create price_history table
    op.create_table(
        'price_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('goal_id', sa.String(), nullable=False),
        sa.Column('flight_price_usd', sa.Float(), nullable=True),
        sa.Column('hotel_price_usd', sa.Float(), nullable=True),
        sa.Column('is_buy_signal', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('recorded_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['goal_id'], ['travel_goals.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_price_history_goal_id'), 'price_history', ['goal_id'], unique=False)

    # Create notification_subscriptions table
    op.create_table(
        'notification_subscriptions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wallet_address', sa.String(), nullable=False),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_notification_subscriptions_wallet_address', 'wallet_address')
    )


def downgrade() -> None:
    op.drop_index(op.f('ix_notification_subscriptions_wallet_address'), table_name='notification_subscriptions')
    op.drop_table('notification_subscriptions')
    op.drop_index(op.f('ix_price_history_goal_id'), table_name='price_history')
    op.drop_table('price_history')
    op.drop_table('routes')
    op.drop_index(op.f('ix_agent_logs_goal_id'), table_name='agent_logs')
    op.drop_table('agent_logs')
    op.drop_table('sponsorships')
    op.drop_table('travel_goals')
    op.drop_table('users')
    op.execute('DROP EXTENSION IF EXISTS vector')
