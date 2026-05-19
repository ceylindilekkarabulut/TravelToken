# Throne Travel

**AI destekli seyahat planlama, Solana blockchain escrow ve topluluk sponsorluğu**

---

## 🎯 Vizyon

Gezginlerin hayallerindeki seyahatleri kitle fonlaması ile gerçekleştirmelerini sağlamak, aynı zamanda AI destekli seyahat planlama almalarını sunmak. Topluluk sponsorları Solana escrow aracılığıyla fon sağlar; AI ajanları rotaları optimize eder, en iyi fırsatları bulur ve bütçeyi yönetir—her şey şeffaf ve merkezi olmayan şekilde.

---

## ✅ MVP Durumu: FAZ 2 TAMAMLANDI

### Geliştirilen Temel Özellikler
- ✅ **FastAPI Backend** gerçek zamanlı SSE streaming ile
- ✅ **3 AI Ajanı** (Rota Planlayıcı, Fırsat Avcısı, Bütçe Optimizatörü)
- ✅ **Hibrit Vektör Arama** pgvector ile (semantik + anahtar kelime)
- ✅ **Ajan Çalıştırma Kaydı** (zamanlama, I/O takibi)
- ✅ **Solana Akıllı Kontratı** (4 talimat + olay yayınlama)
- ✅ **PostgreSQL Veritabanı** (6 tablo + migrasyonlar)
- ✅ **Next.js Frontend** (responsive UI + API entegrasyonu)
- ✅ **Gerçek Zamanlı Hedef Oluşturma** streaming yanıtları ile

---

## 🚀 Hızlı Başlangıç

### Ön Koşullar
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+

### 1. Hizmetleri Başlat
```bash
docker-compose up -d
```

### 2. Backend (Terminal 1)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 4. Demo
`http://localhost:3000` ziyaret et → "✨ AI Planlama Başlat" tıkla → Formu doldur → Gerçek zamanlı AI analizini izle

---

## 📊 Mimari

```
Frontend (Next.js)
    ↓ HTTP/SSE
Backend (FastAPI)
    ├─ Rota Ajanı (Google Maps + LLM)
    ├─ Fırsat Avcısı (Amadeus API + LLM)
    └─ Bütçe Ajanı (Maliyet hesaplama + LLM ipuçları)
    ↓
Veritabanı (PostgreSQL + pgvector)
    └─ SeyahatHedefleri, Sponsorluklar, AjanKayıtları, Rotalar

Akıllı Kontrat (Solana)
    ├─ initialize_goal (PDA oluşturma)
    ├─ sponsor (fon transferi)
    ├─ release_funds (escrow dağıtımı)
    └─ refund_sponsor (geri ödeme)
```

---

## 🤖 AI Ajan Akışı

1. **Rota Ajanı**: Seyahat rotasını Google Maps + LLM içgörüleri ile analiz eder
2. **Fırsat Avcısı**: En iyi uçuşları (Amadeus) + otelleri bulur, değerlendirme sağlar
3. **Bütçe Ajanı**: Toplam maliyeti hesaplar, para tasarrufu ipuçları üretir
4. **Son Rapor**: Tüm ajan çıktılarının Markdown derlemesi

→ **Hepsi SSE aracılığıyla gerçek zamanlı frontend'e aktarılır**

---

## ⛓️ Solana Entegrasyonu

### Akıllı Kontrat Özellikleri
- **Yetkilendirmeye dayalı onay** güvenli fon serbest bırakma için
- **PDA tabanlı escrow** (hiçbir vedi riski yok)
- **Olay yayınlama** (HedefFonlandı, HedefSerbest)
- **Çoklu sponsor desteği** (hedef başına birden fazla katkı)

### İş Akışı
```
1. Hedefi Başlat (backend → blockchain)
2. Sponsor (topluluk üyeleri fon sağlar)
3. Onayla (yetkilendirme release_funds'ı tetikler)
4. Serbest Bırak (fonlar → gezgin cüzdanı)
```

---

## 🔍 Temel Teknik Özellikler

