# AI Content Office — Contexto Maestro

## Visión
Pipeline automatizado de contenido viral sobre IA. Corre **100% dentro de Claude Code** —
sin llamadas a la API de Anthropic, sin costo de tokens más allá de tu suscripción.

Flujo: Trends → 15 noticias (3 bloques) → Top 8-12 → guiones DOS MODOS →
Real + HeyGen → metadata por plataforma → Notion → Telegram.

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

El asistente (Claude Code, modelo actual de la sesión) ejecuta los pasos 0-5 inline
usando WebSearch + WebFetch nativos. Los pasos 6-7 son llamadas HTTP puras vía Python.

## Creador del contenido
- Venezolano, 31 años, vive en Argentina
- Acento venezolano — informa tono y vocabulario de guiones
- Audiencia: hispanohablante, 18-35 años, Latinoamérica
- Formatos: Reels grabados propios + avatar HeyGen con su rostro
- Plataformas: TikTok, Instagram Reels, YouTube Shorts
- Estilo: disruptivo, directo, alta energía — sin violencia ni groserías

## Modelo
La calidad del contenido depende del modelo seleccionado en la sesión de Claude Code
que corra el slash command. **Recomendado: Opus 4.7** (mejor para guiones virales).
Para tareas mecánicas (clasificar, adaptar HeyGen) Sonnet 4.6 también sirve.

## Noticias — 3 Bloques (15 total por ciclo)
- BLOQUE A (5): Información relevante general de IA
- BLOQUE B (4): Nuevos lanzamientos de modelos/herramientas
- BLOQUE C (6): Anthropic, Claude, Claude Code, Claude Cowork — PRIORIDAD

## Guiones — Cantidad y Modos
- Total: entre 8 y 12 guiones por ciclo (score ≥70, o ≥60 si bloque C)
- MODO 1: Viral Corto 30-40 segundos
- MODO 2: Viral Profundo 60-90 segundos
- Cada noticia genera AMBOS modos en versión Real y versión HeyGen

## Metadata por Plataforma
- TikTok:    caption 80-100 palabras, casual, 15-20 hashtags
- Instagram: caption 120-180 palabras, pulido, 20-25 hashtags
- YouTube:   caption 150-200 palabras, búsqueda, 3-5 hashtags
- Thumbnail: specs exactas con hex colors

## Notion — Estructura
- Página raíz: `AI Content Office` (creada, ID en `.env` como `NOTION_DATABASE_ID`)
- Subcarpeta por ciclo: `GUIONES [DÍA] [DD-MM]`
- Cada guion = 2 cards (Real + HeyGen) con guion completo, metadata 3 plataformas, thumbnail, checklist

## Reglas
1. Pipeline siempre secuencial (paso 0 → 7)
2. Paso 7 (Telegram) SIEMPRE corre, incluso con errores previos
3. Nunca hardcodear credenciales
4. Outputs con timestamp en nombre
5. Datos reales siempre vía WebFetch — nunca inventar URLs ni cifras
