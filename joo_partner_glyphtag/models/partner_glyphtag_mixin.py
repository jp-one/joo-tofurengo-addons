import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PartnerGlyphtagMixin(models.AbstractModel):
    _name = "joo.partner.glyphtag.mixin"
    _inherit = ['mail.thread']
    _description = "Partner GlyphTag Mixin"

    # ---------------------------------------------------------
    # Field Mapping Sets
    # ---------------------------------------------------------
    BASE_FIELDS = ["name", "street", "street2", "city"]

    # ---------------------------------------------------------
    # Input Fields
    # ---------------------------------------------------------
    use_glyphtag = fields.Boolean("Use GlyphTag", tracking=True)

    name_glyphtag = fields.Char("Name (GlyphTag)", tracking=True)
    street_glyphtag = fields.Char("Street (GlyphTag)", tracking=True)
    street2_glyphtag = fields.Char("Street2 (GlyphTag)", tracking=True)
    city_glyphtag = fields.Char("City (GlyphTag)", tracking=True)

    # ---------------------------------------------------------
    # Computed Glyph Fields (Stored)
    # ---------------------------------------------------------
    name_glyph = fields.Char(
        string="Name (Glyph)",
        compute="_compute_name_glyph",
        store=True,
    )
    street_glyph = fields.Char(
        string="Street (Glyph)",
        compute="_compute_street_glyph",
        store=True,
    )
    street2_glyph = fields.Char(
        string="Street2 (Glyph)",
        compute="_compute_street2_glyph",
        store=True,
    )
    city_glyph = fields.Char(
        string="City (Glyph)",
        compute="_compute_city_glyph",
        store=True,
    )

    # ---------------------------------------------------------
    # Effective Fields for View/Report (Non-Stored)
    # ---------------------------------------------------------
    name_effective = fields.Char(
        string="Name (Effective)",
        compute="_compute_name_effective",
        store=False,
    )
    street_effective = fields.Char(
        string="Street (Effective)",
        compute="_compute_street_effective",
        store=False,
    )
    street2_effective = fields.Char(
        string="Street2 (Effective)",
        compute="_compute_street2_effective",
        store=False,
    )
    city_effective = fields.Char(
        string="City (Effective)",
        compute="_compute_city_effective",
        store=False,
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _sanitize_spaces(self, text: str) -> str:
        """Replace full-width spaces with standard spaces and normalize consecutive whitespace."""
        if not text:
            return ""
        text = text.replace("\u3000", "\u0020").strip()
        return re.sub(r"\s+", "\u0020", text)

    def _render(self, text: str, use_base: bool = False) -> str:
        """Render normal/glyph text using the Glyph service."""
        if not text:
            return ""
        svc = self.env["joo_tofurengo.glyph_service"].sudo()
        result = svc.normalize(text)
        return svc.render(result.text, use_base=use_base) or ""

    def _simplify(self, text: str) -> str:
        """Simplify text using the Glyph service."""
        if not text:
            return ""
        svc = self.env["joo_tofurengo.glyph_service"].sudo()
        return svc.simplify(text) or ""

    def _inverse(self, text: str) -> str:
        """Convert standard text back into GlyphTag format."""
        if not text:
            return ""
        svc = self.env["joo_tofurengo.glyph_service"].sudo()
        return svc.inverse(text) or ""

    # ---------------------------------------------------------
    # Compute Methods (Glyph - Stored)
    # ---------------------------------------------------------
    def _compute_single_glyph(self, base_field: str):
        """Helper to compute glyph value for a specific base field."""
        tag_field = f"{base_field}_glyphtag"
        glyph_field = f"{base_field}_glyph"
        for rec in self:
            tag_val = getattr(rec, tag_field) or ""
            glyph_val = rec._render(tag_val, use_base=False)
            setattr(rec, glyph_field, glyph_val)

    # Note: use_glyphtag is omitted from depends to avoid re-computations of *_glyph on toggle
    @api.depends("name_glyphtag")
    def _compute_name_glyph(self):
        self._compute_single_glyph("name")

    @api.depends("street_glyphtag")
    def _compute_street_glyph(self):
        self._compute_single_glyph("street")

    @api.depends("street2_glyphtag")
    def _compute_street2_glyph(self):
        self._compute_single_glyph("street2")

    @api.depends("city_glyphtag")
    def _compute_city_glyph(self):
        self._compute_single_glyph("city")

    # ---------------------------------------------------------
    # Compute Methods (Effective - Non-stored)
    # ---------------------------------------------------------
    def _compute_single_effective(self, base_field: str):
        """Helper to compute effective value based on use_glyphtag status."""
        glyph_field = f"{base_field}_glyph"
        effective_field = f"{base_field}_effective"
        for rec in self:
            if rec.use_glyphtag:
                val = getattr(rec, glyph_field) or ""
            else:
                val = getattr(rec, base_field) or ""
            setattr(rec, effective_field, val)

    @api.depends("use_glyphtag", "name_glyph", "name")
    def _compute_name_effective(self):
        self._compute_single_effective("name")

    @api.depends("use_glyphtag", "street_glyph", "street")
    def _compute_street_effective(self):
        self._compute_single_effective("street")

    @api.depends("use_glyphtag", "street2_glyph", "street2")
    def _compute_street2_effective(self):
        self._compute_single_effective("street2")

    @api.depends("use_glyphtag", "city_glyph", "city")
    def _compute_city_effective(self):
        self._compute_single_effective("city")

    # ---------------------------------------------------------
    # Onchange Handlers
    # ---------------------------------------------------------
    def _process_glyphtag_field_change(self, base_field: str):
        """Process changes when a specific GlyphTag field or use_glyphtag is updated."""
        if self.use_glyphtag:
            tag_field = f"{base_field}_glyphtag"
            tag_val = getattr(self, tag_field)
            tag_val = self._simplify(tag_val)
            tag_val = self._sanitize_spaces(tag_val)
            setattr(self, tag_field, tag_val)
            base_val = self._render(tag_val, use_base=True)
            setattr(self, base_field, base_val)

    @api.onchange("name_glyphtag")
    def _onchange_name_glyphtag(self):
        self._process_glyphtag_field_change("name")

    @api.onchange("street_glyphtag")
    def _onchange_street_glyphtag(self):
        self._process_glyphtag_field_change("street")

    @api.onchange("street2_glyphtag")
    def _onchange_street2_glyphtag(self):
        self._process_glyphtag_field_change("street2")

    @api.onchange("city_glyphtag")
    def _onchange_city_glyphtag(self):
        self._process_glyphtag_field_change("city")

    def _process_base_field_change(self, base_field: str):
        """Process changes when a specific base field or use_glyphtag is updated."""
        if not self.use_glyphtag:
            text = getattr(self, base_field)
            text = self._sanitize_spaces(text)
            setattr(self, base_field, text)

    @api.onchange("name")
    def _onchange_name(self):
        self._process_base_field_change("name")

    @api.onchange("street")
    def _onchange_street(self):
        self._process_base_field_change("street")

    @api.onchange("street2")
    def _onchange_street2(self):
        self._process_base_field_change("street2")

    @api.onchange("city")
    def _onchange_city(self):
        self._process_base_field_change("city")

    @api.onchange("use_glyphtag")
    def _onchange_use_glyphtag(self):
        if self.use_glyphtag:
            for base_field in self.BASE_FIELDS:
                tag_field = f"{base_field}_glyphtag"
                tag_val = getattr(self, tag_field)
                if not tag_val:
                    base_val = getattr(self, base_field)
                    base_val = self._sanitize_spaces(base_val)
                    tag_val = self._inverse(base_val)
                    setattr(self, tag_field, tag_val)

    # ---------------------------------------------------------
    # Validations & Syncing Logic
    # ---------------------------------------------------------
    @api.constrains("name_glyphtag", "street_glyphtag", "street2_glyphtag", "city_glyphtag")
    def _check_glyphtag_fields(self):
        """Validate format for all GlyphTag fields."""
        svc = self.env["joo_tofurengo.glyph_service"].sudo()
        for rec in self:
            for base_field in self.BASE_FIELDS:
                tag_field = f"{base_field}_glyphtag"
                tag_val = getattr(rec, tag_field)
                if tag_val:
                    result = svc.normalize(tag_val)
                    if not getattr(result, "success", False):
                        field_description = self._fields[tag_field].string
                        raise ValidationError(
                            _(
                                "Invalid GlyphTag format in '%s'.",
                                field_description,
                            )
                        )

    def _sync_glyphtag_payload(self, record, vals):
        """Detect modified fields in 'vals' and execute synchronization logic."""
        tag_fields = [f"{f}_glyphtag" for f in self.BASE_FIELDS]
        target_fields = set(["use_glyphtag"] + self.BASE_FIELDS + tag_fields)

        # Skip execution if no relevant fields are present in vals
        if not any(k in vals for k in target_fields):
            return

        use_tag = vals.get("use_glyphtag", record.use_glyphtag if record else False)

        for base_field in self.BASE_FIELDS:
            tag_field = f"{base_field}_glyphtag"

            # Check if this specific field requires processing (or if use_glyphtag changed)
            is_modified = ("use_glyphtag" in vals) or (base_field in vals) or (tag_field in vals)
            if not is_modified:
                continue

            if use_tag:
                current_tag_val = record[tag_field] if record else ""
                tag_val = vals.get(tag_field, current_tag_val)
                tag_val = self._sanitize_spaces(tag_val)
                base_val = self._render(tag_val, use_base=True)
                vals[base_field] = base_val
                vals[tag_field] = tag_val
            else:
                current_base_val = record[base_field] if record else ""
                base_val = vals.get(base_field, current_base_val) or ""
                base_val = self._sanitize_spaces(base_val)
                tag_val = self._inverse(base_val)
                vals[base_field] = base_val
                vals[tag_field] = tag_val
