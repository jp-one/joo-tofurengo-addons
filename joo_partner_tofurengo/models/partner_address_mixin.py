from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JooTofurengoPartnerAddressMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.address.mixin'
    _description = 'Partner Address GlyphTag & IVS Mixin'

    # ---------------------------------------------------------
    # Input Fields
    # ---------------------------------------------------------
    use_address_glyphtag = fields.Boolean("Use GlyphTag for Address")

    city_glyphtag = fields.Char("City GlyphTag")
    street_glyphtag = fields.Char("Street GlyphTag")
    street2_glyphtag = fields.Char("Street2 GlyphTag")

    # ---------------------------------------------------------
    # Computed IVS & Address Fields
    # ---------------------------------------------------------
    city_ivs = fields.Char(
        string="City (IVS)",
        compute="_compute_address_ivs",
        store=True,
    )
    street_ivs = fields.Char(
        string="Street (IVS)",
        compute="_compute_address_ivs",
        store=True,
    )
    street2_ivs = fields.Char(
        string="Street2 (IVS)",
        compute="_compute_address_ivs",
        store=True,
    )

    # ---------------------------------------------------------
    # Helpers
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

    # ---------------------------------------------------------
    # Compute Methods
    # ---------------------------------------------------------
    @api.depends(
        'use_address_glyphtag',
        'city_glyphtag', 'street_glyphtag', 'street2_glyphtag',
        'city', 'street', 'street2'
    )
    def _compute_address_ivs(self):
        for rec in self:
            for fname in ['city', 'street', 'street2']:
                tag_field = f"{fname}_glyphtag"
                ivs_field = f"{fname}_ivs"

                if rec.use_address_glyphtag and getattr(rec, tag_field):
                    c_tag = rec._simplify(getattr(rec, tag_field))
                    _, ivs_val = rec._convert_glyphtag_to_raw_ivs(c_tag)
                else:
                    ivs_val = getattr(rec, fname) or ""

                setattr(rec, ivs_field, rec._to_half_space(ivs_val))

    # ---------------------------------------------------------
    # Onchange Handlers (Real-time UI Preview)
    # Note: Reverse synchronization to *_glyphtag is omitted.
    # ---------------------------------------------------------
    @api.onchange('use_address_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _onchange_glyphtag_address(self):
        if self.use_address_glyphtag:
            for fname in ['city', 'street', 'street2']:
                tag_val = getattr(self, f"{fname}_glyphtag")
                if tag_val:
                    c_tag = self._simplify(tag_val)
                    raw, _ = self._convert_glyphtag_to_raw_ivs(c_tag)
                    setattr(self, fname, raw)

    @api.onchange('city', 'street', 'street2')
    def _onchange_raw_address(self):
        for fname in ['city', 'street', 'street2']:
            raw_val = getattr(self, fname)
            if raw_val:
                setattr(self, fname, self._to_half_space(raw_val))

    # ---------------------------------------------------------
    # Validations & Synchronizations (Save / Create / Write)
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

    def _sync_address_payload(self, vals):
        target_fields = {'use_address_glyphtag', 'city', 'street', 'street2', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag'}

        # Trigger synchronization ONLY when address-related fields are present in vals
        if not any(k in vals for k in target_fields):
            return

        use_tag = vals.get('use_address_glyphtag', getattr(self, 'use_address_glyphtag', False))

        for fname in ['city', 'street', 'street2']:
            tag_field = f"{fname}_glyphtag"
            if use_tag:
                tag_val = vals.get(tag_field, getattr(self, tag_field, ''))
                if tag_val:
                    c_tag = self._simplify(tag_val)
                    raw, _ = self._convert_glyphtag_to_raw_ivs(c_tag)
                    vals[fname] = raw
            else:
                # Sync glyphtag fields from address fields upon saving when GlyphTag is disabled
                raw_val = vals.get(fname, getattr(self, fname, '')) or ""
                raw_val = self._to_half_space(raw_val)
                vals[fname] = raw_val
                vals[tag_field] = self._simplify(raw_val)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._sync_address_payload(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._sync_address_payload(vals)
        return super().write(vals)
