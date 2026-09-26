# joo-glyphtag-addons

Odoo Contacts に日本語の氏名・住所を扱うための機能を追加するアドオン群です。  
ふりがな、GlyphTag、異体字正規化、IVS 表示、フォント設定をまとめて提供します。  
`joo_contacts_jp` はこれらを統合したアプリケーションです。

この `joo_contacts_jp` アプリケーションをインストールすることにより、  
MJ文字や行政事務標準文字を扱うことができます。

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
- res.partner への `furigana` フィールド追加  
- 氏名の読み入力（ひらがな／カタカナ）  
- 読みによる検索  
- ひらがな／カタカナ／スペース統一の正規化設定  

### joo_partner_glyphtag
- 氏名・住所の GlyphTag 入力フィールド追加  
- GlyphTag から IVS への変換表示  
- 通常文字列と GlyphTag の同期  
- 氏名・住所の編集用ダイアログ提供  

### joo_tofurengo
- GlyphTag の正規化処理  
- MJ/GJ データセットの切り替え  
- normalize / render / simplify / inverse の内部処理提供  

### joo_glyph_fonts / joo_website_glyph_fonts
- MJ/GJ フォントの backend / website への登録  
- 固定フォント指定用クラスの提供（`.joo-font--DWPIexMincho` など）  
- `.joo-font` クラスを指定した要素へのフォント適用（Odoo 設定画面で選択されたフォントの適用）  

### joo_contacts_jp（アプリケーション）
- Contacts への依存  
- 各モジュールの統合読み込み  
- デモデータの提供  
- アプリ一覧での検索対象化（application: True）  

---

## 3. GlyphTag の使用例

GlyphTag を使用することで、異体字を含む氏名や住所を入力できます。

### 東京都 葛飾区
{% raw %}
```
{{MJ022336}東京都{MJ022336}飾区
とうきょうと かつしかく

東京都
{MJ022336}飾区
```
{% endraw %}

### 奈良県 葛城市
```text
{% raw %}
{{MJ022335}奈良県{MJ022335}城市
ならけん かつらぎし

奈良県
{MJ022335}城市
{% endraw %}
```

---

## 4. フォント指定の例

Odoo のフィールドに CSS クラスを付与することで、フォントを指定できます。

### 共通フォント指定（Odoo 設定画面で選択されたフォントを適用）
```xml
<field name="name" class="joo-font"/>
```

### 固定フォント指定
```xml
<field name="street" class="joo-font--DWPIexMincho"/>
<field name="city" class="joo-font--DWPIMincho"/>
<field name="state_id" class="joo-font--IPAmjMincho"/>
```

---

## 5. インストール手順

Python パッケージをインストールしたあと、  
`joo-glyphtag-addons/` を Odoo の addons パスに追加してください。

### Python パッケージ
```
pip3 install -r requirements.txt
pip3 install -r requirements.tofurengo.txt
```

### モジュールのインストール
`joo_contacts_jp` をインストールします。

---

## 6. 同梱されているフォントについて

MJ文字や行政事務標準文字を表示するために、次のフォントを同梱しています。  
フォルダ: `joo-glyphtag-addons/joo_glyph_fonts/static/src/fonts`  

### 1. IPAmj明朝
* **ファイル**: `ipamjm.ttf`  
* **取得元**: [IPAmj明朝フォント ダウンロード | 文字情報技術促進協議会](https://moji.or.jp/mojikiban/font/)  
* **権利者**: 独立行政法人情報処理推進機構（IPA）  
* **説明**: 戸籍・住民基本台帳等で用いられる文字（MJ文字）を収録した標準明朝体フォントです。

### 2. DWPI明朝
* **ファイル**: `DWPIMincho.ttf`  
* **配布・権利元**: [一般社団法人デジタル広域推進機構（DWPI_mincho）](https://www.digitalwidearea.org/dwpi_mincho)  
* **説明**: IPAmj明朝をベースに、国が整備する「行政事務標準文字」を実装した派生フォントです。

### 3. DWPIex明朝
* **ファイル**: `DWPIexMincho.ttf`  
* **配布・権利元**: [一般社団法人デジタル広域推進機構（DWPI_mincho）](https://www.digitalwidearea.org/dwpi_mincho)  
* **説明**: 行政事務標準文字の実装用フォント「DWPI明朝」をベースに、拡張文字やデフォルトグリフの調整が行われたフォントです。

---

### フォントファイルのライセンス・著作権について

同梱されているすべてのフォントファイルの著作権は、それぞれの提供元に帰属します。

* **IPAmj明朝**: 独立行政法人情報処理推進機構（IPA）の著作物です。  
* **DWPI明朝 / DWPIex明朝**: 著作権は一般社団法人デジタル広域推進機構 等に帰属します。

なお、DWPI明朝およびDWPIex明朝は IPAmj明朝の派生フォントであるため、  
すべてのフォントにおいて **IPAフォントライセンス v1.0** に基づいて利用・配布されています。

---

## 7. ライセンス・作者

本アドオンは LGPL-3 ライセンスで提供しています。  
作者は jp-one です。  
GitHub：https://github.com/jp-one
