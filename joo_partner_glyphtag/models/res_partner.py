import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = [
        "joo.partner.glyphtag.editor.mixin",
        "res.partner",
    ]

    # ---------------------------------------------------------
    # Input Fields
    # ---------------------------------------------------------
    use_glyphtag = fields.Boolean("Use GlyphTag", tracking=True)

    name_glyphtag = fields.Char("Name (GlyphTag)", tracking=True)
    city_glyphtag = fields.Char("City (GlyphTag)", tracking=True)
    street_glyphtag = fields.Char("Street (GlyphTag)", tracking=True)
    street2_glyphtag = fields.Char("Street2 (GlyphTag)", tracking=True)

    # ---------------------------------------------------------
    # Computed Glyph Fields
    # ---------------------------------------------------------
    name_glyph = fields.Char(
        string="Name (Glyph)",
        compute="_compute_glyph_fields",
        store=True,
    )
    city_glyph = fields.Char(
        string="City (Glyph)",
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

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _sanitize_spaces(self, text: str) -> str:
        """Helper to normalize spaces by converting full-width spaces and collapsing multiple whitespaces."""
        if not text:
            return ""
        text = text.replace("\u3000", "\u0020").strip()
        return re.sub(r"\s+", "\u0020", text)

    def _convert_glyphtag(self, text: str, use_base: bool = False) -> str:
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        # normalize には use_base を渡さず、text のみ指定
        result = svc.normalize(text)
        if not getattr(result, 'success', False):
            return ""
        # render 側で use_base を指定して変換
        return svc.render(result.text, use_base=use_base) or ""

    def _simplify(self, text: str) -> str:
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        return svc.simplify(text) or ""

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
            for fname in ['name', 'city', 'street', 'street2']:
                tag_field = f"{fname}_glyphtag"
                glyph_field = f"{fname}_glyph"

                if rec.use_glyphtag:
                    tag_val = getattr(rec, tag_field)
                    glyph_val = rec._convert_glyphtag(tag_val, use_base=False)
                else:
                    glyph_val = getattr(rec, fname) or ""

                setattr(rec, glyph_field, glyph_val)

    # ---------------------------------------------------------
    # Onchange Handlers (Real-time UI Preview)
    # ---------------------------------------------------------
    @api.onchange('use_glyphtag', 'name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _onchange_glyphtag_fields(self):
        if self.use_glyphtag:
            for base_field in ['name', 'city', 'street', 'street2']:
                tag_field = f"{base_field}_glyphtag"
                tag_val = getattr(self, tag_field)
                tag_val = self._simplify(tag_val)
                tag_val = self._sanitize_spaces(tag_val)
                setattr(self, tag_field, tag_val)
                base_val = self._convert_glyphtag(tag_val, use_base=True)
                if base_val:
                    setattr(self, base_field, base_val)

    @api.onchange('name', 'city', 'street', 'street2')
    def _onchange_base_fields(self):
        if not self.use_glyphtag:
            for base_field in ['name', 'city', 'street', 'street2']:
                text = getattr(self, base_field)
                text = self._sanitize_spaces(text)
                setattr(self, base_field, text)

    # ---------------------------------------------------------
    # Validations & Synchronizations (Save / Create / Write)
    # ---------------------------------------------------------
    @api.constrains('name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _check_glyphtag_fields(self):
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        for rec in self:
            for tag_field in ['name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag']:
                tag_val = getattr(rec, tag_field)
                if tag_val:
                    result = svc.normalize(tag_val)
                    if not getattr(result, 'success', False):
                        raise ValidationError("Invalid GlyphTag format.")

    def _sync_glyphtag_payload(self, record, vals):
        target_fields = {
            'use_glyphtag', 'name', 'city', 'street', 'street2',
            'name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag'
        }

        if not any(k in vals for k in target_fields):
            return

        # record が存在する場合はその値を取得、create時など未作成の場合は False/空文字
        use_tag = vals.get('use_glyphtag', record.use_glyphtag if record else False)

        for base_field in ['name', 'city', 'street', 'street2']:
            tag_field = f"{base_field}_glyphtag"
            if use_tag:
                current_tag_val = record[tag_field] if record else ''
                tag_val = vals.get(tag_field, current_tag_val)
                base_val = self._convert_glyphtag(tag_val, use_base=True)
                vals[base_field] = base_val
            else:
                current_base_val = record[base_field] if record else ''
                base_val = vals.get(base_field, current_base_val) or ""
                base_val = self._sanitize_spaces(base_val)
                vals[base_field] = base_val
                vals[tag_field] = base_val

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._sync_glyphtag_payload(record=None, vals=vals)
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._sync_glyphtag_payload(record=record, vals=vals)
        return super().write(vals)
