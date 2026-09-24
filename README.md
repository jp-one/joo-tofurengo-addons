# joo-glyphtag-addons

## モジュール構成

joo_glyph_fonts、joo_tofurengo、joo_partner_furiganaは、独立。
joo_partner_glyphtagは、joo_glyph_fonts、joo_tofurengoに依存。

```
joo-glyphtag-addons/
├── joo_glyph_fonts/        # Webフォント配信 & CSSセレクター定義
├── joo_partner_furigana/   # ふりがな（res.partner）
├── joo_partner_glyphtag/   # GlyphTag（res.partner）
└── joo_tofurengo/          # 異体字変換・テキスト処理エンジン
```

### joo_glyph_fonts

* MJ/GJ文字フォント対応（IPAmjMincho, DWPIMincho, DWPIexMIncho）
* フォントのweb配布
* font-faceの定義
* 選定変更可能なfont-face


### joo_tofurengo

* tofurengoによる正規化、描画、簡素化
* グリフデータセットの設定変更


### joo_partner_furigana

* ふりがなの入力
* ふりがなの検索


### joo_partner_glyphtag

* name の氏名区切り文字の正規化（asciiスペース文字化）
* name での GlyphTag 入力が可能
* 検索・表示用の氏名対応
* 氏名のIVS対応（出力）
* 住所（city, street, street2）でのGlyphTag入力が可能
* 検索・表示用の住所対応
* 住所のIVS対応（出力）


## pythonパッケージ

Pythonパッケージのインストール

```bash
pip3 install -r ./requirements.txt
```

### tofurengo
tofurengo Pythonパッケージをgithubからインストール

```bash
pip3 install -r ./requirements.tofurengo.txt
```

**requirements.tofurengo.txt**

```txt:requirements.tofurengo.txt
# Python dependencies for custom Odoo addons.
# Installed automatically in the Dev Container via:
#     postCreateCommand: pip3 install -r ./custom_addons/requirements.tofurengo.txt

# Use a custom index URL to install Tofurengo packages from a specific repository.
--index-url https://jp-rad.github.io/tofurengo/simple/
tofurengo
tofurengo-data-mj-plus-v4-10
tofurengo-data-mj-plusx-v1-20
tofurengo-data-mj-v6-02-201
tofurengo-data-mj-v6-02-201-onka
```

**インストールの確認**
```bash
pip3 list | grep tofurengo
```


## フォントファイル

joo_glyph_fontsに同梱

joo_glyph_fonts\static\src\fonts
