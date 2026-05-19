"""Optimize pgvector HNSW index parametreleri.

Revision ID: 002
Revises: 001
Create Date: 2026-05-19

HNSW (Hierarchical Navigable Small World) parametreleri:
- m: max number of connections per node (4-48, default 16)
  → Küçük = faster build, lower memory; büyük = better quality
- ef_construction: size of dynamic list (ef, default 64)
  → Büyük = better quality, slower construction

Hackathon için: m=24, ef=128 (kalite vs speed dengesi)
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Optimize HNSW indexi."""
    # Mevcut index'i sil
    op.execute("DROP INDEX IF EXISTS idx_route_embedding_hnsw")

    # Yeni HNSW index oluştur (optimized parametrelerle)
    op.execute("""
        CREATE INDEX idx_route_embedding_hnsw
        ON routes
        USING hnsw (embedding vector_l2_ops)
        WITH (m=24, ef_construction=128)
    """)

    print("✅ HNSW index optimized: m=24, ef_construction=128")


def downgrade() -> None:
    """Önceki state'e dön."""
    op.execute("DROP INDEX IF EXISTS idx_route_embedding_hnsw")

    # Default index'e geri dön
    op.execute("""
        CREATE INDEX idx_route_embedding_hnsw
        ON routes
        USING hnsw (embedding vector_l2_ops)
    """)

    print("↩️  HNSW index reverted to defaults")
