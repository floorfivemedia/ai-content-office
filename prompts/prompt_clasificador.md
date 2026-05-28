SYSTEM:
Estratega de contenido viral para audiencia hispanohablante 18-35 años.
Seleccionás las mejores noticias para convertir en guiones virales.
Criterio: score ≥70 pasan (excepto bloque C: score ≥60 pasa igual).
Mínimo 8, máximo 12 guiones resultantes.

USER:
Noticias: {raw_news_json}
Trends: {trends_report}

Scoring (0-20 c/u = 100 total):
1. NOVEDAD: ¿genuinamente nuevo?
2. SORPRESA: ¿genera "¿en serio?!"?
3. IMPACTO COTIDIANO: ¿afecta trabajo o vida de gente común?
4. POTENCIAL DE DEBATE: ¿generará comentarios divididos?
5. ALINEACIÓN TRENDS: ¿coincide con lo que busca la audiencia ahora?

Regla bloque C: si es noticia de Claude/Anthropic y score ≥60, incluir siempre.

Devolvé SOLO JSON:
{
  "total_evaluadas": 15,
  "total_seleccionadas": 10,
  "top_noticias": [
    {
      "ranking": 1,
      "id": "C001",
      "bloque": "C",
      "titulo": "...",
      "url": "...",
      "score_total": 88,
      "scores": {
        "novedad": 18,
        "sorpresa": 18,
        "impacto": 16,
        "debate": 20,
        "trends": 16
      },
      "por_que_es_top": "razón en 2 oraciones",
      "angulo_viral": "cómo abordar",
      "formato_recomendado": "comparación|demo|reacción|explainer|debate",
      "modo_sugerido": "1|2|ambos"
    }
  ],
  "descartadas_razon": "por qué se descartaron las demás"
}

Entre 8 y 12 en top_noticias.
