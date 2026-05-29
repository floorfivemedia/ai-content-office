---
description: Pipeline completo de AI Content Office. Investiga IA, escribe guiones virales, archiva en Notion y notifica por Telegram. Sin costo de API — corre dentro de Claude Code.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# AI Content Office — Pipeline Completo

Sos el orquestador. Ejecutás los 6 pasos en orden, sin saltarte ninguno.

## Variables de contexto

- **Creador**: venezolano, 31 años, en Argentina. Audiencia: hispanohablante LATAM 18-35.
- **Tono**: disruptivo, directo, alta energía. Sin violencia ni groserías.
- **Plataformas**: TikTok, Instagram Reels, YouTube Shorts.
- **Working dir**: `ai-content-office/`
- **Argumento opcional**: `$ARGUMENTS` — si contiene "MANUAL" o `--now`, marcar trigger como MANUAL; default SCHEDULED.

## Eficiencia de tokens (IMPORTANTE)

- **No leas** los `prompts/*.md` ni `skills/*.md`. Todo lo esencial está acá inline.
- WebFetch sólo donde se indica. Snippets de WebSearch alcanzan para la mayoría.
- No repitas en contexto JSONs ya guardados; trabajá con lo mínimo necesario.

## Setup inicial (siempre)

```bash
cd "ai-content-office"
mkdir -p output/trends output/news output/scripts output/logs
TS=$(date +%Y%m%d_%H%M%S)
```

Generá un número de ciclo leyendo (e incrementando) `output/logs/cycle_counter.txt`.

## PASO 0 — Trend Scout

Usá **WebSearch** (4 queries):
- "AI trending TikTok this week"
- "inteligencia artificial viral [mes actual]"
- "Reddit r/artificial top week"
- "ChatGPT Claude trending now"

WebFetch sólo 1 resultado clave si hace falta contexto.
Producí JSON con 5-8 trends ordenados por score. Guardá en `output/trends/trends_${TS}.json`.

## PASO 1 — Buscador (15 noticias en 3 bloques)

**Bloque A — 5 noticias IA general** (impacto social, trabajo, debates). WebSearch:
- "AI artificial intelligence news [fecha hoy]"
- "AI impact jobs society latest"
- "inteligencia artificial noticias últimas 48 horas"

**Bloque B — 4 nuevos lanzamientos**. WebSearch:
- "new AI model released this week"
- "AI tool launch latest"
- "LLM benchmark new release"

**Bloque C — 6 noticias Claude/Anthropic** (PRIORIDAD).
SIEMPRE empezar por **WebFetch** a `https://www.anthropic.com/news`. Luego WebSearch:
- "Claude Anthropic announcement [fecha]"
- "Claude Code update [fecha]"
- "claude.ai new model"

Si menos de 6 en 48h, ampliar a 96h.

**WebFetch SOLO a las top 5 noticias** (las de mayor impacto, priorizando bloque C) para tener datos reales. El resto, usar el snippet de WebSearch. Nunca inventar cifras ni URLs.

Producí JSON con `bloque_a`, `bloque_b`, `bloque_c`, `todas` (15 total). Guardá en `output/news/raw_news_${TS}.json`.

## PASO 2 — Clasificador

Usá trends (paso 0) + noticias (paso 1). Scoring 0-100 (5 dimensiones de 0-20). Bloque C: score ≥60 pasa igual; resto ≥70.

**Devolvé máximo 8 noticias top** (calidad > cantidad). Guardá en `output/news/classified_${TS}.json`.

## PASO 3 — Guionista (CRÍTICO — máxima calidad)

Para CADA noticia clasificada (máx 8), creá:
- **Modo 1 — Viral Corto (30-40s)**: hook en 3s + dato + giro + CTA
- **Modo 2 — Viral Profundo (60-90s)**: hook + tensión + pregunta abierta + desarrollo + CTA cierre

Reglas:
- El hook **debe** parar el scroll en 3-5 seg. Si no convence, reescribilo antes de seguir.
- Lenguaje venezolano natural, comprensible en toda LATAM. Sin "Hola", sin presentaciones.
- **Oraciones claras y cortas**: el mismo guion se graba en vivo Y se usa en HeyGen. Frases simples = funciona en ambos. No hace falta versión aparte.

