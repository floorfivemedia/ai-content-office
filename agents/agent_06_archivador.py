"""Agent 06 — Archivador (CLI standalone).

Crea páginas en Notion bajo subcarpeta del día. Solo HTTP, sin LLM.

Uso:
    python agents/agent_06_archivador.py <full_content.json>

donde full_content.json contiene:
{
  "guiones":      [...],   # de output/scripts/scripts_master_*.json -> guiones
  "adaptaciones": [...],   # de output/scripts/scripts_adapted_*.json -> adaptaciones
  "metadata":     [...]    # de output/scripts/metadata_*.json -> metadata
}
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

NOTION_VERSION = "2022-06-28"
NOTION_API = "https://api.notion.com/v1"

DIAS_ES = {
    0: "LUNES", 1: "MARTES", 2: "MIÉRCOLES", 3: "JUEVES",
    4: "VIERNES", 5: "SÁBADO", 6: "DOMINGO",
}


def _subcarpeta_nombre():
    now = datetime.now()
    return f"GUIONES {DIAS_ES[now.weekday()]} {now.strftime('%d-%m')}"


def _headers():
    return {
        "Authorization": f"Bearer {os.environ['NOTION_API_KEY']}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def _create_page(parent_id, title, children=None, icon_emoji=None):
    payload = {
        "parent": {"page_id": parent_id},
        "properties": {"title": [{"type": "text", "text": {"content": title}}]},
    }
    if icon_emoji:
        payload["icon"] = {"type": "emoji", "emoji": icon_emoji}
    if children:
        payload["children"] = children[:100]
    r = requests.post(f"{NOTION_API}/pages", headers=_headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def _paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": (text or "")[:1900]}}]},
    }


def _heading(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def _callout(text):
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{
                "type": "text",
                "text": {"content": (text or "")[:1900]},
                "annotations": {"bold": True},
            }],
            "icon": {"type": "emoji", "emoji": "🎯"},
        },
    }


def _todo(text):
    return {
        "object": "block",
        "type": "to_do",
        "to_do": {
            "rich_text": [{"type": "text", "text": {"content": text}}],
            "checked": False,
        },
    }


def _build_card_blocks(guion, adapt, meta, formato):
    blocks = []
    hook = guion.get("modo_1", {}).get("hook") or guion.get("modo_2", {}).get("hook") or ""
    if hook:
        blocks.append(_callout(hook))

    blocks.append(_heading("📰 Noticia"))
    titulo = guion.get("noticia_titulo", "")
    url = guion.get("noticia_url", "")
    blocks.append(_paragraph(f"{titulo}\n{url}"))

    if formato == "Real":
        blocks.append(_heading("📋 Modo 1 — Corto (30-40 seg)"))
        blocks.append(_paragraph(adapt.get("1", {}).get("version_real", {}).get("guion", "")
                                 or guion.get("modo_1", {}).get("guion_completo", "")))
        blocks.append(_heading("📋 Modo 2 — Profundo (60-90 seg)"))
        blocks.append(_paragraph(adapt.get("2", {}).get("version_real", {}).get("guion", "")
                                 or guion.get("modo_2", {}).get("guion_completo", "")))
    else:
        blocks.append(_heading("🤖 Modo 1 — HeyGen (con pausas)"))
        blocks.append(_paragraph(adapt.get("1", {}).get("version_heygen", {}).get("guion", "")))
        blocks.append(_heading("🤖 Modo 2 — HeyGen (con pausas)"))
        blocks.append(_paragraph(adapt.get("2", {}).get("version_heygen", {}).get("guion", "")))

    tk = meta.get("tiktok", {})
    blocks.append(_heading("📊 TikTok"))
    blocks.append(_paragraph(
        (tk.get("caption", "") or "") + "\n\n" + " ".join("#" + h for h in tk.get("hashtags", []))
    ))

    ig = meta.get("instagram", {})
    blocks.append(_heading("📊 Instagram"))
    blocks.append(_paragraph(
        (ig.get("caption", "") or "") + "\n\n" + " ".join("#" + h for h in ig.get("hashtags", []))
    ))

    yt = meta.get("youtube", {})
    titulos = yt.get("titulos", {})
    yt_text = (yt.get("caption", "") or "") + "\n\n" + " ".join("#" + h for h in yt.get("hashtags", []))
    yt_text += (
        f"\n\nBeneficio: {titulos.get('beneficio', '')}"
        f"\nCuriosidad: {titulos.get('curiosidad', '')}"
        f"\nNúmero: {titulos.get('numero', '')}"
    )
    blocks.append(_heading("📊 YouTube Shorts"))
    blocks.append(_paragraph(yt_text))

    th = meta.get("thumbnail", {})
    if th:
        blocks.append(_heading("🖼️ Thumbnail"))
        blocks.append(_paragraph(json.dumps(th, ensure_ascii=False, indent=2)))

    blocks.append(_heading("✅ Checklist publicación"))
    blocks.append(_todo("TikTok subido — Fecha: ___"))
    blocks.append(_todo("Reels subido — Fecha: ___"))
    blocks.append(_todo("Shorts subido — Fecha: ___"))
    blocks.append(_paragraph(f"Formato usado: {formato}"))

    return blocks


def archivar(payload):
    parent_id = os.environ["NOTION_DATABASE_ID"]
    subcarpeta_nombre = _subcarpeta_nombre()

    result = {
        "subcarpeta_nombre": subcarpeta_nombre,
        "subcarpeta_id": None,
        "cards_creadas": [],
        "total_ok": 0,
        "total_error": 0,
        "link_subcarpeta": None,
    }

    sub = _create_page(parent_id, subcarpeta_nombre, icon_emoji="📅")
    result["subcarpeta_id"] = sub.get("id")
    result["link_subcarpeta"] = sub.get("url")

    guiones = payload.get("guiones", [])
    adapt_by_guion = {}
    for a in payload.get("adaptaciones", []):
        adapt_by_guion.setdefault(a.get("guion_id"), {})[str(a.get("modo"))] = a
    meta_by_adapt = {m.get("adaptacion_id"): m for m in payload.get("metadata", [])}

    for g in guiones:
        titulo = g.get("noticia_titulo", "Sin título")
        bloque = g.get("bloque", "?")
        score = g.get("score_viral", 0)
        adapt_map = adapt_by_guion.get(g.get("id"), {})

        for emoji, formato in (("🎬", "Real"), ("🤖", "HeyGen")):
            card_title = f"{emoji} {titulo} — {formato}"
            adapt1 = adapt_map.get("1", {})
            meta1 = meta_by_adapt.get(adapt1.get("id"), {})
            try:
                blocks = _build_card_blocks(g, adapt_map, meta1, formato)
                page = _create_page(result["subcarpeta_id"], card_title, blocks, icon_emoji=emoji)
                result["cards_creadas"].append({
                    "titulo": card_title,
                    "notion_id": page.get("id"),
                    "notion_url": page.get("url"),
                    "bloque": bloque,
                    "score": score,
                    "status": "creada",
                })
                result["total_ok"] += 1
                print(f"  ✓ {card_title}")
            except Exception as e:
                result["cards_creadas"].append({
                    "titulo": card_title,
                    "status": "error",
                    "error": str(e),
                })
                result["total_error"] += 1
                print(f"  ✗ {card_title}: {e}")

    return result


def main():
    if len(sys.argv) < 2:
        print("Uso: python agents/agent_06_archivador.py <full_content.json>")
        sys.exit(1)

    root = Path(__file__).parent.parent
    load_dotenv(root / ".env", override=True)

    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    result = archivar(payload)

    out_dir = root / "output" / "logs"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"notion_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n✅ {result['total_ok']} cards creadas | ✗ {result['total_error']} errores")
    print(f"📂 Subcarpeta: {result['subcarpeta_nombre']}")
    print(f"🔗 {result['link_subcarpeta']}")
    print(f"📝 Log: {out_path}")


if __name__ == "__main__":
    main()
