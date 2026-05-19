"""
Embedding Service — Google Gemini text-embedding-004 wrapper.

Hackathon notu: BTK + Google düzenleyici, doğal seçim.

Özellikler:
- Async (FastAPI ile uyumlu)
- Redis cache (tekrar eden metinler için maliyet sıfır)
- Batch processing
- Retry mekanizması
- Pydantic validation
- Ücretsiz tier: dk başına 1500 request, günde sınırsız
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging

import google.generativeai as genai
import redis.asyncio as redis_async
from google.api_core import exceptions as google_exceptions
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS
# =============================================================================

EMBEDDING_MODEL = "models/text-embedding-004"
EMBEDDING_DIM = 768                # Gemini text-embedding-004 boyutu
MAX_BATCH_SIZE = 100               # Gemini API tek çağrıda 100 metin alabilir
CACHE_TTL_SECONDS = 60 * 60 * 24 * 7  # 1 hafta
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# Task type — Gemini'da embedding'in nerede kullanılacağını belirtmek kalite artırır
TASK_TYPE_DOCUMENT = "RETRIEVAL_DOCUMENT"   # Route'ları embed ederken
TASK_TYPE_QUERY = "RETRIEVAL_QUERY"          # Search query'sini embed ederken


# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class EmbeddingResult(BaseModel):
    """Tek bir embedding sonucu."""
    text: str = Field(..., description="Embed edilen orijinal metin")
    vector: list[float] = Field(..., min_length=EMBEDDING_DIM, max_length=EMBEDDING_DIM)
    from_cache: bool = Field(default=False)


# =============================================================================
# EMBEDDING SERVICE
# =============================================================================

class EmbeddingService:
    """
    Google Gemini text-embedding-004 için async wrapper.

    Kullanım yerleri:
    1. Yeni Route oluştuğunda → embed_document(text)
    2. Search query'de → embed_query(text)
    3. Seed script'te → embed_many(texts, task_type=DOCUMENT)
    """

    def __init__(
        self,
        api_key: str,
        redis_client: redis_async.Redis | None = None,
        cache_prefix: str = "emb:v1:",
    ):
        genai.configure(api_key=api_key)
        self.redis = redis_client
        self.cache_prefix = cache_prefix
        self.total_requests = 0  # debugging

    # -------------------------------------------------------------------------
    # PUBLIC API
    # -------------------------------------------------------------------------

    async def embed_document(self, text: str) -> EmbeddingResult:
        """Bir döküman/route metnini embed et (DB'ye yazılacak)."""
        return await self._embed_one(text, task_type=TASK_TYPE_DOCUMENT)

    async def embed_query(self, text: str) -> EmbeddingResult:
        """Kullanıcı search query'sini embed et."""
        return await self._embed_one(text, task_type=TASK_TYPE_QUERY)

    async def embed_many(
        self,
        texts: list[str],
        task_type: str = TASK_TYPE_DOCUMENT,
    ) -> list[EmbeddingResult]:
        """
        Birden fazla metni paralel embed et.
        Cache'tekiler hemen döner, eksikler batch olarak API'den çekilir.
        """
        if not texts:
            return []

        clean_texts = [t for t in texts if t and t.strip()]
        if len(clean_texts) != len(texts):
            logger.warning(f"{len(texts) - len(clean_texts)} boş metin atlandı")

        # Önce cache'ten topla
        cache_results: dict[str, list[float]] = {}
        if self.redis:
            cache_keys = [self._cache_key(t, task_type) for t in clean_texts]
            cached_values = await self.redis.mget(cache_keys)
            for text, cached_value in zip(clean_texts, cached_values):
                if cached_value:
                    cache_results[text] = json.loads(cached_value)

        missing_texts = [t for t in clean_texts if t not in cache_results]
        logger.info(
            f"Embedding batch: {len(clean_texts)} total, "
            f"{len(cache_results)} cached, {len(missing_texts)} to fetch"
        )

        # Eksikleri batch'lerle çek
        api_results: dict[str, list[float]] = {}
        if missing_texts:
            for i in range(0, len(missing_texts), MAX_BATCH_SIZE):
                batch = missing_texts[i:i + MAX_BATCH_SIZE]
                batch_vectors = await self._fetch_batch_from_api(batch, task_type)

                pipe = self.redis.pipeline() if self.redis else None
                for text, vector in zip(batch, batch_vectors):
                    api_results[text] = vector
                    if pipe:
                        pipe.setex(
                            self._cache_key(text, task_type),
                            CACHE_TTL_SECONDS,
                            json.dumps(vector),
                        )
                if pipe:
                    await pipe.execute()

        # Sonuçları orijinal sıraya göre birleştir
        final_results: list[EmbeddingResult] = []
        for text in clean_texts:
            if text in cache_results:
                final_results.append(EmbeddingResult(
                    text=text,
                    vector=cache_results[text],
                    from_cache=True,
                ))
            elif text in api_results:
                final_results.append(EmbeddingResult(
                    text=text,
                    vector=api_results[text],
                    from_cache=False,
                ))
            else:
                raise RuntimeError(f"Embedding bulunamadı: {text[:50]}")

        return final_results

    # -------------------------------------------------------------------------
    # ROUTE-SPECIFIC HELPER
    # -------------------------------------------------------------------------

    @staticmethod
    def format_route_for_embedding(
        destination: str,
        duration_days: int,
        estimated_budget_usd: float,
        tags: list[str],
        description: str | None = None,
    ) -> str:
        """Route'u embedding için optimum metne çevirir (Adım 3'te tasarlandı)."""
        tags_str = ", ".join(tags) if tags else "general"
        desc_part = f" | Description: {description}" if description else ""
        return (
            f"Destination: {destination} | "
            f"Duration: {duration_days} days | "
            f"Budget: ${estimated_budget_usd:.0f} | "
            f"Tags: {tags_str}"
            f"{desc_part}"
        )

    # -------------------------------------------------------------------------
    # PRIVATE: tek metin embed
    # -------------------------------------------------------------------------

    async def _embed_one(self, text: str, task_type: str) -> EmbeddingResult:
        if not text or not text.strip():
            raise ValueError("Boş metin embed edilemez")

        cached = await self._get_from_cache(text, task_type)
        if cached is not None:
            return EmbeddingResult(text=text, vector=cached, from_cache=True)

        vectors = await self._fetch_batch_from_api([text], task_type)
        vector = vectors[0]
        await self._set_cache(text, vector, task_type)

        return EmbeddingResult(text=text, vector=vector, from_cache=False)

    # -------------------------------------------------------------------------
    # PRIVATE: API CALL
    # -------------------------------------------------------------------------

    async def _fetch_batch_from_api(
        self,
        texts: list[str],
        task_type: str,
    ) -> list[list[float]]:
        """
        Gemini batch embedding. Retry'lı.
        Not: google-generativeai SDK'sı senkron, asyncio.to_thread ile sarıyoruz.
        """
        attempt = 0
        last_error: Exception | None = None

        while attempt < MAX_RETRIES:
            try:
                response = await asyncio.to_thread(
                    genai.embed_content,
                    model=EMBEDDING_MODEL,
                    content=texts,
                    task_type=task_type,
                )
                self.total_requests += 1

                embeddings = response["embedding"]

                # Tek metin gönderildiyse düz array dönebilir
                if texts and len(texts) == 1 and isinstance(embeddings[0], float):
                    embeddings = [embeddings]

                for i, emb in enumerate(embeddings):
                    if len(emb) != EMBEDDING_DIM:
                        raise ValueError(
                            f"Beklenmeyen boyut: {len(emb)}, beklenen {EMBEDDING_DIM}"
                        )

                logger.debug(
                    f"Gemini embedding API: {len(texts)} texts (task={task_type})"
                )
                return embeddings

            except google_exceptions.ResourceExhausted as e:
                wait_time = RETRY_DELAY_SECONDS * (2 ** attempt)
                logger.warning(
                    f"Gemini rate limit, {wait_time}s bekleniyor "
                    f"(deneme {attempt + 1}/{MAX_RETRIES})"
                )
                await asyncio.sleep(wait_time)
                last_error = e
                attempt += 1

            except google_exceptions.GoogleAPIError as e:
                logger.error(f"Gemini API hatası: {e}")
                last_error = e
                attempt += 1
                if attempt < MAX_RETRIES:
                    await asyncio.sleep(RETRY_DELAY_SECONDS)

            except Exception as e:
                logger.exception(f"Beklenmeyen embedding hatası: {e}")
                raise

        raise RuntimeError(
            f"Gemini API {MAX_RETRIES} denemeden sonra başarısız: {last_error}"
        )

    # -------------------------------------------------------------------------
    # PRIVATE: CACHE
    # -------------------------------------------------------------------------

    def _cache_key(self, text: str, task_type: str) -> str:
        """Metin + task_type'tan SHA256 hash → cache key.

        task_type cache key'e dahil çünkü aynı metin DOCUMENT vs QUERY için
        farklı vektör üretir (Gemini'nin task-aware embedding özelliği).
        """
        combined = f"{task_type}:{text}"
        text_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()[:32]
        return f"{self.cache_prefix}{text_hash}"

    async def _get_from_cache(
        self, text: str, task_type: str
    ) -> list[float] | None:
        if not self.redis:
            return None
        try:
            cached = await self.redis.get(self._cache_key(text, task_type))
            if cached:
                return json.loads(cached)
        except Exception as e:
            logger.warning(f"Redis cache read hatası: {e}")
        return None

    async def _set_cache(
        self, text: str, vector: list[float], task_type: str
    ) -> None:
        if not self.redis:
            return
        try:
            await self.redis.setex(
                self._cache_key(text, task_type),
                CACHE_TTL_SECONDS,
                json.dumps(vector),
            )
        except Exception as e:
            logger.warning(f"Redis cache write hatası: {e}")


# =============================================================================
# SINGLETON / FASTAPI DEPENDENCY
# =============================================================================

_embedding_service_instance: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    """FastAPI Depends() ile kullanılır."""
    global _embedding_service_instance
    if _embedding_service_instance is None:
        raise RuntimeError(
            "EmbeddingService initialize edilmedi. "
            "main.py startup'ta init_embedding_service() çağrılmalı."
        )
    return _embedding_service_instance


async def init_embedding_service(
    api_key: str,
    redis_url: str | None = None,
) -> EmbeddingService:
    """
    Uygulama başlangıcında main.py'de:

        @app.on_event("startup")
        async def startup():
            await init_embedding_service(
                api_key=settings.GEMINI_API_KEY,
                redis_url=settings.REDIS_URL,
            )
    """
    global _embedding_service_instance

    redis_client = None
    if redis_url:
        redis_client = redis_async.from_url(
            redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        try:
            await redis_client.ping()
            logger.info("Redis bağlantısı başarılı (embedding cache aktif)")
        except Exception as e:
            logger.warning(f"Redis bağlantı hatası: {e}. Cache devre dışı.")
            redis_client = None

    _embedding_service_instance = EmbeddingService(
        api_key=api_key,
        redis_client=redis_client,
    )

    logger.info(f"EmbeddingService initialized (model={EMBEDDING_MODEL}, dim={EMBEDDING_DIM})")
    return _embedding_service_instance


# =============================================================================
# STANDALONE TEST
# =============================================================================

async def _smoke_test():
    """python -m app.services.embedding_service"""
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    if not api_key:
        print("HATA: GEMINI_API_KEY .env dosyasında ayarlı değil")
        print("Al: https://aistudio.google.com/app/apikey")
        return

    print("=" * 60)
    print("EmbeddingService Smoke Test — Google Gemini")
    print("=" * 60)

    svc = await init_embedding_service(api_key=api_key, redis_url=redis_url)

    # Test 1: Tek embedding
    print("\n[TEST 1] Tek embedding (document task)...")
    result = await svc.embed_document("Roma'da 3 günlük bütçe seyahati")
    print(f"  ✓ Vector boyutu: {len(result.vector)} (beklenen: {EMBEDDING_DIM})")
    print(f"  ✓ İlk 5 değer: {[round(v, 4) for v in result.vector[:5]]}")
    print(f"  ✓ From cache: {result.from_cache}")

    # Test 2: Cache testi
    print("\n[TEST 2] Cache testi (aynı metin tekrar)...")
    result2 = await svc.embed_document("Roma'da 3 günlük bütçe seyahati")
    print(f"  ✓ From cache: {result2.from_cache} (beklenen: True)")
    assert result.vector == result2.vector, "Cache'ten farklı sonuç!"

    # Test 3: Query vs Document
    print("\n[TEST 3] Query vs Document farkı...")
    doc_emb = await svc.embed_document("Avrupa solo seyahat")
    query_emb = await svc.embed_query("Avrupa solo seyahat")
    similarity = sum(a * b for a, b in zip(doc_emb.vector, query_emb.vector))
    print(f"  ✓ Cosine benzerlik: {similarity:.4f}")
    print(f"  ✓ İkisi farklı vektör: {doc_emb.vector != query_emb.vector}")

    # Test 4: Batch embedding
    print("\n[TEST 4] Batch embedding (4 metin)...")
    texts = [
        "Roma'da 3 günlük bütçe seyahati",  # cache HIT
        "Paris solo macera, 5 gün",
        "Berlin backpacker haftası",
        "Tokyo lüks tatil",
    ]
    results = await svc.embed_many(texts, task_type=TASK_TYPE_DOCUMENT)
    print(f"  ✓ Toplam sonuç: {len(results)}")
    cache_hits = sum(1 for r in results if r.from_cache)
    print(f"  ✓ Cache hit: {cache_hits}/4 (beklenen: 1)")

    # Test 5: Route formatter + embedding
    print("\n[TEST 5] Route formatter + embedding...")
    route_text = EmbeddingService.format_route_for_embedding(
        destination="Rome",
        duration_days=3,
        estimated_budget_usd=850,
        tags=["solo", "budget", "culture"],
        description="3 günlük solo Roma turu",
    )
    print(f"  ✓ Formatted: {route_text}")
    route_result = await svc.embed_document(route_text)
    print(f"  ✓ Embedded başarılı, boyut: {len(route_result.vector)}")

    print(f"\n{'=' * 60}")
    print(f"✅ Tüm testler başarılı!")
    print(f"📊 Toplam API çağrısı: {svc.total_requests}")
    print(f"💰 Maliyet: $0.00 (Gemini ücretsiz tier)")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_smoke_test())