# joo-glyphtag-addons

Odoo Contacts に日本語の氏名・住所を扱うための機能を追加するアドオン群です。  
ふりがな、GlyphTag、異体字正規化、IVS 表示、フォント設定をまとめて提供します。  
`joo_contacts_jp` はこれらを統合したアプリケーションです。

---

## 1. モジュール構成

```
joo_partner_furigana       氏名のふりがな入力・検索
joo_partner_glyphtag       GlyphTag 入力と IVS 出力
joo_tofurengo              GlyphTag 正規化エンジン
joo_glyph_fonts            MJ/GJ フォント（backend）
joo_website_glyph_fonts    MJ/GJ フォント（website）
joo_contacts_jp            Contacts 日本語拡張アプリ
```

---

## 2. 各モジュールの機能

### joo_partner_furigana
- res.partner に `furigana` を追加  
- 氏名の読みを入力できる  
- 読みで検索できる  
- ひらがな／カタカナ／スペース統一の正規化設定

### joo_partner_glyphtag
- 氏名・住所の GlyphTag 入力フィールドを追加  
- GlyphTag を IVS に変換して表示  
- 通常文字列と GlyphTag の同期  
- 氏名・住所の編集用ダイアログを提供  
- Contacts の検索に GlyphTag を統合

#### 入力タグの例（出力例は記載しない）
```
{MJ022335}
{MJ007003}
𛀆𛀁𛀀
```

### joo_tofurengo
- GlyphTag の正規化処理  
- MJ/GJ データセットの切り替え  
- normalize / render / simplify / inverse を内部処理として提供

### joo_glyph_fonts / joo_website_glyph_fonts
- MJ/GJ フォントを backend / website に登録  
- `.joo-font` によるフォント指定

### joo_contacts_jp（アプリケーション）
- Contacts に依存するアプリケーション  
- 上記モジュールをまとめて読み込む  
- デモデータを含む  
- アプリ一覧で検索可能（application: True）

---

## 3. デモデータ（demo.xml）

### 異体字を含む住所の例
- `{MJ022335}` を含む住所の入力例  
- GlyphTag → IVS の変換を確認できる

### 変体仮名を含む建物名の例
- `𛀆𛀁𛀀荘` の入力例  
- Unicode の変体仮名をそのまま利用

### ふりがな付き顧客
- 氏名の読みを入力し、検索できる例

---

## 4. インストール手順

### Python パッケージ
```
pip3 install -r requirements.txt
pip3 install -r requirements.tofurengo.txt
```

### アドオン配置
`joo-glyphtag-addons/` を Odoo の addons パスに追加します。

### モジュールのインストール順
1. Contacts  
2. joo_glyph_fonts  
3. joo_tofurengo  
4. joo_partner_furigana  
5. joo_partner_glyphtag  
6. joo_website_glyph_fonts（必要に応じて）  
7. joo_contacts_jp

---

## 5. 利用できる機能

- 氏名の読みを入力し、読みで検索できる  
- 氏名・住所に異体字を含めても表示できる  
- GlyphTag を使って拡張漢字を指定できる  
- Contacts の画面で日本語向けの入力・検索・表示が可能になる

---

## 6. 組み込まれているフォントについて

本アドオンには、IVS を表示するために以下のフォントが含まれています。  
配布元が公開しているライセンスに基づいて利用しています。

### IPAmj明朝
- ファイル名：`ipamjm.ttf`  
- 配布元：独立行政法人 情報処理推進機構（IPA）  
- 配布ページ：https://moji.or.jp/mojikiban/font/  
- ライセンス：IPAフォントライセンス v1.0

### DWPI明朝
- ファイル名：`DWPIMincho.ttf`  
- 配布元：一般社団法人 デジタル広域推進機構（DWPI）  
- 配布ページ：https://www.digitalwidearea.org/dwpi_mincho  
- ライセンス：IPAフォントライセンス v1.0

### DWPIex明朝
- ファイル名：`DWPIexMincho.ttf`  
- 配布元：一般社団法人 デジタル広域推進機構（DWPI）  
- 配布ページ：https://www.digitalwidearea.org/dwpi_mincho  
- ライセンス：IPAフォントライセンス v1.0

### ライセンスについて
- 上記フォントはすべて IPAフォントライセンス v1.0 に基づいて利用しています。  
- 著作権は各フォントの提供元に帰属します。  
- 本アドオンはライセンス条件に従いフォントを同梱しています。

---

## 7. ライセンス・作者

- ライセンス：LGPL-3  
- 作者：jp-one  
- GitHub：https://github.com/jp-one
