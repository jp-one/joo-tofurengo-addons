from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JooTofurengoPartnerAddressMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.address.mixin'
    _description = 'Partner Address GlyphTag & IVS Mixin'

    # ---------------------------------------------------------
    # GlyphTag usage flags
    # ---------------------------------------------------------
    use_address_glyphtag = fields.Boolean("Use GlyphTag for Address")

    # ---------------------------------------------------------
    # GlyphTag input fields
    # ---------------------------------------------------------
    city_glyphtag = fields.Char("City GlyphTag", tracking=True)
    street_glyphtag = fields.Char("Street GlyphTag", tracking=True)
    street2_glyphtag = fields.Char("Street2 GlyphTag", tracking=True)

    # ---------------------------------------------------------
    # IVS output fields (Stored standard fields)
    # ---------------------------------------------------------
    city_ivs = fields.Char(string="City (IVS)")
    street_ivs = fields.Char(string="Street (IVS)")
    street2_ivs = fields.Char(string="Street2 (IVS)")

    # ---------------------------------------------------------
    # Service Helpers
    # ---------------------------------------------------------
    def _convert_glyphtag_to_raw_ivs(self, text):
        if not text:
            return "", ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        result = svc.normalize(text)
        if not result.success:
            return "", ""
        norm = result.text
        return svc.render(norm, use_base=True), svc.render(norm)

    def _simplify(self, text):
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        return svc.simplify(text)

    def _to_half_space(self, text):
        if not text:
            return ""
        return text.replace("\u3000", " ")

    def _sync_address_fields(self, vals):
        """Helper to compute/sync address, glyphtag, and IVS values for dictionary payloads."""
        use_tag = vals.get('use_address_glyphtag', getattr(self, 'use_address_glyphtag', False))

        if use_tag:
            # Sync from GlyphTag -> Raw & IVS
            for fname in ['city', 'street', 'street2']:
                tag_val = vals.get(f'{fname}_glyphtag', getattr(self, f'{fname}_glyphtag', ''))
                if tag_val:
                    c_tag = self._simplify(tag_val)
                    raw, ivs = self._convert_glyphtag_to_raw_ivs(c_tag)
                    vals[fname] = self._to_half_space(raw)
                    vals[f'{fname}_ivs'] = self._to_half_space(ivs)
        else:
            # Sync from Raw -> GlyphTag & IVS
            for fname in ['city', 'street', 'street2']:
                if fname in vals or getattr(self, fname, False):
                    raw_val = self._to_half_space(vals.get(fname, getattr(self, fname, '')))
                    vals[fname] = raw_val
                    vals[f'{fname}_ivs'] = raw_val
                    # Sync GlyphTag from Raw
                    vals[f'{fname}_glyphtag'] = self._simplify(raw_val)

    # ---------------------------------------------------------
    # Onchange Handlers (UI Interaction)
    # ---------------------------------------------------------
    @api.onchange('use_address_glyphtag', 'city', 'street', 'street2', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _onchange_glyphtag_fields(self):
        if self.use_address_glyphtag:
            # Sync from GlyphTag -> Raw & IVS
            for fname in ['city', 'street', 'street2']:
                tag_val = getattr(self, f'{fname}_glyphtag')
                if tag_val:
                    c_tag = self._simplify(tag_val)
                    raw, ivs = self._convert_glyphtag_to_raw_ivs(c_tag)
                    setattr(self, fname, raw)
                    setattr(self, f'{fname}_ivs', ivs)
        else:
            # Sync from Raw -> GlyphTag & IVS
            for fname in ['city', 'street', 'street2']:
                raw_val = self._to_half_space(getattr(self, fname))
                setattr(self, fname, raw_val)
                setattr(self, f'{fname}_ivs', raw_val)
                # setattr(self, f'{fname}_glyphtag', raw_val)

    # ---------------------------------------------------------
    # Validations & ORM Overrides
    # ---------------------------------------------------------
    @api.constrains('city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _check_glyphtag_fields(self):
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        for rec in self:
            for fname in ['city_glyphtag', 'street_glyphtag', 'street2_glyphtag']:
                val = getattr(rec, fname)
                if val:
                    result = svc.normalize(val)
                    if not result.success:
                        raise ValidationError("Invalid GlyphTag format.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._sync_address_fields(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._sync_address_fields(vals)
        return super().write(vals)
