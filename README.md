# Language-processor — 言語処理系 試験対策サイト 共有リポジトリ

「言語処理系」の試験対策として、各自が作成したサイトや資料を共有するためのリポジトリです。

## 📁 ルール: 1人1フォルダ

**自分専用のサブフォルダを作り、その中に一式を置いてください。**
root 直下や他人のフォルダには触れないこと（上書き・衝突防止のため）。

```
Language-processor/
├── README.md            ← このファイル
├── kasuteara/           ← 蒲谷佳和 のサイト
│   ├── index.html
│   └── images/ …
├── <あなたのGitHub名>/   ← あなたのサイトはここに
│   └── index.html …
└── …
```

- フォルダ名は **自分のGitHubユーザー名** を推奨（半角英数で URL/Pages と相性が良い）。
- そのフォルダの中に `index.html` を置けば、あなたのサイトの入口になります。

## ⚠️ index.html だけで足りるか確認

- **自己完結型**（画像を `data:image` の base64 で埋め込み・外部ファイル参照なし）
  → `index.html` 1枚だけ置けばOK。
- **外部ファイル参照型**（`<img src="images/…">` のように別ファイルを読む）
  → `index.html` と一緒に **`images/` などの参照ファイルもすべて** 同じフォルダに入れること。
  入れ忘れると画像がリンク切れ（×表示）になります。

判定の目安（自分のindex.htmlがあるフォルダで実行）:
```bash
grep -c 'src="images/' index.html   # 1以上なら images/ フォルダも必要
grep -c 'data:image'   index.html   # 多ければ自己完結寄り
```

## 🚀 サイトの追加方法

### 方法A: フォーク + プルリクエスト（書き込み権限が無い人向け・推奨）

```bash
# 1. このリポジトリをフォーク（GitHub上の Fork ボタン、または）
gh repo fork Test-preparation/Language-processor --clone

cd Language-processor

# 2. 自分のフォルダを作って一式をコピー
mkdir <あなたのGitHub名>
cp -r /path/to/あなたのサイト/* <あなたのGitHub名>/

# 3. コミットして自分のフォークに push
git add <あなたのGitHub名>
git commit -m "Add <あなたの名前>'s site"
git push origin main

# 4. プルリクエストを作成（管理者がマージ）
gh pr create --repo Test-preparation/Language-processor --base main
```

### 方法B: 直接 push（このリポジトリへの書き込み権限がある人向け）

```bash
git clone https://github.com/Test-preparation/Language-processor.git
cd Language-processor
mkdir <あなたのGitHub名>
cp -r /path/to/あなたのサイト/* <あなたのGitHub名>/
git add <あなたのGitHub名>
git commit -m "Add <あなたの名前>'s site"
git push origin main
```

## 💡 補足

- **軽量化**: サイト表示に使わない原資料スキャンや中間ファイルは、共有前に削っておくとリポジトリが軽くなります。
- **ブラウザ閲覧（GitHub Pages）**: Pages を有効化すると、各サイトを
  `https://test-preparation.github.io/Language-processor/<フォルダ名>/`
  のURLで直接閲覧できます（有効化は管理者が設定）。

## 参加者一覧

| フォルダ | 作者 | 内容 |
|---|---|---|
| `kasuteara/` | 蒲谷佳和 | 言語処理系 試験対策サイト（index.html + 図・過去問・MD資料） |
