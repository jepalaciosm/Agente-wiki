from datetime import datetime
from html import escape
from pathlib import Path
import re

from langchain.tools import tool


def _inline_markdown(text: str) -> str:
    safe_text = escape(text)
    safe_text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", safe_text)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", safe_text)


def _markdown_to_html(content: str) -> str:
    blocks = []
    paragraph = []
    list_tag = None
    list_items = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(paragraph)
            blocks.append(f"<p>{_inline_markdown(text)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_tag
        if list_tag:
            items = "".join(
                f"<li>{_inline_markdown(item)}</li>" for item in list_items
            )
            blocks.append(f"<{list_tag}>{items}</{list_tag}>")
            list_items.clear()
            list_tag = None

    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = min(len(heading.group(1)) + 1, 4)
            blocks.append(
                f"<h{level}>{_inline_markdown(heading.group(2))}</h{level}>"
            )
            continue

        unordered_item = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered_item = re.match(r"^\d+[.)]\s+(.+)$", stripped)
        item = unordered_item or ordered_item
        if item:
            flush_paragraph()
            current_list_tag = "ul" if unordered_item else "ol"
            if list_tag != current_list_tag:
                flush_list()
                list_tag = current_list_tag
            list_items.append(item.group(1))
            continue

        flush_list()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    return "\n".join(blocks)


@tool
def generar_reporte_html(contenido: str) -> str:
    """Guarda el informe del agente como un archivo HTML con formato profesional."""
    if not contenido.strip():
        raise ValueError("El contenido del informe no puede estar vacío.")

    now = datetime.now().astimezone()
    report_dir = Path(__file__).resolve().parents[1] / "reportes"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"informe_{now.strftime('%Y%m%d_%H%M%S_%f')}.html"

    html_document = """<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>Informe de agent-wiki</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Inter, "Segoe UI", Arial, sans-serif;
      color: #182230;
      background: #f2f5f9;
    }
    body { margin: 0; padding: 48px 20px; }
    main {
      max-width: 900px;
      margin: 0 auto;
      overflow: hidden;
      border: 1px solid #e3e8ef;
      border-radius: 18px;
      background: #fff;
      box-shadow: 0 18px 50px #18223012;
    }
    header {
      padding: 36px 44px;
      color: #fff;
      background: linear-gradient(125deg, #063b35, #087e70);
    }
    .eyebrow {
      margin: 0 0 10px;
      color: #b8eee4;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .14em;
      text-transform: uppercase;
    }
    h1 { margin: 0; font-size: clamp(27px, 5vw, 38px); }
    .date { margin: 12px 0 0; color: #d4f4ef; font-size: 14px; }
    article { padding: 32px 44px 44px; line-height: 1.7; }
    article h2, article h3, article h4 {
      margin: 30px 0 12px;
      color: #075e54;
      line-height: 1.3;
    }
    article h2 { padding-bottom: 9px; border-bottom: 1px solid #e7eeec; }
    article h3 { font-size: 20px; }
    article h4 { font-size: 17px; }
    article p { margin: 12px 0; }
    article ul, article ol { padding-left: 24px; }
    article li { margin: 7px 0; padding-left: 4px; }
    strong { color: #075e54; }
    code {
      padding: 2px 6px;
      border-radius: 5px;
      background: #edf4f3;
      color: #075e54;
      font-family: Consolas, monospace;
    }
    footer {
      padding: 16px 44px;
      border-top: 1px solid #e7eeec;
      color: #687782;
      font-size: 12px;
    }
    @media (max-width: 600px) {
      body { padding: 16px 10px; }
      header, article { padding: 26px 22px; }
      footer { padding: 14px 22px; }
    }
    @media print {
      :root { background: #fff; }
      body { padding: 0; }
      main { max-width: none; border: 0; box-shadow: none; }
      header { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <p class="eyebrow">Gerencia Analítica de Fraudes</p>
      <h1>Informe técnico</h1>
      <p class="date">Generado el __GENERATED_AT__</p>
    </header>
    <article>
      __REPORT_CONTENT__
    </article>
    <footer>Generado por agent-wiki</footer>
  </main>
</body>
</html>
"""
    html_document = html_document.replace(
        "__GENERATED_AT__", escape(now.strftime("%d/%m/%Y %H:%M"))
    ).replace("__REPORT_CONTENT__", _markdown_to_html(contenido))

    report_path.write_text(html_document, encoding="utf-8")
    return str(report_path.resolve())
