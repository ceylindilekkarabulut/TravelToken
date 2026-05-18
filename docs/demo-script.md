# Demo Script (5 dakika)

## Dakika 0-1: Hook

"Hayal ettiğin seyahati planlamak artık saniyeler alıyor. Throne Travel'da AI ajanlar sizin için uçuş, otel ve bütçeyi otomatik analiz ediyor — ve topluluk sponsorluğuyla gerçeğe dönüşüyor."

## Dakika 1-2: Goal Oluşturma

1. `/create` sayfasına git
2. Istanbul → Tokyo, Temmuz 2026, $2000 bütçe gir
3. "Start AI Planning" tıkla
4. **AgentStreamPanel**'i göster: Route Agent, Deal Hunter, Budget Agent sırayla canlı çalışıyor

## Dakika 2-3: Final Report

1. Goal detail sayfasına otomatik yönlenme
2. Final raporun markdown olarak render edildiğini göster
3. Fiyat geçmişi grafiğini göster (buy signal badge)

## Dakika 3-4: Sponsorship + Blockchain

1. "Sponsor" butonuna tıkla
2. Phantom wallet pop-up → 0.1 SOL gönder
3. Solana Explorer'da işlemi göster
4. Progress bar'ın güncellenmesini göster

## Dakika 4-5: Social Routes + Q&A

1. `/routes/search` → "Tokyo" ara
2. Route kopyalama göster
3. Değer önerisi: "Tek platform, AI + Web3 + sosyal seyahat"

## Pre-Demo Checklist

- [ ] Demo wallet'ta min 1 SOL var
- [ ] Backend çalışıyor (`uvicorn app.main:app`)
- [ ] Docker containers up (`docker compose up -d`)
- [ ] Phantom extension yüklü, auto-approve KAPALI
- [ ] Seed data yüklenmiş (`python scripts/seed_routes.py`)
- [ ] Mapbox token `.env.local`'da var
