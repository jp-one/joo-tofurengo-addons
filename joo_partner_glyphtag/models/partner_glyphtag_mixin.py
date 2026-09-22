import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PartnerGlyphtagMixin(models.AbstractModel):
    _name = 'joo.partner.glyphtag.mixin'
    _description = 'Partner GlyphTag Mixin'

    # ---------------------------------------------------------
    # Field Mapping Sets
    # ---------------------------------------------------------
    BASE_FIELDS = ['name', 'street', 'street2', 'city']

    # ---------------------------------------------------------
    # Input Fields
    # ---------------------------------------------------------
    use_glyphtag = fields.Boolean("Use GlyphTag", tracking=True)

    name_glyphtag = fields.Char("Name (GlyphTag)", tracking=True)
    street_glyphtag = fields.Char("Street (GlyphTag)", tracking=True)
    street2_glyphtag = fields.Char("Street2 (GlyphTag)", tracking=True)
    city_glyphtag = fields.Char("City (GlyphTag)", tracking=True)

    # ---------------------------------------------------------
    # Computed Glyph Fields
    # ---------------------------------------------------------
    name_glyph = fields.Char(
        string="Name (Glyph)",
        compute="_compute_glyph_fields",
        store=True,
    )
    street_glyph = fields.Char(
        string="Street (Glyph)",
        compute="_compute_glyph_fields",
        store=True,
    )
    street2_glyph = fields.Char(
        string="Street2 (Glyph)",
        compute="_compute_glyph_fields",
        store=True,
    )
    city_glyph = fields.Char(
        string="City (Glyph)",
        compute="_compute_glyph_fields",
        store=True,
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _sanitize_spaces(self, text: str) -> str:
        if not text:
            return ""
        text = text.replace("\u3000", "\u0020").strip()
        return re.sub(r"\s+", "\u0020", text)

    def _render(self, text: str, use_base: bool = False) -> str:
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        result = svc.normalize(text)
        return svc.render(result.text, use_base=use_base) or ""

    def _simplify(self, text: str) -> str:
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        return svc.simplify(text) or ""

    def _inverse(self, text: str) -> str:
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        return svc.inverse(text) or ""

    # ---------------------------------------------------------
    # Compute Methods
    # ---------------------------------------------------------
    @api.depends(
        'use_glyphtag',
        'name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag',
        'name', 'city', 'street', 'street2'
    )
    def _compute_glyph_fields(self):
        for rec in self:
            for fname in self.BASE_FIELDS:
                tag_field = f"{fname}_glyphtag"
                glyph_field = f"{fname}_glyph"

                if rec.use_glyphtag:
                    tag_val = getattr(rec, tag_field)
                    glyph_val = rec._render(tag_val, use_base=False)
                else:
                    glyph_val = getattr(rec, fname) or ""

                setattr(rec, glyph_field, glyph_val)

    # ---------------------------------------------------------
    # Onchange Handlers
    # ---------------------------------------------------------
    @api.onchange('use_glyphtag', 'name_glyphtag', 'street_glyphtag', 'street2_glyphtag', 'city_glyphtag')
    def _onchange_glyphtag_fields(self):
        if self.use_glyphtag:
            for base_field in self.BASE_FIELDS:
                tag_field = f"{base_field}_glyphtag"
                tag_val = getattr(self, tag_field)
                tag_val = self._simplify(tag_val)
                tag_val = self._sanitize_spaces(tag_val)
                setattr(self, tag_field, tag_val)
                base_val = self._render(tag_val, use_base=True)
                if base_val:
                    setattr(self, base_field, base_val)

    @api.onchange('name', 'street', 'street2', 'city')
    def _onchange_base_fields(self):
        if not self.use_glyphtag:
            for base_field in self.BASE_FIELDS:
                text = getattr(self, base_field)
                text = self._sanitize_spaces(text)
                setattr(self, base_field, text)

    # ---------------------------------------------------------
    # Validations & Syncing logic
    # ---------------------------------------------------------
    @api.constrains('name_glyphtag', 'street_glyphtag', 'street2_glyphtag', 'city_glyphtag')
    def _check_glyphtag_fields(self):
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        for rec in self:
            for base_field in self.BASE_FIELDS:
                tag_field = f"{base_field}_glyphtag"
                tag_val = getattr(rec, tag_field)
                if tag_val:
                    result = svc.normalize(tag_val)
                    if not getattr(result, 'success', False):
                        raise ValidationError("Invalid GlyphTag format.")

    def _sync_glyphtag_payload(self, record, vals):
        tag_fields = [f"{f}_glyphtag" for f in self.BASE_FIELDS]
        target_fields = set(['use_glyphtag'] + self.BASE_FIELDS + tag_fields)

        if not any(k in vals for k in target_fields):
            return

        use_tag = vals.get('use_glyphtag', record.use_glyphtag if record else False)

        for base_field in self.BASE_FIELDS:
            tag_field = f"{base_field}_glyphtag"
            if use_tag:
                current_tag_val = record[tag_field] if record else ''
                tag_val = vals.get(tag_field, current_tag_val)
                tag_val = self._sanitize_spaces(tag_val)
                base_val = self._render(tag_val, use_base=True)
                vals[base_field] = base_val
                vals[tag_field] = tag_val
            else:
                current_base_val = record[base_field] if record else ''
                base_val = vals.get(base_field, current_base_val) or ""
                base_val = self._sanitize_spaces(base_val)
                tag_val = self._inverse(base_val)
                vals[base_field] = base_val
                vals[tag_field] = tag_val
