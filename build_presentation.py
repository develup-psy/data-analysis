"""편집 가능한 소스를 독립 실행되는 발표용 index.html로 묶는다."""

from __future__ import annotations

import base64
from html import escape
from pathlib import Path
from urllib.parse import quote

from presentation_source import SLIDES


ROOT = Path(__file__).resolve().parent


def render_slide(slide: dict[str, str], number: int) -> str:
    kind = slide["kind"]
    classes = f"slide {kind}" + (" dark" if kind in {"cover", "chapter", "closing"} else "")
    title = escape(slide["title"])
    if kind == "cover":
        title = title.replace(" 및 시각화", " 및<br><em>시각화</em>")
        inner = (
            f'<div class="hero"><h1>{title}</h1><p class="lead">{escape(slide["lead"])}</p></div>'
            f'{slide["body"]}<div class="byline">11.21 · 11.28　|　데이터 분석·시각화 프로젝트</div>'
        )
    elif kind == "chapter":
        chapter_number = slide["part"].split(" ")[0]
        inner = (
            f'<div class="kicker">PART {escape(chapter_number)}</div>'
            f'<div class="body"><span class="chapter-number" aria-hidden="true">{escape(chapter_number)}</span>'
            f'<h1>{title}</h1><p class="lead">{escape(slide["lead"])}</p></div>'
        )
    elif kind == "closing":
        inner = f'<div class="body"><h1>{title}</h1><p class="lead">{escape(slide["lead"])}</p>{slide["body"]}</div>'
    else:
        kicker = "TODAY’S ROUTE" if kind == "toc" else escape(slide["part"])
        inner = (
            f'<div class="kicker">{kicker}</div><h1>{title}</h1>'
            f'<p class="lead">{escape(slide["lead"])}</p><div class="body">{slide["body"]}</div>'
        )
    source = escape(slide["source"])
    return (
        f'<section class="{classes}" data-title="{escape(slide["title"], quote=True)}" '
        f'data-part="{escape(slide["part"], quote=True)}" aria-label="{number}. {escape(slide["title"], quote=True)}">'
        f'{inner}<div class="foot"><span class="source">{source}</span><span class="page">{number:02d}</span></div>'
        f'<aside class="speaker-note" hidden>{escape(slide["note"])}</aside></section>'
    )


def build() -> Path:
    fonts = (ROOT / "assets" / "fonts.css").read_text()
    font_licenses = "\n\n".join(
        (ROOT / "assets" / "licenses" / name).read_text()
        for name in ("Paperlogy-OFL.txt", "Pretendard-LICENSE.txt")
    )
    styles = (ROOT / "presentation.css").read_text()
    javascript = (ROOT / "presentation.js").read_text()
    image = base64.b64encode((ROOT / "assets" / "telecom-cover.png").read_bytes()).decode("ascii")
    telecom_files = list((ROOT / "결과물").glob("*.html"))
    if len(telecom_files) != 1:
        raise RuntimeError("통신사 시연 HTML 파일을 하나만 찾을 수 있어야 합니다.")
    href = "./결과물/" + quote(telecom_files[0].name)
    slides_html = "\n".join(render_slide(slide, i) for i, slide in enumerate(SLIDES, 1))
    slides_html = slides_html.replace("{{TELECOM_IMAGE}}", "data:image/png;base64," + image)
    slides_html = slides_html.replace("{{TELECOM_HREF}}", escape(href, quote=True))
    result = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>데이터 분석 및 시각화 · 강의 자료</title>
<!-- Paperlogy and Pretendard fonts: SIL OFL 1.1. See lecture/assets/fonts.css. -->
<style>{fonts}\n{styles}</style></head>
<body><div id="viewport"><main id="stage" aria-label="데이터 분석 및 시각화 발표 자료">{slides_html}</main></div>
<nav id="toolbar" aria-label="발표 조작"><div id="progress"></div><div><strong id="counter"></strong>　<span id="partname"></span></div>
<div class="toolbar-actions"><button id="prev" type="button">← 이전</button><button id="next" type="button">다음 →</button>
<button id="notesButton" type="button">발표자 노트 N</button><button id="fullButton" type="button">전체 화면 F</button></div></nav>
<div id="promptModal" class="overlay" role="dialog" aria-modal="true" aria-label="실습 프롬프트"><div class="modal-panel">
<div class="modal-head"><div><span>실습 프롬프트</span><h2 id="promptTitle"></h2></div><button id="promptClose" type="button" aria-label="닫기">닫기 ×</button></div>
<pre id="promptFull"></pre><button id="modalCopy" type="button">프롬프트 복사</button></div></div>
<div id="notes" class="overlay" role="dialog" aria-modal="true" aria-label="발표자 노트"><div class="modal-panel">
<div class="modal-head"><div><span id="notePage"></span><h2 id="noteTitle"></h2></div><button id="closeNotes" type="button" aria-label="닫기">닫기 ×</button></div>
<textarea id="noteText" aria-label="현재 슬라이드의 발표자 노트" spellcheck="true"></textarea>
<div class="note-actions"><button id="saveNotes" type="button">저장</button><button id="downloadNotes" type="button">전체 노트 다운로드</button>
<label>노트 파일 불러오기<input id="uploadNotes" type="file" accept="application/json,.json"></label><span id="noteStatus"></span></div></div></div>
<div id="copyStatus" role="status" aria-live="polite"></div><div id="blackout"></div>
<template id="font-license-notices"><pre>{escape(font_licenses)}</pre></template>
<script>{javascript}</script></body></html>'''
    output = ROOT / "index.html"
    output.write_text(result, encoding="utf-8")
    return output


if __name__ == "__main__":
    output = build()
    print(f"{output}: {len(SLIDES)} slides, {output.stat().st_size:,} bytes")
