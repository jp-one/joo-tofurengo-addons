from odoo import models, fields, api
from odoo.exceptions import ValidationError


class JooTofurengoPartnerNameMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.name.mixin'
    _description = 'Partner Name GlyphTag & IVS Mixin'

    # ---------------------------------------------------------
    # Input Fields
    # ---------------------------------------------------------
    use_name_glyphtag = fields.Boolean("Use GlyphTag for Name")
    name_glyphtag = fields.Char("Name GlyphTag", tracking=True)

    # ---------------------------------------------------------
    # Computed IVS & Name Fields
    # ---------------------------------------------------------
    name_ivs = fields.Char(
        string="Name (IVS)",
        compute="_compute_name_components",
        store=True,
    )
    family_name = fields.Char(
        string="Family Name",
        compute="_compute_name_components",
        store=True,
        index=True,
    )
    given_name = fields.Char(
        string="Given Name",
        compute="_compute_name_components",
        store=True,
        index=True,
    )
    family_name_ivs = fields.Char(
        string="Family Name (IVS)",
        compute="_compute_name_components",
        store=True,
    )
    given_name_ivs = fields.Char(
        string="Given Name (IVS)",
        compute="_compute_name_components",
        store=True,
    )

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------
    def _glyph_convert(self, text):
        if not text:
            return "", ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        result = svc.normalize(text)
        if not result.success:
            return "", ""
        norm = result.text
        return svc.render(norm, use_base=True), svc.render(norm)

    def _glyph_simplify(self, text):
        if not text:
            return ""
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        return svc.simplify(text)

    def _to_half_space(self, text):
        if not text:
            return ""
        return text.replace("\u3000", " ")

    def _split_name(self, text):
        if not text:
            return "", ""
        parts = text.split(" ", 1)
        return (parts[0], parts[1]) if len(parts) == 2 else (parts[0], "")

    # ---------------------------------------------------------
    # Compute Methods
    # ---------------------------------------------------------
    @api.depends('name', 'name_glyphtag', 'use_name_glyphtag', 'is_company')
    def _compute_name_components(self):
        for rec in self:
            if rec.use_name_glyphtag and rec.name_glyphtag:
                c_tag = rec._glyph_simplify(rec.name_glyphtag)
                _, ivs_name = rec._glyph_convert(c_tag)
            else:
                ivs_name = rec.name or ""

            raw_name = rec._to_half_space(rec.name or "")
            ivs_name = rec._to_half_space(ivs_name)

            rec.name_ivs = ivs_name

            if getattr(rec, 'is_company', False):
                rec.family_name = raw_name
                rec.given_name = ""
                rec.family_name_ivs = ivs_name
                rec.given_name_ivs = ""
            else:
                fam, giv = rec._split_name(raw_name)
                fam_ivs, giv_ivs = rec._split_name(ivs_name)
                rec.family_name = fam
                rec.given_name = giv
                rec.family_name_ivs = fam_ivs
                rec.given_name_ivs = giv_ivs

    # ---------------------------------------------------------
    # Onchange Handlers (Real-time UI Preview)
    # Note: Reverse synchronization to *_glyphtag is omitted.
    # ---------------------------------------------------------
    @api.onchange('use_name_glyphtag', 'name_glyphtag')
    def _onchange_name_glyphtag(self):
        if self.use_name_glyphtag and self.name_glyphtag:
            c_tag = self._glyph_simplify(self.name_glyphtag)
            raw_name, _ = self._glyph_convert(c_tag)
            self.name = self._to_half_space(raw_name)

    @api.onchange('name')
    def _onchange_name_raw(self):
        if self.name:
            self.name = self._to_half_space(self.name)

    # ---------------------------------------------------------
    # Validations & Synchronizations (Save / Create / Write)
    # ---------------------------------------------------------
    @api.constrains('name_glyphtag')
    def _check_name_glyphtag(self):
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        for rec in self:
            if rec.name_glyphtag:
                result = svc.normalize(rec.name_glyphtag)
                if not result.success:
                    raise ValidationError("Invalid Name GlyphTag format.")

    def _sync_name_payload(self, vals):
        target_fields = {'name', 'name_glyphtag', 'use_name_glyphtag'}

        # Trigger synchronization ONLY when name-related fields are present in vals
        if not any(k in vals for k in target_fields):
            return

        use_tag = vals.get('use_name_glyphtag', getattr(self, 'use_name_glyphtag', False))
        if use_tag:
            tag_val = vals.get('name_glyphtag', getattr(self, 'name_glyphtag', ''))
            if tag_val:
                c_tag = self._glyph_simplify(tag_val)
                raw_name, _ = self._glyph_convert(c_tag)
                vals['name'] = self._to_half_space(raw_name)
        else:
            # Sync name_glyphtag from name upon saving when GlyphTag is disabled
            target_name = vals.get('name', getattr(self, 'name', '')) or ""
            target_name = self._to_half_space(target_name)
            vals['name'] = target_name
            vals['name_glyphtag'] = self._glyph_simplify(target_name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._sync_name_payload(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._sync_name_payload(vals)
        return super().write(vals)
