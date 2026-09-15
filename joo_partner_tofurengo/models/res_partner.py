from odoo import models, fields, api


class ResPartner(models.Model):
    """
    Extends res.partner to support:
      - Split names (family_name, given_name) derived automatically from 'name'
      - Furigana inputs (family_name_kana, given_name_kana)
      - Space delimiter normalization and split logic
      - Individual IVS output fields (*_ivs) for name and address components
      - Individual search-optimized fields (*_search) for name and address components
    """
    _inherit = 'res.partner'

    # --- Furigana Fields ---
    family_name_kana = fields.Char(
        string="Family Name Kana",
        help="Furigana for Family Name (Uji)."
    )
    given_name_kana = fields.Char(
        string="Given Name Kana",
        help="Furigana for Given Name (Na)."
    )

    # --- Name Derived Fields ---
    family_name = fields.Char(
        string="Family Name",
        compute="_compute_glyph_outputs",
        store=True,
        help="Family Name (Uji) extracted from 'name'."
    )
    given_name = fields.Char(
        string="Given Name",
        compute="_compute_glyph_outputs",
        store=True,
        help="Given Name (Na) extracted from 'name'."
    )

    # --- Name IVS Output Fields ---
    family_name_ivs = fields.Char(
        string="Family Name (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        help="Family Name rendered with Unicode IVS sequences."
    )
    given_name_ivs = fields.Char(
        string="Given Name (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        help="Given Name rendered with Unicode IVS sequences."
    )

    # --- Name Search Fields ---
    family_name_search = fields.Char(
        string="Family Name (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        index=True,
        help="Simplified Family Name with glyph tags stripped for searching."
    )
    given_name_search = fields.Char(
        string="Given Name (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        index=True,
        help="Simplified Given Name with glyph tags stripped for searching."
    )

    # --- Address IVS Output Fields ---
    city_ivs = fields.Char(
        string="City (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        help="City rendered with Unicode IVS sequences."
    )
    street_ivs = fields.Char(
        string="Street (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        help="Street rendered with Unicode IVS sequences."
    )
    street2_ivs = fields.Char(
        string="Street2 (IVS)",
        compute="_compute_glyph_outputs",
        store=True,
        help="Street2 rendered with Unicode IVS sequences."
    )

    # --- Address Search Fields ---
    city_search = fields.Char(
        string="City (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        index=True,
        help="Simplified City with glyph tags stripped for searching."
    )
    street_search = fields.Char(
        string="Street (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        index=True,
        help="Simplified Street with glyph tags stripped for searching."
    )
    street2_search = fields.Char(
        string="Street2 (Search)",
        compute="_compute_glyph_outputs",
        store=True,
        index=True,
        help="Simplified Street2 with glyph tags stripped for searching."
    )

    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    def _get_glyph_service(self):
        """
        Retrieves joo_tofurengo.glyph_service if installed in the environment.
        """
        if 'joo_tofurengo.glyph_service' in self.env:
            return self.env['joo_tofurengo.glyph_service']
        return None

    def _normalize_delimiter(self, text: str) -> str:
        """
        Normalizes full-width spaces (U+3000) and redundant whitespace to a single ASCII space.
        """
        if not text:
            return ""
        cleaned = text.replace('\u3000', ' ')
        return " ".join(cleaned.split())

    def _split_full_name(self, name_str: str):
        """
        Splits full name by space into (family_name, given_name).
        """
        normalized = self._normalize_delimiter(name_str)
        if not normalized:
            return ("", "")
        parts = normalized.split(' ', 1)
        if len(parts) == 2:
            return (parts[0], parts[1])
        return (parts[0], "")

    def _process_text_field(self, raw_text: str, service):
        """
        Normalizes, renders IVS, and simplifies a single text field.
        Returns a tuple of (normalized_raw, ivs_output, search_output).
        """
        cleaned = self._normalize_delimiter(raw_text)
        if not cleaned:
            return ("", "", "")

        if service:
            norm_res = service.normalize(cleaned)
            norm_text = norm_res.normalized_text if hasattr(norm_res, 'normalized_text') else str(norm_res)
            ivs_text = service.render(norm_text)
            search_text = service.simplify(norm_text)
            return (norm_text, ivs_text, search_text)

        return (cleaned, cleaned, cleaned)

    # -------------------------------------------------------------------------
    # Compute Methods
    # -------------------------------------------------------------------------
    @api.depends('name', 'city', 'street', 'street2')
    def _compute_glyph_outputs(self):
        """
        Triggers automatically when 'name', 'city', 'street', or 'street2' changes.
        Splits 'name' into family_name and given_name, then processes IVS and Search fields.
        """
        svc = self._get_glyph_service()

        for record in self:
            # 1. Split 'name' into family_name and given_name
            fam_raw, giv_raw = self._split_full_name(record.name)

            # 2. Process Name Fields (Normalize -> IVS -> Search)
            record.family_name, record.family_name_ivs, record.family_name_search = self._process_text_field(fam_raw, svc)
            record.given_name, record.given_name_ivs, record.given_name_search = self._process_text_field(giv_raw, svc)

            # 3. Process Address Fields
            _, record.city_ivs, record.city_search = self._process_text_field(record.city, svc)
            _, record.street_ivs, record.street_search = self._process_text_field(record.street, svc)
            _, record.street2_ivs, record.street2_search = self._process_text_field(record.street2, svc)
