"""change embedding dim to 768 for gemini

Revision ID: 07b5401b6bc4
Revises: 002
Create Date: 2026-05-19 21:55:03.064459
"""
from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision = '07b5401b6bc4'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Vector boyutunu 1536'dan 768'e düşür (Gemini text-embedding-004 için).
    
    pgvector ALTER COLUMN ile boyut değişimini destekler ANCAK
    içeride veri varsa boyut uyuşmaması sorun yaratır.
    O yüzden önce embedding kolonunu NULL'a set ediyoruz, sonra boyutu değiştiriyoruz.
    """
    # 1. Eski (1536-boyutlu) verileri temizle — yenisini seed_routes ile dolduracağız
    op.execute("UPDATE routes SET embedding = NULL")
    
    # 2. HNSW index'i drop et (boyut değişimi için zorunlu)
    op.execute("DROP INDEX IF EXISTS idx_route_embedding_hnsw")
    
    # 3. Vector boyutunu değiştir
    op.alter_column(
        'routes', 'embedding',
        existing_type=pgvector.sqlalchemy.Vector(dim=1536),
        type_=pgvector.sqlalchemy.Vector(dim=768),
        existing_nullable=True,
    )
    
    # 4. HNSW index'i yeniden oluştur (yeni boyutla)
    op.execute("""
        CREATE INDEX idx_route_embedding_hnsw
        ON routes 
        USING hnsw (embedding vector_l2_ops)
        WITH (m = 24, ef_construction = 128)
    """)


def downgrade() -> None:
    """Geri al: 768 → 1536"""
    op.execute("UPDATE routes SET embedding = NULL")
    op.execute("DROP INDEX IF EXISTS idx_route_embedding_hnsw")
    
    op.alter_column(
        'routes', 'embedding',
        existing_type=pgvector.sqlalchemy.Vector(dim=768),
        type_=pgvector.sqlalchemy.Vector(dim=1536),
        existing_nullable=True,
    )
    
    op.execute("""
        CREATE INDEX idx_route_embedding_hnsw
        ON routes
        USING hnsw (embedding vector_l2_ops)
        WITH (m = 24, ef_construction = 128)
    """)
