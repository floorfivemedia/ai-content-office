"""Agent 07 — Notificador (CLI standalone).

Intenta envío directo a Telegram. Si el entorno cloud bloquea api.telegram.org,
hace fallback automático a GitHub Actions workflow_dispatch (relay gratuito).

Uso:
    python agents/agent_07_notificador.py <pipeline_summary.json>

Vars de entorno (.env):
    TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID   — siempre requeridas
    GITHUB_PAT                             — PAT con Actions:write (para fallback cloud)
    GITHUB_REPO                            — ej: floorfivemedia/ai-content-office
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# ── Telegram directo ──────────────────────────────────────────────────────────

def _send_telegram(token, chat_id, text):
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data={"chat_id": chat_id, "text": text[:4090], "parse_mode": "HTML"},
        timeout=20,
    )
    return r.ok, r.text


# ── GitHub Actions dispatch (fallback cloud) ──────────────────────────────────

def _dispatch_github(summary_data):
    """Dispara telegram-notify.yml via GitHub API. Retorna (ok, msg)."""
    pat = os.environ.get("GITHUB_PAT", "")
    repo = os.environ.get("GITHUB_REPO", "floorfivemedia/ai-content-office")
    if not pat:
        return False, "GITHUB_PAT no configurado — no se puede hacer fallback"

    url = f"https://api.github.com/repos/{repo}/actions/workflows/telegram-notify.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {
        "ref": "main",
        "inputs": {"summary_json": json.dumps(summary_data, ensure_ascii=False)},
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code == 204:
            return True, "GitHub Actions dispatch OK — mensajes llegan en ~30s"
        return False, f"GitHub API {r.status_code}: {r.text[:300]}"
    except Exception as e:
        return False, f"GitHub dispatch exception: {e}"


# ── Mensajes Telegram ─────────────────────────────────────────────────────────

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
        f"✅ {s.get('cards_ok', 0)} cards en Notion → {s.get('subcarpeta', '?')}\n\n"
        f"🏆 Top: {s.get('top1', {}).get('titulo', '—')} "
        f"(Score {s.get('top1', {}).get('score', '—')}/100)"
    )
    if errores:
        msg += f"\n\n⚠️ <b>{len(errores)} error(es):</b> " + ", ".join(errores[:5])
    return msg


def _top3_msg(s):
    out = ["📋 <b>Top 3 guiones:</b>\n"]
    for g in s.get("top3", [])[:3]:
        out.append(
            f"🎬 [{g.get('bloque', '?')}] {g.get('titulo', '—')} — Score {g.get('score', '?')}/100\n"
            f"M1: \"{g.get('hook_modo1', '')}\"\n"
            f"M2: \"{g.get('hook_modo2', '')}\"\n"
        )
    link = s.get("link_subcarpeta", "")
    if link:
        out.append(f"\n🔗 Notion: {link}")
    return "\n".join(out)


# ── Orquestador ───────────────────────────────────────────────────────────────

def notificar(pipeline_summary):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return {
            "mensajes_enviados": 0,
            "telegram_ok": False,
            "via": None,
            "error": "TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID no configurados",
        }

    # Intento directo
    try:
        enviados = 0
        ok1, _ = _send_telegram(token, chat_id, _resumen_msg(pipeline_summary))
        if ok1:
            enviados += 1
        ok2, _ = _send_telegram(token, chat_id, _top3_msg(pipeline_summary))
        if ok2:
            enviados += 1
        return {
            "mensajes_enviados": enviados,
            "telegram_ok": enviados == 2,
            "via": "direct",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
    except Exception as e:
        print(f"  ⚠️ Telegram directo falló ({e}). Fallback → GitHub Actions...")

    # Fallback: GitHub Actions dispatch
    ok, msg = _dispatch_github(pipeline_summary)
    return {
        "mensajes_enviados": 2 if ok else 0,
        "telegram_ok": ok,
        "via": "github_actions" if ok else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "github_dispatch": msg,
        "error": None if ok else msg,
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python agents/agent_07_notificador.py <pipeline_summary.json>")
        sys.exit(1)

    root = Path(__file__).parent.parent
    load_dotenv(root / ".env", override=True)

    summary = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = notificar(summary)

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    print(json.dumps(result, ensure_ascii=False, indent=2))
    via = result.get("via")
    if result.get("telegram_ok"):
        print(f"\n[OK] Telegram enviado via {via}")
    else:
        print(f"\n[FAIL] Telegram fallo: {result.get('error')}")


if __name__ == "__main__":
    main()
