import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PartnerNameMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.name.mixin'
    _description = 'Partner Name GlyphTag & IVS Mixin'

    use_name_glyphtag = fields.Boolean("Use GlyphTag for Name")
    name_glyphtag = fields.Char("Name GlyphTag", tracking=True)

    name = fields.Char(
        compute="_compute_name_fields",
        inverse="_inverse_name",
        store=True,
        readonly=False,
    )
    name_ivs = fields.Char("Name (IVS)", compute="_compute_name_fields", store=True)

    family_name = fields.Char("Family Name", compute="_compute_name_fields", store=True, index=True)
    given_name = fields.Char("Given Name", compute="_compute_name_fields", store=True, index=True)
    family_name_ivs = fields.Char("Family Name (IVS)", compute="_compute_name_fields", store=True)
    given_name_ivs = fields.Char("Given Name (IVS)", compute="_compute_name_fields", store=True)

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
    # Inverse & Sync
    # ---------------------------------------------------------
    def _inverse_name(self):
        for rec in self:
            if rec.name:
                rec.name = rec._to_half_space(rec.name)
            if not rec.use_name_glyphtag:
                rec.name_glyphtag = rec._glyph_simplify(rec.name)

    @api.onchange('use_name_glyphtag', 'name')
    def _onchange_name_sync(self):
        if not self.use_name_glyphtag and self.name:
            self.name_glyphtag = self._glyph_simplify(self.name)

    @api.constrains('name_glyphtag')
    def _check_name_glyphtag(self):
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        for rec in self:
            if rec.name_glyphtag:
                result = svc.normalize(rec.name_glyphtag)
                if not result.success:
                    raise ValidationError("Invalid Name GlyphTag")

    # ---------------------------------------------------------
    # Compute Logic (store=True により DB に保持され一覧表示時の再計算を回避)
    # ---------------------------------------------------------
    @api.depends('is_company', 'use_name_glyphtag', 'name_glyphtag', 'name')
    def _compute_name_fields(self):
        for rec in self:
            if rec.use_name_glyphtag:
                c_tag = rec._glyph_simplify(rec.name_glyphtag)
                raw_name, ivs_name = rec._glyph_convert(c_tag)
            else:
                raw_name = rec.name or ""
                ivs_name = raw_name

            raw_name = rec._to_half_space(raw_name)
            ivs_name = rec._to_half_space(ivs_name)

            rec.name = raw_name
            rec.name_ivs = ivs_name

            if getattr(rec, 'is_company', False):
                rec.family_name = raw_name
                rec.given_name = ""
                rec.family_name_ivs = ivs_name
                rec.given_name_ivs = ""
            else:
                fam, giv = rec._split_name(raw_name)
                rec.family_name, rec.given_name = fam, giv

                fam_ivs, giv_ivs = rec._split_name(ivs_name)
                rec.family_name_ivs, rec.given_name_ivs = fam_ivs, giv_ivs
