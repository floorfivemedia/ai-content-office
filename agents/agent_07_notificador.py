"""Agent 07 — Notificador (CLI standalone).

Manda resumen + top 3 guiones por Telegram. Solo HTTP, sin LLM.

Uso:
    python agents/agent_07_notificador.py <pipeline_summary.json>
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


def _send(token, chat_id, text):
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text[:4090], "parse_mode": "HTML"},
        timeout=20,
    )
    return r.ok, r.text


def _resumen_msg(s):
    bloques = s.get("bloques", {})
    errores = s.get("errores", [])
    msg = (
        f"🤖 <b>AI Content Office — Ciclo #{s.get('ciclo', '?')}</b>\n"
        f"📅 {s.get('fecha', '')} | ⏱️ {s.get('duracion_min', '?')} min | {s.get('trigger', 'SCHEDULED')}\n\n"
        f"📦 <b>Noticias (15 total):</b>\n"
        f"• 🌐 Bloque A (IA general): {bloques.get('A', 0)}\n"
        f"• 🚀 Bloque B (Lanzamientos): {bloques.get('B', 0)}\n"
        f"• 🤖 Bloque C (Claude/Anthropic): {bloques.get('C', 0)}\n\n"
        f"📋 <b>Guiones generados: {s.get('total_guiones', 0)}</b>\n"
        f"• Modo 1 (cortos): {s.get('n_modo_1', 0)}\n"
        f"• Modo 2 (profundos): {s.get('n_modo_2', 0)}\n"
        f"• Versiones Real: {s.get('n_real', 0)}\n"
        f"• Versiones HeyGen: {s.get('n_heygen', 0)}\n\n"
        f"✅ {s.get('cards_ok', 0)} cards en Notion → {s.get('subcarpeta', '?')}\n\n"
        f"🏆 Noticia #1: {s.get('top1', {}).get('titulo', '—')} (Score {s.get('top1', {}).get('score', '—')}/100)"
    )
    if errores:
        msg += f"\n\n⚠️ <b>{len(errores)} error(es):</b> " + ", ".join(errores[:5])
    return msg


def _top3_msg(s):
    out = ["📋 <b>Top 3 guiones listos:</b>\n"]
    for g in s.get("top3", [])[:3]:
        emoji = "🤖" if g.get("formato_principal") == "HeyGen" else "🎬"
        out.append(
            f"{emoji} [{g.get('bloque', '?')}] {g.get('titulo', '—')} — Score {g.get('score', '?')}/100\n"
            f"M1 Hook: \"{g.get('hook_modo1', '')}\"\n"
            f"M2 Hook: \"{g.get('hook_modo2', '')}\"\n"
        )
    link = s.get("link_subcarpeta", "")
    if link:
        out.append(f"\n🔗 Notion: {link}")
    out.append("\n💡 Revisá HeyGen antes de subir el avatar.")
    return "\n".join(out)


def notificar(pipeline_summary):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return {
            "mensajes_enviados": 0,
            "telegram_ok": False,
            "error": "TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados",
        }

    enviados, error = 0, None
    try:
        ok1, _ = _send(token, chat_id, _resumen_msg(pipeline_summary))
        if ok1:
            enviados += 1
        ok2, _ = _send(token, chat_id, _top3_msg(pipeline_summary))
        if ok2:
            enviados += 1
    except Exception as e:
        error = str(e)

    return {
        "mensajes_enviados": enviados,
        "telegram_ok": enviados == 2,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "error": error,
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python agents/agent_07_notificador.py <pipeline_summary.json>")
        sys.exit(1)

    root = Path(__file__).parent.parent
    load_dotenv(root / ".env", override=True)

    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = notificar(summary)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
