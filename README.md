# Camino de Cambio — cronología (preview)

Interactive, **bilingual (ES/EN)** preview of Fundación Puna's history ("Camino de Cambio").
Format **B**: a year selector (2020–2026) with editorial chapters — each community/milestone
has its narrative, an **auto-running captioned photo carousel**, its **video** (where it exists),
and a **mini locator map** of the place. Content follows the source cronología doc, milestone by
milestone.

> ⚠️ Standalone preview / decision aid. **Not** connected to punafoundation.org.

## Structure
- `index.html` — the site (static; brand palette; Leaflet locator maps + OSM tiles)
- `assets/` — web-optimized photos + videos
- `tools/content_full.py` — milestone content (ES/EN, photos, captions, locations) → writes `tools/years.json`
- `tools/years.json` — the data
- `tools/generate_b.py` — renders `index.html` from `years.json`

Rebuild:  `python3 tools/content_full.py && python3 tools/generate_b.py`