Guardá en `output/scripts/scripts_master_${TS}.json`:
```json
{
  "total_guiones": N,
  "guiones": [
    {
      "id": "G001", "noticia_id": "...", "bloque": "C", "noticia_titulo": "...",
      "noticia_url": "...", "score_viral": N, "modo_recomendado": "1|2|ambos",
      "modo_1": {"hook": "...", "guion_completo": "...", "duracion_seg": N, "tipo_hook": "..."},
      "modo_2": {"hook": "...", "guion_completo": "...", "duracion_seg": N, "tipo_hook": "..."},
      "notas_produccion": "..."
    }
  ]
}
```

## PASO 4 — Metadata por plataforma

Para CADA guion, un solo bloque de metadata. **Captions cortos — máximo 40 palabras cada uno**:
- TikTok: caption ≤40 palabras + 15-20 hashtags
- Instagram: caption ≤40 palabras + 20-25 hashtags
- YouTube Shorts: caption ≤40 palabras + 3-5 hashtags + 3 títulos (beneficio/curiosidad/número)
- Thumbnail: specs cortas con hex colors

Guardá en `output/scripts/metadata_${TS}.json` con `metadata[]`. **Cada item lleva `guion_id`** apuntando al `id` del guion (el archivador lo usa como pivote):
```json
{"guion_id":"G001","tiktok":{"caption":"...","hashtags":[...]},"instagram":{...},"youtube":{"caption":"...","hashtags":[...],"titulos":{"beneficio":"...","curiosidad":"...","numero":"..."}},"thumbnail":{...}}
```

## PASO 5 — Archivador a Notion

Armá `output/scripts/full_content_${TS}.json` combinando 2 outputs:
```json
{
  "guiones":  [...desde scripts_master],
  "metadata": [...desde metadata]
}
```

Corré:
```bash
python agents/agent_06_archivador.py output/scripts/full_content_${TS}.json
```

Crea la subcarpeta `GUIONES [DÍA] [DD-MM]` dentro de `AI Content Office` y **una card por guion** (Modo 1 + Modo 2 + metadata 3 plataformas + thumbnail + checklist). Imprime el link y un JSON en `output/logs/notion_result_*.json`.

## PASO 6 — Summary + Notificador Telegram

Armá `output/logs/pipeline_summary_${TS}.json`:
```json
{
  "ciclo": N,
  "trigger": "MANUAL|SCHEDULED",
  "fecha": "YYYY-MM-DD HH:MM",
  "duracion_min": N,
  "bloques": {"A": 5, "B": 4, "C": 6},
  "total_guiones": N,
  "cards_ok": N,
  "subcarpeta": "GUIONES JUEVES 29-05",
  "link_subcarpeta": "https://notion.so/...",
  "top1": {"titulo": "...", "score": 88},
  "top3": [
    {"titulo": "...", "bloque": "C", "score": 88, "hook_modo1": "...", "hook_modo2": "..."}
  ],
  "errores": []
}
```

Corré:
```bash
python agents/agent_07_notificador.py output/logs/pipeline_summary_${TS}.json
```

## Reporte final al usuario

```
✅ Ciclo #N completado en M min
   📰 15 noticias (A=5, B=4, C=6)
   📋 N guiones × 2 modos = N cards
   ✅ N cards en Notion → [link subcarpeta]
   📱 2 mensajes Telegram enviados
```

## Reglas operativas

- **Nunca inventes URLs ni datos**. WebFetch antes de citar cifras.
- **Si un paso falla**, loggeá en `output/logs/error_paso_X_${TS}.log` y continuá con dict vacío.
- **El paso 6 (Telegram) SIEMPRE se ejecuta**, incluso si pasos previos fallaron.
- **Auth**: Notion y Telegram desde `.env` (los scripts Python usan `load_dotenv(override=True)`).
- **Sin LLM externo**: corre 100% dentro de Claude Code. Costo API: $0.
