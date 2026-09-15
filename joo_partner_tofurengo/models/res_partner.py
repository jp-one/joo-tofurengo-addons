import jaconv
from odoo import models, fields, api


class ResPartner(models.Model):
    """
    Extends res.partner to process name and address glyph conversions via the
    joo_tofurengo glyph service. Generates search-optimized and Unicode IVS
    rendered text variants upon name or address updates.
    """
    _inherit = 'res.partner'

    # --- Furigana Fields (Editable & Auto-converted to Hiragana) ---
    family_name_kana = fields.Char(
        string="Family Name Kana",
        help="Furigana for Family Name or Company Name (Automatically converted to Hiragana)."
    )
    given_name_kana = fields.Char(
        string="Given Name Kana",
        help="Furigana for Given Name. Empty for companies (Automatically converted to Hiragana)."
    )

    # --- Name IVS Output Fields (Readonly) ---
    family_name_ivs = fields.Char(
        string="Family Name (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        help="Family Name rendered with Unicode IVS sequences."
    )
    given_name_ivs = fields.Char(
        string="Given Name (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        help="Given Name rendered with Unicode IVS sequences."
    )

    # --- Name Search Fields (Readonly) ---
    family_name_search = fields.Char(
        string="Family Name (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        index=True,
        help="Simplified Family Name with glyph tags stripped for search index."
    )
    given_name_search = fields.Char(
        string="Given Name (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        index=True,
        help="Simplified Given Name with glyph tags stripped for search index."
    )

    # --- Address IVS Output Fields (Readonly) ---
    city_ivs = fields.Char(
        string="City (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        help="City rendered with Unicode IVS sequences."
    )
    street_ivs = fields.Char(
        string="Street (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        help="Street rendered with Unicode IVS sequences."
    )
    street2_ivs = fields.Char(
        string="Street2 (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        help="Street2 rendered with Unicode IVS sequences."
    )

    # --- Address Search Fields (Readonly) ---
    city_search = fields.Char(
        string="City (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        index=True,
        help="Simplified City with glyph tags stripped for search index."
    )
    street_search = fields.Char(
        string="Street (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        index=True,
        help="Simplified Street with glyph tags stripped for search index."
    )
    street2_search = fields.Char(
        string="Street2 (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        readonly=True,
        index=True,
        help="Simplified Street2 with glyph tags stripped for search index."
    )

    # -------------------------------------------------------------------------
    # Overrides
    # -------------------------------------------------------------------------
    @api.depends("family_name_search", "given_name_search", "is_company")
    def _compute_display_name(self):
        for record in self:
            if record.is_company:
                record.display_name = f"{record.family_name_search or ''}{record.given_name_search or ''}"
            else:
                record.display_name = record.family_name_search
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    def _katakana_to_hiragana(self, text: str) -> str:
        """
        Converts full-width and half-width Katakana to Hiragana using jaconv module.
        """
        if not text:
            return ""
        
        zenkaku = jaconv.h2z(text, kana=True)
        hiragana = jaconv.kata2hira(zenkaku)
        return hiragana

    def _get_glyph_service(self):
        """
        Retrieves the joo_tofurengo.glyph_service if installed in the environment.
        """
        if 'joo_tofurengo.glyph_service' in self.env:
            return self.env['joo_tofurengo.glyph_service']
        return None

    def _tofurengo_convert(self, text: str, service):
        """
        Normalizes input text and generates search ('b' / simplify) and IVS ('v' / render) variants.
        Returns tuple: (normalized_text, search_b, ivs_v)
        """
        result = service.normalize(text)
        norm = result.text
        b = service.render(norm, True)
        b = self._normalize_whitespace(b)
        v = service.render(norm)
        v = self._normalize_whitespace(v)
        return (b, v)

    def _normalize_whitespace(self, text: str) -> str:
        """
        Replaces full-width spaces (U+3000) and collapses duplicate whitespace.
        """
        if not text:
            return ""
        cleaned = text.replace('\u3000', ' ')
        return " ".join(cleaned.split())

    def _split_name_part(self, name_str: str):
        """
        Splits a string by space delimiter into a tuple of (family_part, given_part).
        """
        if not name_str:
            return ("", "")
        parts = name_str.split(' ', 1)
        if len(parts) == 2:
            return (parts[0], parts[1])
        return (parts[0], "")

    # -------------------------------------------------------------------------
    # Onchange / Compute Methods
    # -------------------------------------------------------------------------
    @api.onchange('family_name_kana', 'given_name_kana')
    def _onchange_furigana_kana_to_hiragana(self):
        """
        Automatically converts Katakana inputs (including half-width) to Hiragana on UI interaction.
        """
        if self.family_name_kana:
            self.family_name_kana = self._katakana_to_hiragana(
                self.family_name_kana)
        if self.given_name_kana:
            self.given_name_kana = self._katakana_to_hiragana(
                self.given_name_kana)

    @api.depends('name', 'is_company', 'city', 'street', 'street2', 'family_name_kana', 'given_name_kana')
    def _compute_glyph_outputs(self):
        """
        Pipeline execution order:
          1. Normalize & render via tofurengo service.
          2. Assign search 'b' and IVS 'v' values to address fields.
          3. Process 'name':
             - If company: Assign full converted name to family fields, clear given fields.
             - If individual: Split converted name into family and given fields.
          4. Normalize furigana inputs (convert Katakana to Hiragana).
        """
        svc = self._get_glyph_service().sudo()

        for record in self:
            # 1. Process Address Fields
            record.city_search, record.city_ivs = self._tofurengo_convert(
                record.city, svc)
            record.street_search, record.street_ivs = self._tofurengo_convert(
                record.street, svc)
            record.street2_search, record.street2_ivs = self._tofurengo_convert(
                record.street2, svc)

            # 2. Process Name Field via tofurengo
            name_b, name_v = self._tofurengo_convert(record.name, svc)

            if record.is_company:
                # Company: Populate family fields with full name and empty given fields
                record.family_name_search = name_b
                record.family_name_ivs = name_v
                record.given_name_search = ""
                record.given_name_ivs = ""

                # Consolidate furigana into family_name_kana for companies
                if record.family_name_kana or record.given_name_kana:
                    full_kana = self._normalize_whitespace(
                        f"{record.family_name_kana or ''} {record.given_name_kana or ''}"
                    )
                    record.family_name_kana = self._katakana_to_hiragana(
                        full_kana)
                    record.given_name_kana = ""

            else:
                # Individual: Split into family and given name parts
                fam_b, giv_b = self._split_name_part(name_b)
                fam_v, giv_v = self._split_name_part(name_v)

                record.family_name_search = fam_b
                record.family_name_ivs = fam_v
                record.given_name_search = giv_b
                record.given_name_ivs = giv_v

                # Normalize furigana inputs to Hiragana
                if record.family_name_kana:
                    record.family_name_kana = self._katakana_to_hiragana(
                        record.family_name_kana)
                if record.given_name_kana:
                    record.given_name_kana = self._katakana_to_hiragana(
                        record.given_name_kana)

                # Auto-split furigana if provided in a single input string
                if record.family_name_kana and not record.given_name_kana:
                    fam_k, giv_k = self._split_name_part(
                        self._normalize_whitespace(record.family_name_kana))
                    if giv_k:
                        record.family_name_kana = fam_k
                        record.given_name_kana = giv_k
