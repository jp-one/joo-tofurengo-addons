# Contacts(res.partner)のビュー
repos/odoo/odoo/addons/base/views/res_partner_views.xml

結論から言うと、あなたが貼ってくれた巨大 XML は **Odoo19 の res.partner に関するすべてのビュー（list / kanban / form / simple form / address form / search view / actions）を完全に網羅した公式構成**になっている。  
そこで、開発者が使いやすいように **ビュー構成を役割別にまとめた「全体マップ」**を作った。  
このマップを見れば、どこを継承すればよいか一瞬で判断できる。

---

# 📘 **Odoo19 res.partner ビュー構成まとめ（完全版）**

---

## 🟦 **1. Tree（List）ビュー**
### **ID: `view_partner_tree`**
用途：一覧表示（multi_edit 対応）

主なフィールド：
- avatar_128（画像）
- display_name / complete_name
- email / phone
- address（street, city, state, country）
- category_id（タグ）
- application_statistics（統計）
- company_id（マルチカンパニー）

---

## 🟩 **2. Simplified Form（簡易フォーム）**
### **ID: `view_partner_simple_form`**
用途：最小限の情報でコンタクト作成

構成：
- 画像
- name（会社/個人で placeholder 切替）
- parent_id（会社選択）
- email / phone / function

---

## 🟧 **3. Address Form（住所専用フォーム）**
### **ID: `view_partner_address_form`**
用途：住所だけ編集する軽量フォーム

構成：
- name（readonly）
- street / street2 / city / state / zip / country
- website

---

## 🟥 **4. Full Form（メインフォーム）**
### **ID: `view_partner_form`**
用途：Odoo の標準「Contacts」画面

構成（大きく 5 ブロック）：

### 4.1 ヘッダー
- image_1920（contact_image）
- company_type（radio）
- name（会社/個人で placeholder 切替）
- email / phone

### 4.2 会社情報
- parent_id（会社）
- company_name（会社名の簡易作成）
- type_address_label（住所ラベル）
- 住所（street, city, state, zip, country）

### 4.3 基本情報
- function
- vat
- website
- lang
- category_id（タグ）

### 4.4 プロパティ
- properties（dynamic properties）

### 4.5 Notebook（タブ）
#### Contacts（子住所）
- child_ids（kanban + form）

#### Sales & Purchase
- user_id（営業担当）
- company_registry
- ref
- industry_id

#### Notes
- comment
- warnings

---

## 🟪 **5. Search View（検索ビュー）**
### **ID: `view_res_partner_filter`**
用途：検索パネル

フィルタ：
- name（display_name ilike）
- parent_id（child_of）
- email / phone
- category_id（child_of）
- user_id
- Persons / Companies
- Archived
- group_by（user_id / parent_id / country_id / properties）

---

## 🟫 **6. Kanban View（カードビュー）**
### **ID: `res_partner_kanban_view`**
用途：カード表示

構成：
- avatar_128（会社/個人で表示切替）
- display_name
- email / phone
- city, country
- properties
- application_statistics

---

## 🟨 **7. Actions（メニューアクション）**
### **顧客（Customers）**
- `action_partner_form`
- list / kanban / form

### **顧客（eCommerce Customers）**
- `action_partner_customer_form`

### **仕入先（Vendors）**
- `action_partner_supplier_form`

---

## 🟪 **8. Tags（res.partner.category）**
### List / Form / Search / Action  
ID:
- `view_partner_category_form`
- `view_partner_category_list`
- `res_partner_category_view_search`
- `action_partner_category_form`

---

## 🟦 **9. Industry（res.partner.industry）**
### List / Form / Search / Action  
ID:
- `res_partner_industry_view_form`
- `res_partner_industry_view_tree`
- `res_partner_industry_view_search`
- `res_partner_industry_action`

---

# 🧩 **あなたがカスタムする時のポイント（Odoo19対応）**

### ✔ どのビューを継承すべきか一瞬で判断できる
- **一覧を変えたい → `view_partner_tree`**
- **メインフォームを変えたい → `view_partner_form`**
- **住所だけ変えたい → `view_partner_address_form`**
- **簡易フォームを変えたい → `view_partner_simple_form`**
- **検索条件を変えたい → `view_res_partner_filter`**
- **Kanban を変えたい → `res_partner_kanban_view`**

### ✔ Odoo19 の RelaxNG ルール
- `<record>` は必ず `<data>` 内
- `<arch>` は `<field name="arch" type="xml">`
- `<field>` タグ以外で name/model を書かない

あなたの XML はすべてこのルールに適合している。

---

# 📦 **まとめて 1 ファイルに統合したい？**
もし目的が「ビューを 1 ファイルにまとめたい」なら、  
あなたの XML はすでに **1 ファイルに完全統合済み**。

