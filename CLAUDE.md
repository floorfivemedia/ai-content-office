# AI Content Office — Contexto Maestro

## Visión
Pipeline automatizado de contenido viral sobre IA. Corre **100% dentro de Claude Code** —
sin llamadas a la API de Anthropic, sin costo de tokens más allá de tu suscripción.

Flujo: Trends → 15 noticias (3 bloques) → Top 8 → guiones DOS MODOS →
metadata corta por plataforma → Notion → Telegram.

Optimizado para bajo consumo de tokens (~130K/ciclo en Sonnet vs ~310K en Opus).

## Cómo correrlo

**Manual** (desde cualquier sesión de Claude Code en este proyecto):
```
/ai-content-office MANUAL
```

**Automático cada 48h** (Cloud Routine):
1. Ir a https://claude.ai/code/scheduled
2. Nuevo task → comando: `/ai-content-office`
3. Schedule: `0 9 */2 * *` (9 AM cada 2 días)
4. Working dir: este proyecto
5. Activar

## Arquitectura

```
.claude/commands/ai-content-office.md   ← el slash command (orquestador)
ai-content-office/
├── prompts/                            ← 8 prompts de referencia para cada paso
├── skills/                             ← 6 docs de criterio (hooks, HeyGen, etc.)
├── agents/
│   ├── agent_06_archivador.py          ← HTTP a Notion (sin LLM)
│   └── agent_07_notificador.py         ← HTTP a Telegram (sin LLM)
├── output/{trends,news,scripts,logs}/  ← JSON intermedios
└── .env                                 ← credenciales (no committear)
```

El asistente (Claude Code, modelo actual de la sesión) ejecuta los pasos 0-4 inline
usando WebSearch + WebFetch nativos. Los pasos 5-6 son llamadas HTTP puras vía Python.
Pipeline = 6 pasos (se eliminó el Adaptador para ahorrar tokens).

## Creador del contenido
- Venezolano, 31 años, vive en Argentina
- Acento venezolano — informa tono y vocabulario de guiones
- Audiencia: hispanohablante, 18-35 años, Latinoamérica
- Formatos: Reels grabados propios + avatar HeyGen con su rostro
- Plataformas: TikTok, Instagram Reels, YouTube Shorts
- Estilo: disruptivo, directo, alta energía — sin violencia ni groserías

## Modelo
La calidad del contenido depende del modelo de la sesión que corra el slash command.
- **Rutina automática cada 48h**: `claude-sonnet-4-8` (mejor relación calidad/tokens, ~5× más barato que Opus).
- **Guion premium puntual**: correr `/ai-content-office MANUAL` desde sesión local con Opus.

## Noticias — 3 Bloques (15 total por ciclo)
- BLOQUE A (5): Información relevante general de IA
- BLOQUE B (4): Nuevos lanzamientos de modelos/herramientas
- BLOQUE C (6): Anthropic, Claude, Claude Code, Claude Cowork — PRIORIDAD

## Guiones — Cantidad y Modos
- Total: máximo 8 guiones por ciclo (score ≥70, o ≥60 si bloque C). Calidad > cantidad.
- MODO 1: Viral Corto 30-40 segundos
- MODO 2: Viral Profundo 60-90 segundos
- Oraciones cortas y claras: el mismo guion sirve para grabar en vivo y para HeyGen (sin versión aparte).

## Metadata por Plataforma (captions cortos para ahorrar tokens)
- TikTok:    caption ≤40 palabras, casual, 15-20 hashtags
- Instagram: caption ≤40 palabras, pulido, 20-25 hashtags
- YouTube:   caption ≤40 palabras, búsqueda, 3-5 hashtags + 3 títulos
- Thumbnail: specs cortas con hex colors

## Notion — Estructura
- Página raíz: `AI Content Office` (creada, ID en `.env` como `NOTION_DATABASE_ID`)
- Subcarpeta por ciclo: `GUIONES [DÍA] [DD-MM]`
- Cada guion = 1 card (Modo 1 + Modo 2 + metadata 3 plataformas + thumbnail + checklist)

## Reglas
1. Pipeline siempre secuencial (paso 0 → 6)
2. Paso 6 (Telegram) SIEMPRE corre, incluso con errores previos
3. Nunca hardcodear credenciales
4. Outputs con timestamp en nombre
5. Datos reales siempre vía WebFetch — nunca inventar URLs ni cifras
