---
description: Pipeline completo de AI Content Office. Investiga IA, escribe guiones virales, archiva en Notion y notifica por Telegram. Sin costo de API — corre dentro de Claude Code.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# AI Content Office — Pipeline Completo

Sos el orquestador. Ejecutás los 7 pasos en orden, sin saltarte ninguno.

## Variables de contexto

- **Creador**: venezolano, 31 años, en Argentina. Audiencia: hispanohablante LATAM 18-35.
- **Tono**: disruptivo, directo, alta energía. Sin violencia ni groserías.
- **Plataformas**: TikTok, Instagram Reels, YouTube Shorts.
- **Working dir**: `ai-content-office/`
- **Argumento opcional**: `$ARGUMENTS` — si contiene "MANUAL" o `--now`, marcar trigger como MANUAL; default SCHEDULED.

## Setup inicial (siempre)

```bash
cd "ai-content-office"
mkdir -p output/trends output/news output/scripts output/logs
TS=$(date +%Y%m%d_%H%M%S)
```

Generá un número de ciclo leyendo (e incrementando) `output/logs/cycle_counter.txt`.

## PASO 0 — Trend Scout

Lee `prompts/prompt_trend_scout.md` para el rol y formato JSON exacto.

Usá la tool **WebSearch** (nunca menos de 4 queries distintas):
- "AI trending TikTok this week"
- "inteligencia artificial viral [mes actual]"
- "Reddit r/artificial top week"
- "ChatGPT Claude trending now"

Usá **WebFetch** sobre 1-2 resultados clave si necesitás contexto.

Producí JSON con 5-8 trends ordenados por score.
Guardá en `output/trends/trends_${TS}.json` usando la tool Write.

## PASO 1 — Buscador (15 noticias en 3 bloques)

Lee `prompts/prompt_buscador.md` para criterios y JSON exacto.

**Bloque A — 5 noticias IA general** (impacto social, trabajo, debates).
WebSearch queries:
- "AI artificial intelligence news [fecha hoy]"
- "AI impact jobs society latest"
- "inteligencia artificial noticias últimas 48 horas"

**Bloque B — 4 nuevos lanzamientos**.
WebSearch queries:
- "new AI model released this week"
- "AI tool launch latest"
- "LLM benchmark new release"

**Bloque C — 6 noticias Claude/Anthropic** (PRIORIDAD).
SIEMPRE empezar por **WebFetch** a `https://www.anthropic.com/news` para extraer las últimas.
Luego WebSearch:
- "Claude Anthropic announcement [fecha]"
- "Claude Code update [fecha]"
- "Claude Cowork feature"
- "claude.ai new model"

Si menos de 6 en 48h, ampliar a 96h.

Para cada noticia, hacé **WebFetch** al menos a las top 8 para tener detalles reales (no inventar datos).

Producí JSON con `bloque_a`, `bloque_b`, `bloque_c`, `todas` (15 total).
Guardá en `output/news/raw_news_${TS}.json`.

## PASO 2 — Clasificador

Lee `prompts/prompt_clasificador.md`. Usá los trends del paso 0 y las noticias del paso 1.

Aplicá scoring 0-100 (5 dimensiones de 0-20). Regla bloque C: score ≥60 pasa igual.
Devolvé entre 8 y 12 noticias top.

Guardá en `output/news/classified_${TS}.json`.

## PASO 3 — Guionista (CRÍTICO — máxima calidad)

Lee `prompts/prompt_guionista.md`. Lee también `skills/skill-viral-hooks.md` para repasar tipos de hook.

Para CADA noticia clasificada, creá:
- **Modo 1 — Viral Corto (30-40s)**: hook en 3s + dato + giro + CTA
- **Modo 2 — Viral Profundo (60-90s)**: hook + tensión + pregunta abierta + desarrollo + CTA cierre

Regla crítica: el hook **debe** parar el scroll en 3-5 segundos. Si no convence, reescribilo antes de pasar al siguiente.

Lenguaje venezolano natural pero comprensible en toda LATAM. Sin "Hola", sin presentaciones.

Guardá en `output/scripts/scripts_master_${TS}.json` con formato:
```json
{
  "total_guiones": N,
  "guiones": [
    {
      "id": "G001", "noticia_id": "...", "bloque": "C", "noticia_titulo": "...",
      "noticia_url": "...", "score_viral": N, "modo_recomendado": "1|2|ambos",
      "modo_1": {"hook": "...", "cuerpo": "...", "cta": "...", "guion_completo": "...", "duracion_seg": N, "tipo_hook": "..."},
      "modo_2": {"hook": "...", "desarrollo_tension": "...", "pregunta_abierta": "...", "desarrollo_final": "...", "cta_cierre": "...", "guion_completo": "...", "duracion_seg": N, "tipo_hook": "..."},
      "notas_produccion": "..."
    }
  ]
}
```

