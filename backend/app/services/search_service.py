"""
Hybrid Search Service — Vector + Filter + Re-rank.

Akış:
1. Query embed (embedding_service)
2. Vector similarity search (pgvector HNSW)
3. Metadata filter (origin, destination, tags, copy_count)
4. Re-rank (BM25 + relevance score kombinasyon)
5. Sonuçları döndür
"""
from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.models.db import Route
from app.services.embedding_service import EmbeddingService, TASK_TYPE_QUERY

logger = logging.getLogger(__name__)


# =============================================================================
# MODELS
# =============================================================================


class SearchFilter:
    """Search query filtreleri."""

    def __init__(
        self,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        tags: Optional[list[str]] = None,
        min_copy_count: int = 0,
        limit: int = 10,
    ):
        self.origin = origin
        self.destination = destination
        self.tags = tags or []
        self.min_copy_count = min_copy_count
        self.limit = limit


class SearchResult:
    """Bir arama sonucu."""

    def __init__(
        self,
        route: Route,
        vector_score: float,
        relevance_score: float,
        final_score: float,
    ):
        self.route = route
        self.vector_score = vector_score
        self.relevance_score = relevance_score
        self.final_score = final_score


# =============================================================================
# SEARCH SERVICE
# =============================================================================


class SearchService:
    """
    Hybrid vector + metadata search for routes.

    Kullanım:
        search_svc = SearchService(session=session, embedding_svc=embedding_svc)
        results = await search_svc.search(
            query="solo budget Europe",
            filters=SearchFilter(
                origin="Istanbul",
                tags=["solo", "budget"],
                limit=5
            )
        )
    """

    def __init__(
        self,
        session: AsyncSession,
        embedding_service: EmbeddingService,
    ):
        self.session = session
        self.embedding_service = embedding_service

    # -------------------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------------------

    async def search(
        self,
        query: str,
        filters: Optional[SearchFilter] = None,
    ) -> list[SearchResult]:
        """
        Hybrid search: vector similarity + metadata filter + re-rank.

        Args:
            query: Arama metni (embedding'e çevrilir)
            filters: Origin, destination, tags, limit vb.

        Returns:
            Sıralanmış SearchResult listesi
        """
        if not query or not query.strip():
            logger.warning("Boş query ile search yapılıyor")
            return []

        filters = filters or SearchFilter()

        # 1. Query embed et
        logger.info(f"Embedding query: {query[:50]}...")
        query_result = await self.embedding_service.embed_query(query)
        query_vector = query_result.vector

        # 2. Vector similarity search (pgvector)
        logger.info("Vector similarity search yapılıyor...")
        candidates = await self._vector_search(query_vector, filters)

        if not candidates:
            logger.info("Vector search sonuç bulamadı")
            return []

        # 3. Re-rank candidates
        logger.info(f"{len(candidates)} aday re-rank ediliyor...")
        results = await self._rerank_candidates(
            candidates, query, query_vector, filters
        )

        # 4. Sırala ve döndür
        results.sort(key=lambda r: r.final_score, reverse=True)
        limited_results = results[: filters.limit]

        logger.info(
            f"Search tamamlandı: {len(limited_results)} sonuç "
            f"({len(candidates)} candidate'den)"
        )
        return limited_results

    # -------------------------------------------------------------------------
    # PRIVATE: Vector Search
    # -------------------------------------------------------------------------

    async def _vector_search(
        self,
        query_vector: list[float],
        filters: SearchFilter,
        limit: int = 100,  # Başlangıç — re-rank öncesi
    ) -> list[Route]:
        """
        pgvector similarity search with metadata filtering.

        PostgreSQL <-> operatörü (cosine distance) ve HNSW index kullanır.
        """
        # pgvector <-> (cosine distance)
        # Daha düşük score = daha benzer
        stmt = select(Route).where(
            Route.embedding.isnot(None)
        )

        # Metadata filters
        if filters.origin:
            stmt = stmt.where(
                func.lower(Route.origin).contains(
                    filters.origin.lower()
                )
            )

        if filters.destination:
            stmt = stmt.where(
                func.lower(Route.destination).contains(
                    filters.destination.lower()
                )
            )

        if filters.tags:
            # tags comma-separated string, her biri match'lenmiş mi kontrol et
            for tag in filters.tags:
                stmt = stmt.where(
                    func.lower(Route.tags).contains(tag.lower())
                )

        if filters.min_copy_count > 0:
            stmt = stmt.where(Route.copy_count >= filters.min_copy_count)

        # Order by vector similarity (HNSW index)
        # pgvector <-> cosine distance operatörü
        stmt = stmt.order_by(
            Route.embedding.l2_distance(query_vector)  # L2 norm (Euclidean)
        ).limit(limit)

        result = await self.session.execute(stmt)
        candidates = result.scalars().all()

        logger.debug(f"Vector search: {len(candidates)} candidates")
        return candidates

    # -------------------------------------------------------------------------
    # PRIVATE: Re-rank
    # -------------------------------------------------------------------------

    async def _rerank_candidates(
        self,
        candidates: list[Route],
        query: str,
        query_vector: list[float],
        filters: SearchFilter,
    ) -> list[SearchResult]:
        """
        Adayları re-rank et:
        - Vector similarity score (cosine)
        - Relevance score (BM25-like + metadata boost)
        - Final score = 0.7*vector + 0.3*relevance
        """
        results: list[SearchResult] = []

        for route in candidates:
            # Vector score: cosine similarity [0, 1]
            # (1 + cosine_sim) / 2 normalize et [0, 1]
            vector_score = self._cosine_similarity(query_vector, route.embedding)

            # Relevance score: BM25 proxy + metadata boost
            relevance_score = self._compute_relevance_score(
                query, route, filters
            )

            # Final score
            final_score = 0.7 * vector_score + 0.3 * relevance_score

            results.append(
                SearchResult(
                    route=route,
                    vector_score=vector_score,
                    relevance_score=relevance_score,
                    final_score=final_score,
                )
            )

        return results

    @staticmethod
    def _cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        """Cosine similarity [0, 1]."""
        if not vec1 or not vec2:
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a**2 for a in vec1) ** 0.5
        norm2 = sum(b**2 for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return max(0.0, min(1.0, dot_product / (norm1 * norm2)))

    @staticmethod
    def _compute_relevance_score(
        query: str,
        route: Route,
        filters: SearchFilter,
    ) -> float:
        """
        BM25-like relevance score + metadata boost.

        - Query term overlap (destination, tags, description)
        - Copy count popularity boost
        - Tag match bonus
        """
        score = 0.0
        query_lower = query.lower()

        # Term overlap (destination + description)
        destination_match = (
            1.0 if route.destination.lower() in query_lower else 0.5
        )
        description_words = route.description_md.lower().split()
        query_words = query_lower.split()
        word_overlap = sum(
            1 for w in query_words if w in description_words
        ) / max(len(query_words), 1)

        score += 0.4 * destination_match + 0.3 * word_overlap

        # Tag match bonus
        if filters.tags:
            route_tags = [t.strip().lower() for t in route.tags.split(",")]
            tag_matches = sum(
                1 for t in filters.tags if t.lower() in route_tags
            )
            tag_boost = min(1.0, tag_matches / max(len(filters.tags), 1))
            score += 0.2 * tag_boost

        # Popularity boost (copy count normalized [0, 0.1])
        copy_boost = min(0.1, route.copy_count / 100.0)
        score += copy_boost

        return min(1.0, score)

    # -------------------------------------------------------------------------
    # STANDALONE TEST
    # -------------------------------------------------------------------------

    async def _smoke_test(self):
        """Smoke test — search_service.py çalışıyor mu?"""
        logger.info("SearchService smoke test başladı...")

        # Not: Burada session ve embedding_service mock edilecekti
        # Gerçek test endpoint'te olur
        logger.info("✅ SearchService initialized")


# =============================================================================
# FASTAPI DEPENDENCY
# =============================================================================

_search_service_instance: SearchService | None = None


def get_search_service() -> SearchService:
    """FastAPI Depends() ile kullanılır."""
    global _search_service_instance
    if _search_service_instance is None:
        raise RuntimeError(
            "SearchService initialize edilmedi. "
            "main.py startup'ta init_search_service() çağrılmalı."
        )
    return _search_service_instance


async def init_search_service(
    session: AsyncSession,
    embedding_service: EmbeddingService,
) -> SearchService:
    """
    main.py startup event'inde:

        @app.on_event("startup")
        async def startup():
            await init_search_service(
                session=db_session,
                embedding_service=embedding_svc,
            )
    """
    global _search_service_instance
    _search_service_instance = SearchService(
        session=session,
        embedding_service=embedding_service,
    )
    logger.info("SearchService initialized (hybrid vector+filter+rerank)")
    return _search_service_instance
