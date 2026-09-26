[GitHub Pages (Japanese)](./README.ja.html)

# joo-glyphtag-addons

This is a collection of Odoo add-ons that extend the Contacts application to properly handle Japanese names and addresses.  
It provides furigana input, GlyphTag processing, variant character normalization, IVS rendering, and font configuration.  
The `joo_contacts_jp` module integrates all of these features into a single application.

By installing the `joo_contacts_jp` application, you can work with MJ characters and the Administrative Standard Characters used in Japanese government systems.

---

## 1. Module Structure

```
joo_partner_furigana       Furigana input and search for partner names
joo_partner_glyphtag       GlyphTag input and IVS rendering
joo_tofurengo              GlyphTag normalization engine
joo_glyph_fonts            MJ/GJ fonts (backend)
joo_website_glyph_fonts    MJ/GJ fonts (website)
joo_contacts_jp            Japanese extension for Odoo Contacts
```

---

## 2. Features of Each Module

### joo_partner_furigana
- Adds a `furigana` field to `res.partner`  
- Allows input of name readings (hiragana / katakana)  
- Enables searching by reading  
- Provides normalization settings for hiragana, katakana, and spacing  

### joo_partner_glyphtag
- Adds GlyphTag input fields for names and addresses  
- Converts GlyphTag to IVS for display  
- Synchronizes normal text and GlyphTag  
- Provides editing dialogs for name and address fields  

### joo_tofurengo
- Performs normalization of GlyphTag  
- Allows switching between MJ and GJ datasets  
- Provides internal operations: normalize / render / simplify / inverse  

### joo_glyph_fonts / joo_website_glyph_fonts
- Registers MJ/GJ fonts for backend and website  
- Provides fixed-font CSS classes (e.g., `.joo-font--DWPIexMincho`)  
- Applies fonts to elements using the `.joo-font` class (based on the font selected in Odoo settings)  

### joo_contacts_jp (Application)
- Depends on Odoo Contacts  
- Loads all related modules  
- Provides demo data  
- Appears in the Apps list (application: True)  

---

## 3. Examples of GlyphTag Usage

Using GlyphTag allows you to input names and addresses containing variant characters.

### Katsushika-ku, Tokyo
{% raw %}
```text
{{MJ022336}東京都{MJ022336}飾区
とうきょうと かつしかく

東京都
{MJ022336}飾区
```
{% endraw %}

### Katsuragi-shi, Nara
```text
{% raw %}
{{MJ022335}奈良県{MJ022335}城市
ならけん かつらぎし

奈良県
{MJ022335}城市
{% endraw %}
```

---

## 4. Font Assignment Examples

You can assign fonts by adding CSS classes to Odoo fields.

### Common Font Assignment (uses the font selected in Odoo Settings)
```xml
<field name="name" class="joo-font"/>
```

### Fixed Font Assignment
```xml
<field name="street" class="joo-font--DWPIexMincho"/>
<field name="city" class="joo-font--DWPIMincho"/>
<field name="state_id" class="joo-font--IPAmjMincho"/>
```

---

## 5. Installation

After installing the required Python packages,  
please add `joo-glyphtag-addons/` to your Odoo addons path.

### Python Packages
```
pip3 install -r requirements.txt
pip3 install -r requirements.tofurengo.txt
```

### Module Installation
Install the `joo_contacts_jp` module.

---

## 6. Included Fonts

To display MJ characters and Administrative Standard Characters, the following fonts are bundled.  
Folder: `joo-glyphtag-addons/joo_glyph_fonts/static/src/fonts`

### 1. IPAmj Mincho
* **File**: `ipamjm.ttf`  
* **Source**: [IPAmj Mincho Download | Moji Technical Council](https://moji.or.jp/mojikiban/font/)  
* **Rights Holder**: Information-technology Promotion Agency, Japan (IPA)  
* **Description**: A standard Mincho font containing MJ characters used in family registers and resident records.

### 2. DWPI Mincho
* **File**: `DWPIMincho.ttf`  
* **Distribution / Rights**: [Digital Wide-area Promotion Institute (DWPI_mincho)](https://www.digitalwidearea.org/dwpi_mincho)  
* **Description**: A derivative font based on IPAmj Mincho, implementing the Administrative Standard Characters defined by the Japanese government.

### 3. DWPIex Mincho
* **File**: `DWPIexMincho.ttf`  
* **Distribution / Rights**: [Digital Wide-area Promotion Institute (DWPI_mincho)](https://www.digitalwidearea.org/dwpi_mincho)  
* **Description**: An extended version of DWPI Mincho, adding additional characters and adjusting default glyphs.

---

### Font License and Copyright

All bundled font files are copyrighted by their respective providers.

* **IPAmj Mincho**: Copyright (c) IPA  
* **DWPI Mincho / DWPIex Mincho**: Copyright (c) Digital Wide-area Promotion Institute

Since DWPI Mincho and DWPIex Mincho are derivative works of IPAmj Mincho,  
all fonts are distributed under the **IPA Font License v1.0**.

---

## 7. License & Author

This add-on is provided under the LGPL-3 license.  
Author: jp-one  
GitHub: [https://github.com/jp-one](https://github.com/jp-one)