## PASO 4 — Adaptador (Real vs HeyGen)

Lee `prompts/prompt_adaptador.md` y `skills/skill-heygen-scripts.md`.

Para cada guion × cada modo, generá:
- **version_real**: coloquial, con `[MOSTRAR: ...]`, `[reaccionar sorpresa]`, `[bajar voz]`
- **version_heygen**: máx 12 palabras/oración, marcadores `[PAUSA 0.5 seg]` `[PAUSA 1 seg]` `[PAUSA 2 seg]` (max 2 pausas de 2s por guion)

Guardá en `output/scripts/scripts_adapted_${TS}.json` con `adaptaciones[]`:
```json
{"id":"A001","guion_id":"G001","modo":"1","version_real":{...},"version_heygen":{...}}
```

## PASO 5 — Metadata por plataforma

Lee `prompts/prompt_metadata.md`.

Para CADA guion (un solo bloque de metadata por guion, no duplicado por formato):
- TikTok: caption 80-100 palabras + 15-20 hashtags
- Instagram: caption 120-180 palabras + 20-25 hashtags
- YouTube Shorts: caption 150-200 palabras + 3-5 hashtags + 3 títulos
- Thumbnail: specs exactas con hex colors

Guardá en `output/scripts/metadata_${TS}.json` con `metadata[]`. Importante: cada item lleva `adaptacion_id` apuntando al `id` de la adaptación Modo 1 correspondiente (el archivador lo usa como pivote).

## PASO 6 — Archivador a Notion

Armá `output/scripts/full_content_${TS}.json` combinando los 3 outputs anteriores:
```json
{
  "guiones": [...desde scripts_master],
  "adaptaciones": [...desde scripts_adapted],
  "metadata": [...desde metadata]
}
```

Corré:
```bash
python agents/agent_06_archivador.py output/scripts/full_content_${TS}.json
```

El script crea la subcarpeta `GUIONES [DÍA] [DD-MM]` dentro de `AI Content Office` en Notion y dos cards por guion (Real + HeyGen). Imprime el link de la subcarpeta y un JSON de resultado en `output/logs/notion_result_*.json`.

## PASO 7 — Summary + Notificador Telegram

Armá `output/logs/pipeline_summary_${TS}.json` con:
```json
{
  "ciclo": N,
  "trigger": "MANUAL|SCHEDULED",
  "fecha": "YYYY-MM-DD HH:MM",
  "duracion_min": N,
  "bloques": {"A": 5, "B": 4, "C": 6},
  "total_guiones": N,
  "n_modo_1": N, "n_modo_2": N,
  "n_real": N, "n_heygen": N,
  "cards_ok": N,
  "subcarpeta": "GUIONES JUEVES 29-05",
  "link_subcarpeta": "https://notion.so/...",
  "top1": {"titulo": "...", "score": 88},
  "top3": [
    {"titulo": "...", "bloque": "C", "score": 88,
     "hook_modo1": "...", "hook_modo2": "...",
     "formato_principal": "HeyGen"}
  ],
  "errores": []
}
```

Corré:
```bash
python agents/agent_07_notificador.py output/logs/pipeline_summary_${TS}.json
```

## Reporte final al usuario

Después del paso 7, imprimí:

```
✅ Ciclo #N completado en M min
   📰 15 noticias (A=5, B=4, C=6)
   📋 N guiones × 2 modos × 2 formatos = N cards
   ✅ N cards en Notion → [link subcarpeta]
   📱 2 mensajes Telegram enviados
```

## Reglas operativas

- **Nunca inventes URLs ni datos**. Siempre WebFetch antes de citar.
- **Si un paso falla**, loggeá el error en `output/logs/error_paso_X_${TS}.log` y continuá con dict vacío.
- **El paso 7 SIEMPRE se ejecuta**, incluso si pasos previos fallaron.
- **Auth**: Notion y Telegram se autentican desde `.env` (cargado por los scripts Python con `load_dotenv(override=True)`).
- **Sin LLM externo**: este pipeline corre 100% dentro de Claude Code. No usa la API de Anthropic. Costo extra: $0.
