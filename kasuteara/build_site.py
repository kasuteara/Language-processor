from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CH = ROOT / "md" / "chapters"
TEMPLATE = Path(r"C:\Users\kabay\OneDrive\3年前期\.codex\skills\study-site-builder\assets\index-template.html")


def read(name: str) -> str:
    return (CH / name).read_text(encoding="utf-8")


# 2026-07-12にここで発見した3つの見づらさ問題（color-scheme未宣言によるブラウザ強制ダーク
# モードの誤変換、.intuition-boxのダークモード未対応、.lecture-headerがセクション全体を
# 単色グラデーションで塗りつぶす設計）は、skill共通テンプレート
# （.codex/skills/study-site-builder/assets/index-template.html）側に直接反映済み。
# 以下はそのテンプレートと二重になるが、無害なので残してある（テンプレートが将来さらに
# 更新されても、このサイトの見た目は最低限このバージョンで固定される）。
LOCAL_STYLE_OVERRIDE = """
<meta name="color-scheme" content="light dark">
<style>
  :root { color-scheme: light dark; }
  /* .intuition-box: ダークモードで固定の薄い水色のまま浮いて見づらい問題を修正 */
  .intuition-box { background: #eff6ff; border-left: 6px solid #2563eb; color: #1e3a8a; }
  @media (prefers-color-scheme: dark) {
    .intuition-box { background: #16233f; border-left-color: #60a5fa; color: #dbeafe; }
  }
  /* .lecture-header: セクション全体の単色塗りをやめ、見出し帯だけに色を限定 */
  .lecture-header { background: none; color: var(--text); padding: 0; border-radius: 0; margin-top: 50px; }
  .lecture-header h2 {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white; border: none; margin: 0 0 20px; padding: 16px 20px; border-radius: 10px;
  }
</style>
"""


def main() -> None:
    global_pre = read("global_pre.html")
    global_mid = read("global_mid.html")
    fragment_a = read("fragment_A.html")
    fragment_b = read("fragment_B.html")
    fragment_c = read("fragment_C.html")
    fragment_d = read("fragment_D.html")

    sources_intro = """
<section id="sources-complete" class="band">
<h2>授業回ごとの0から理解する解説</h2>
<p>ここから先は、授業資料12回分を「0から理解する」解説記事として書き直したものである。原文の逐語コピーではなく、各回の概念を定義・直感・具体例・図解の順に説明し直している。原資料にない事実は書かず、補足には必ず「補足:」と明記した。全ページの原文（テキストと画像）は要約・改変せずそのままフォルダ内 <code>md/sources/</code> に保存してあり、各回の記事末尾のリンクから参照できる。</p>
</section>
"""

    yamai_wrapper_open = '<section id="yamai-full" class="band soft"><h2>山井先生パート 0から理解する（形式言語・オートマトン・構文解析）</h2>'
    yamai_wrapper_close = "</section>"
    kaneko_wrapper_open = '<section id="kaneko-full" class="band"><h2>金子先生パート 0から理解する（コンパイラのコード生成・実行時モデル・最適化）</h2>'
    kaneko_wrapper_close = "</section>"

    content_parts = [
        global_pre,
        global_mid,
        sources_intro,
        yamai_wrapper_open, fragment_a, fragment_b, yamai_wrapper_close,
        kaneko_wrapper_open, fragment_c, fragment_d, kaneko_wrapper_close,
    ]
    content = "\n".join(content_parts)

    # master.md: same assembled content, saved as reference markdown (embedded HTML is valid in md)
    master_md = "# 言語処理系 テスト対策完全版\n\n" + content
    (ROOT / "md" / "master.md").write_text(master_md, encoding="utf-8")

    template = TEMPLATE.read_text(encoding="utf-8")
    html = template.replace("{{SUBJECT}}", "言語処理系").replace("{{CONTENT}}", content)
    html = html.replace("</head>", LOCAL_STYLE_OVERRIDE + "</head>")
    (ROOT / "index.html").write_text(html, encoding="utf-8")

    # --- quality checks ---
    n_lecture = len(re.findall(r'class="lecture-header"', content))
    n_h3 = len(re.findall(r'<h3>', content))
    n_ai_badge = len(re.findall(r'badge-ai|⚙ AI生成', content))
    n_pred = len(re.findall(r'class="prediction-card', content))
    n_pastq = len(re.findall(r'class="past-exam-q"', content))
    n_source_links = len(re.findall(r'href="md/sources/[^"]+\.md"', content))

    img_srcs = set(re.findall(r'src="(images/[^"]+)"', content))
    missing = [p for p in img_srcs if not (ROOT / p).exists()]

    href_ids = set(re.findall(r'href="#([^"]+)"', content))
    real_ids = set(re.findall(r'id="([^"]+)"', content))
    broken_anchors = [h for h in href_ids if h not in real_ids and "' + " not in h]

    report = f"""# 完全攻略サイト 品質チェックレポート

- lecture-header数: {n_lecture} (期待値: 12)
- h3見出し数（0から理解する解説の内部構成）: {n_h3}
- AI生成バッジ/表記の出現数: {n_ai_badge}
- prediction-card数: {n_pred}
- past-exam-q数: {n_pastq}
- 原文(md/sources/)へのリンク数: {n_source_links} (期待値: 12)
- 画像参照ユニーク数: {len(img_srcs)}
- 存在しない画像参照: {len(missing)}件
{chr(10).join('  - ' + m for m in missing) if missing else '  (なし)'}
- 壊れた内部アンカーリンク: {len(broken_anchors)}件
{chr(10).join('  - ' + m for m in broken_anchors) if broken_anchors else '  (なし)'}
"""
    (ROOT / "md" / "quality_check_report.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
