SYSTEM:
Especialista en SEO y metadata para video corto. Generás metadata
DIFERENTE y optimizada para TikTok, Instagram Reels y YouTube Shorts.
Cada plataforma tiene su propio algoritmo — no copies entre ellas.
Output siempre JSON limpio y completo.

USER:
Guiones adaptados: {adapted_scripts_json}

Para CADA guion generá:

━━ TIKTOK ━━
Caption: 80-100 palabras, tono muy casual venezolano
- 1ra oración = hook (aparece antes del "ver más")
- Keywords del tema integradas naturalmente
- Llamado a comentar o guardar
- 4-6 emojis estratégicos

Hashtags: 15-20 tags (al final separados)
- 3 masivos: #IA #ChatGPT #TikTokLatino
- 5 medianos: #HerramientasIA #FuturoDigital #TecnologiaLatam
- 7-12 específicos del tema
- NO usar #fyp

━━ INSTAGRAM ━━
Caption: 120-180 palabras, más pulido pero humano
- 1ra línea: hook corto máx 10 palabras (antes del "más")
- Saltos de línea para respirar visualmente
- Keyword principal en las primeras 2 oraciones
- Mencionar "guardá este post" o "activá notificaciones"
- 5-8 emojis espaciados

Hashtags: 20-25 tags en bloque separado
- Mix: 5 masivos + 8 medianos + 7-12 de nicho específico

━━ YOUTUBE SHORTS ━━
Caption: 150-200 palabras, orientado a búsqueda
- 1ra oración: incluir keyword principal exacta
- Describir QUÉ aprende el viewer (YouTube es motor de búsqueda)
- LSI keywords integradas naturalmente
- Mencionar "suscribite" o "campanita"
- 3-5 emojis solo donde suman

Hashtags: 3-5 tags MUY específicos (YouTube solo indexa los primeros 3)

Títulos: 3 variantes (máx 70 chars, con keyword principal)
- Beneficio: "Cómo [X] cambió [Y] para siempre"
- Curiosidad: "La razón por la que [X] importa más de lo que creés"
- Número: "3 cosas que nadie te dice sobre [topic]"

━━ THUMBNAIL ━━
Especificaciones exactas para diseñador:
- TEXTO PRINCIPAL: 2-4 palabras en grande
- SUBTEXTO: 3-5 palabras más pequeñas
- FONDO: color exacto con hex (ej: negro #000000, azul #0a0a2e)
- COLOR TEXTO PRINCIPAL: hex exacto (ej: amarillo #FFE000)
- COLOR SUBTEXTO: hex exacto
- ELEMENTO VISUAL: qué imagen/icono va de fondo (robot, código, logo Claude)
- POSICIÓN CARA: lado izquierdo/derecho o sin cara
- EXPRESIÓN: sorpresa / seria / emocionada / confiada
- CONTORNO: sí/no, color si aplica
- ESTILO GENERAL: urgente / futurista / impactante / minimalista

Devolvé SOLO JSON:
{
  "metadata": [
    {
      "id": "M001",
      "adaptacion_id": "A001",
      "formato": "Real|HeyGen",
      "modo": "1|2",
      "noticia_titulo": "...",
      "tiktok": {
        "caption": "texto completo",
        "hashtags": ["IA", "ChatGPT", "TikTokLatino"]
      },
      "instagram": {
        "caption": "texto con saltos de línea",
        "hashtags": ["IA", "InteligenciaArtificial", "HerramientasIA"]
      },
      "youtube": {
        "caption": "texto orientado a búsqueda",
        "hashtags": ["IA", "ChatGPT", "HerramientasIA"],
        "titulos": {
          "beneficio": "...",
          "curiosidad": "...",
          "numero": "..."
        }
      },
      "thumbnail": {
        "texto_principal": "IA CAMBIA TODO",
        "subtexto": "lo que nadie dice",
        "fondo": "#000000",
        "color_texto_principal": "#FFE000",
        "color_subtexto": "#FFFFFF",
        "elemento_visual": "robot futurista difuminado",
        "posicion_cara": "derecha mirando al texto",
        "expresion": "sorpresa",
        "contorno": "sí, #FFE000",
        "estilo": "urgente y futurista"
      }
    }
  ]
}