| Özellik | Teknoloji | Detaylar |
|---------|-----------|----------|
| **Vektör Arama** | pgvector + OpenAI | 1536-boyutlu embeddings, HNSW indexing |
| **Ajan Kaydı** | SQLAlchemy | Her ajan için çalıştırma zamanı + I/O |
| **Gerçek Zamanlı Güncellemeler** | SSE | Canlı ajan ilerleme streaming |
| **API Çerçevesi** | FastAPI | Otomatik Swagger dokümentasyonu |
| **Akıllı Kontrat** | Anchor + Rust | 4 talimat, 2 olay, PDA'lar |
| **Veritabanı** | PostgreSQL 16 | Async SQLAlchemy + Alembic migrasyonları |
| **Frontend** | Next.js 15 | TypeScript, React Query, Tailwind |

---

## 📁 Proje Yapısı

```
TravelToken/
├── backend/
│   ├── app/
│   │   ├── agents/        # 3 AI ajanı + orkestrasyoncu
│   │   ├── api/routes/    # 8 uç nokta
│   │   ├── models/        # SQLAlchemy + Pydantic
│   │   ├── services/      # Harici API'ler
│   │   └── main.py
│   └── alembic/           # Migrasyonlar
├── contracts/
│   └── programs/travel_escrow/src/
│       ├── instructions/  # 4 talimat
│       ├── state.rs       # PDA'lar
│       └── lib.rs         # Program
├── frontend/
│   ├── src/app/           # Next.js sayfaları
│   └── src/components/    # React bileşenleri
├── idl/
│   └── travel_escrow.json # Akıllı kontrat IDL'i
└── docker-compose.yml
```

---

## 🎬 API Uç Noktaları

| Yöntem | Uç Nokta | Amaç |
|--------|----------|------|
| POST | `/api/goals/create` | Hedef oluştur + AI analizini stream et |
| GET | `/api/goals/{id}` | Hedef getir |
| GET | `/api/goals/list/by-wallet` | Kullanıcı hedeflerini listele |
| POST | `/api/sponsorships/create` | Sponsor ekle |
| GET | `/api/routes/search` | Hibrit rota arama |
| POST | `/api/routes/{id}/copy` | Rotayı kopyala |
| WS | `/ws/notifications/{wallet}` | Gerçek zamanlı güncellemeler |
| POST | `/api/agents/approve-purchase` | Solana'da fonları serbest bırak |

---

## 💡 İnovasyon Noktaları

1. **Ajanlar + Blockchain**: LLM ajanları Solana escrow ile orkestrasyonu
2. **Hibrit Arama**: Vektör benzerliği (embeddings) + anahtar kelime eşleştirmesi
3. **Gerçek Zamanlı Streaming**: Kullanıcılar AI'nin "düşünüşünü" SSE aracılığıyla izler
4. **Güvensiz Escrow**: PDA'lar aracı riskini ortadan kaldırır
5. **Modüler Tasarım**: Ajanlar, hizmetler, API'nin açık ayrımı

---

## 👥 Takım

- **Şeyma**: Backend (FastAPI, ajanlar, API, Solana)
- **Ceylin**: Altyapı (DB, migrasyonlar, akıllı kontrat)
- **Irmak**: Frontend (Next.js, UI, UX)

---

## 📚 Belgeler

- **Görev Dağılımı & İlerleme**: [TASK_DISTRIBUTION.md](TASK_DISTRIBUTION.md) dosyasına bak
- **API Dokümentasyonu**: `http://localhost:8000/docs` (otomatik oluşturulur)
- **Akıllı Kontrat IDL'i**: `idl/travel_escrow.json`

---

## 🔗 Bağlantılar

- **Solana Programı**: `programs/travel_escrow/src/`
- **Devnet Explorer**: https://explorer.solana.com/?cluster=devnet
- **GitHub**: https://github.com/ceylindilekkarabulut/TravelToken

---

**Hackathon'26 için geliştirildi • Faz 2 Tamamlandı • MVP Hazır**
