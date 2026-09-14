# joo-tofurengo-addons

## モジュール構成

joo_tofurengoとjoo_glyph_fontsとは、独立。
joo_partner_tofurengoは、joo_tofurengoとjoo_glyph_fontsに依存。

```
joo-tofurengo-addons/
├── joo_tofurengo/  # 異体字変換・テキスト処理エンジン
├── joo_glyph_fonts/          # Webフォント配信 & CSSセレクター定義
└── joo_partner_tofurengo/  # 取引先（res.partner）統合
```


### joo_tofurengo

* tofurengoによる正規化、描画、簡素化
* グリフデータセットの設定変更


### joo_glyph_fonts

* MJ+文字フォント対応（IPAmjMincho, DWPIMincho, DWPIexMIncho）
* フォントのweb配布
* font-faceの定義
* 選定変更可能なfont-face


### joo_partner_tofurengo

* 氏名の分割対応
* name の氏名区切り文字の正規化（asciiスペース文字化）
* name での Glyph-Tag 入力が可能
* 検索・表示用の氏名対応
* 氏名のIVS対応（出力）
* ふりがなの入力（うじ・な）
* 住所（city, street, street2）でのGlyph-Tag入力が可能
* 検索・表示用の住所対応
* 住所のIVS対応（出力）


## pythonパッケージ

### tofurengo
tofurengo Pythonパッケージをgithubからインストール
requirements.txt に追記
※ --index-urlを利用しているので後続のインストールに注意する。

```txt:requirements.txt
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

