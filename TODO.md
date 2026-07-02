# Camino de Cambio — TODO

## Pending (needs WhatsApp / computer use — currently locked by another session)
- [ ] **Message Sol** (comms) with the summary of changes + ask her to re-check the page already sent to her.
- [ ] **Mariano's photos:** review Mariano's message in the group chat → open Mariano's chat → download the photos he shared → add them to the correct year/section of the chronology (confirm placement with Jeremy before publishing).
- [ ] **Article links on photos (from Amor/Victoria):** she added article URLs in WhatsApp for the photos that are press/news coverage. Make any photo that has an associated article **clickable → opens that article's web page** (e.g. a "Ver nota →" affordance / linked image). Known example already in the doc: 2024 Cumbre del Agua → Cultural Survival article. Add support in `tools/content_full.py` (optional `link` per photo) + render in `tools/generate_b.py`; wire Amor's WhatsApp URLs once retrieved.

## Content gaps
- [ ] **Cumbre del Agua (2024):** 2 referenced photos not found on disk (`IMG_9906` — Tres Pozos agreement; `07d1d7a0…` — summit support request). Section currently shows text-only. Get them from Drive.

## Scheduled
- [ ] **2026 section** — add in January (removed for now).

## Done
- [x] Format **B** chosen and built (year selector + editorial chapters).
- [x] Full content rebuild from the doc's milestones (26 sections, all years 2020–2025).
- [x] Bilingual ES/EN; per-photo captions; inline videos (Sausalito, Santa Ana).
- [x] Brand palette; removed the standalone map + link; removed per-section mini-maps.
- [x] Carousel: whole photos (no crop/cutoff), captions below, manual (no auto-rotate).
- [x] Deploy via GitHub Actions (legacy Pages build was hanging).