ただし、開発効率のためには：

- `views/partner_form.xml`
- `views/partner_tree.xml`
- `views/partner_kanban.xml`
- `views/partner_search.xml`
- `views/partner_actions.xml`
- `views/partner_category.xml`
- `views/partner_industry.xml`

のように **分割した方が Odoo19 では管理しやすい**。

---

# 🔥 次にどうする？
あなたの目的はどっち？

### ① **ビューを分割したい（推奨）**  
→ 分割用の XML ファイル構成を作る

### ② **ビューをカスタムしたい**  
→ どのビューをどう変更したいか教えてくれれば、  
Odoo19 RelaxNG 完全対応の継承 XML を書く。

どちらに進める？


了解。  
あなたが求めているのは **「Odoo19 の各ビューが、どの画面・どのアクションから呼び出されるのか」**  
つまり **ビューの呼び出しルート（画面遷移マップ）** だね。

Odoo のビューは  
- **アクション（ir.actions.act_window）**  
- **ビュータイプ（tree / form / kanban / search）**  
- **ビューの優先度（priority）**  
で決まる。

あなたが貼った XML は巨大だけど、呼び出しルートは整理すると非常にシンプルになる。

---

# 🔵 **Odoo19 res.partner ビュー呼び出しマップ（完全版）**

---

## ① **一覧画面（List / Tree）**
### 呼び出し元
- メニュー：**Contacts → Customers / Vendors / Contacts**
- アクション：`action_partner_form` / `action_partner_supplier_form` / `action_partner_customer_form`

### 使用ビュー
- **`view_partner_tree`**（list）

### 仕組み
アクションの `view_mode="tree,form"` により  
最初に **tree** が表示される。

---

## ② **メインフォーム（Full Form）**
### 呼び出し元
- 一覧からレコードをクリック
- Kanban からクリック
- 検索ビューから選択

### 使用ビュー
- **`view_partner_form`**（form）

### 仕組み
アクションの `view_mode="tree,form"` の **form** が使われる。  
priority=1 のため、他の form より優先される。

---

## ③ **簡易フォーム（Simplified Form）**
### 呼び出し元
- 一部のウィザード
- 外部モジュール（CRMなど）が「簡易作成」を呼ぶ場合

### 使用ビュー
- **`view_partner_simple_form`**

### 仕組み
`context={'default_view_id': 'view_partner_simple_form'}`  
などで明示的に指定されたときのみ呼ばれる。

---

## ④ **住所専用フォーム（Address Form）**
### 呼び出し元
- 子住所（child_ids）を編集するとき
- 「Open Address」アクション

### 使用ビュー
- **`view_partner_address_form`**

### 仕組み
子レコード（type != contact）を開くと  
Odoo が自動的に address 用フォームを選択する。

---

## ⑤ **Kanban（カードビュー）**
### 呼び出し元
- メニュー：Contacts → Kanban 切り替え
- アクション：`action_partner_form`（view_mode に kanban が含まれる場合）

### 使用ビュー
- **`res_partner_kanban_view`**

### 仕組み
アクションの `view_mode="kanban,tree,form"` の場合  
最初に kanban が表示される。

---

## ⑥ **検索ビュー（Search）**
### 呼び出し元
- 一覧画面の検索バー

### 使用ビュー
- **`view_res_partner_filter`**

### 仕組み
アクションの `search_view_id="view_res_partner_filter"` により  
検索パネルがこのビューになる。

---

# 🔶 **ビュー呼び出しの全体図（視覚的マップ）**

```
Menu → Action → ViewMode → View
-----------------------------------------
Contacts → action_partner_form
    → tree → view_partner_tree
    → form → view_partner_form
    → kanban → res_partner_kanban_view
    → search → view_res_partner_filter

child_ids (address)
    → form → view_partner_address_form

simple create (外部モジュール)
    → form → view_partner_simple_form
```

---

# 🔧 **Odoo がビューを選択する優先順位**

1. **アクションの view_mode**
2. **ビューの model が一致**
3. **ビュータイプ（tree / form / kanban / search）**
4. **priority が低いほど優先**
5. **context に default_view_id があればそれを最優先**

あなたの XML はこのルールに完全準拠している。

---

# 🔥 次にどうする？
あなたの目的はどれ？

### A. **どのビューを継承すべきか知りたい**  
→ 変更したい画面を教えてくれれば、  
そのビューの継承 XML を Odoo19 RelaxNG 100%対応で書く。

### B. **ビューの呼び出し順をカスタムしたい**  
→ アクションの view_mode を調整する。

### C. **ビューを分割したい**  
→ 分割用の XML ファイル構成を作る。

どれを進める？

