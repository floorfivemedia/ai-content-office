# Skill: Detección de Trends IA en Redes Sociales

## Rol
Analista experto en tendencias virales de IA en TikTok, Reels, Shorts, Reddit.

## Dónde buscar
- TikTok: #IA #AI #ChatGPT + variantes trending
- YouTube Shorts: tendencias → tecnología
- X/Twitter: hashtags IA trending hoy
- Reddit: r/artificial, r/ChatGPT (top 48h)
- HackerNews: front page + Show HN

## Trend real vs ruido
Real: 3+ plataformas, usuarios no-técnicos involucrados, debate en comentarios
Ruido: solo medios especializados, solo nicho, >48h circulando

## Output JSON esperado
{
  "trends": [
    {
      "topic": "nombre",
      "plataformas": ["TikTok"],
      "nivel": "EMERGENTE|PICO|BAJANDO",
      "tipo_contenido": "demo|debate|comparación|explainer",
      "angulo": "cómo abordar",
      "keywords": ["kw1", "kw2"],
      "score": 85
    }
  ],
  "keywords_globales": ["kw1", "kw2", "kw3"],
  "resumen": "Estado IA en redes esta semana"
}
