# Skill: Estructura Notion — Content Office

## Jerarquía
NIVEL 1: "PROYECTO CONTENIDO IA - AGENTES"  ← carpeta raíz (crear una vez)
NIVEL 2: "GUIONES [DÍA] [DD-MM]"            ← crear en cada carga
  Ej: "GUIONES JUEVES 29-05"
  Ej: "GUIONES SÁBADO 31-05"

## Propiedades de cada card
Título:      "🎬 [noticia] — Modo 1" o "🤖 [noticia] — HeyGen M2"
Estado:      Listo / Grabado / Publicado / Descartado
Modo:        Modo 1 (corto) / Modo 2 (profundo)
Formato:     Real / HeyGen
Bloque:      A / B / C
Score viral: 0-100
Fuente:      URL noticia

## Contenido de cada página
1. Callout → HOOK en negrita
2. "📰 Noticia" → resumen + URL
3. "📋 Modo 1 — Corto" → guion completo
4. "📋 Modo 2 — Profundo" → guion completo
5. "🤖 Versión HeyGen" → guion con pausas
6. "📊 TikTok" → caption + hashtags TikTok
7. "📊 Instagram" → caption + hashtags Instagram
8. "📊 YouTube" → caption + hashtags + títulos YouTube
9. "🖼️ Thumbnail" → especificaciones exactas
10. "✅ Checklist publicación":
    [ ] TikTok subido   — Fecha: ___
    [ ] Reels subido    — Fecha: ___
    [ ] Shorts subido   — Fecha: ___
    [ ] Formato: Real / HeyGen

## API Notion
POST https://api.notion.com/v1/pages
Headers: Authorization Bearer + Notion-Version: 2022-06-28
