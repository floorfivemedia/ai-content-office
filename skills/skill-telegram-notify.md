# Skill: Notificaciones Telegram

## Setup
1. @BotFather → /newbot → guardar TOKEN
2. Enviar msg al bot → api.telegram.org/bot{TOKEN}/getUpdates → tomar chat.id

## Función
import requests

def send_telegram(token, chat_id, msg):
    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
    )

## Formato HTML soportado
<b>negrita</b>  <i>cursiva</i>  <code>mono</code>  — emojis nativos ✅

## Templates

MENSAJE 1 — Resumen:
🤖 <b>AI Content Office — Ciclo #{n}</b>
📅 {fecha} | ⏱️ {min} min | Trigger: {SCHEDULED|MANUAL}

📊 <b>Resultado:</b>
• 📰 Bloque A: {n_a} | Bloque B: {n_b} | Bloque C: {n_c}
• 📋 {modo1} guiones Modo 1 + {modo2} guiones Modo 2
• 🎬 {real} versiones grabación | 🤖 {heygen} versiones HeyGen
• ✅ {cards} cards en Notion → {subcarpeta}

🏆 Noticia #1: {titulo} (Score {score}/100)

MENSAJE 2 — Guiones:
📋 <b>Top 3 guiones listos:</b>

{emoji} {titulo} — Score {score}/100
Hook M1: "{hook_modo1}"
Hook M2: "{hook_modo2}"

🔗 {link_notion}

💡 Revisá HeyGen antes de subir el avatar.
