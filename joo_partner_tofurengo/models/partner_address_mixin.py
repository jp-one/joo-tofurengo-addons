import logging
import traceback
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PartnerAddressMixin(models.AbstractModel):
    _name = 'joo.tofurengo.partner.address.mixin'
    _description = 'Partner Address GlyphTag & IVS Mixin'

    # ---------------------------------------------------------
    # GlyphTag usage flags
    # ---------------------------------------------------------
    use_address_glyphtag = fields.Boolean("Use GlyphTag for Address")

    # ---------------------------------------------------------
    # GlyphTag input fields
    # ---------------------------------------------------------
    city_glyphtag = fields.Char("City GlyphTag")
    street_glyphtag = fields.Char("Street GlyphTag")
    street2_glyphtag = fields.Char("Street2 GlyphTag")

    # ---------------------------------------------------------
    # Override standard fields to attach compute & inverse
    # ---------------------------------------------------------
    city = fields.Char(
        compute="_compute_address_fields",
        inverse="_inverse_address",
        store=True,
        readonly=False,
    )
    street = fields.Char(
        compute="_compute_address_fields",
        inverse="_inverse_address",
        store=True,
        readonly=False,
    )
    street2 = fields.Char(
        compute="_compute_address_fields",
        inverse="_inverse_address",
        store=True,
        readonly=False,
    )

    # ---------------------------------------------------------
    # IVS output fields (store=True により一覧表示時の再計算を回避)
    # ---------------------------------------------------------
    city_ivs = fields.Char(
        string="City (IVS)",
        compute="_compute_address_fields",
        store=True,
    )
    street_ivs = fields.Char(
        string="Street (IVS)",
        compute="_compute_address_fields",
        store=True,
    )
    street2_ivs = fields.Char(
        string="Street2 (IVS)",
        compute="_compute_address_fields",
        store=True,
    )

    # ---------------------------------------------------------
    # Glyph service helpers
    # ---------------------------------------------------------
    def _convert_glyphtag_to_raw_ivs(self, text):
        if not text:
            return "", ""

        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        result = svc.normalize(text)

        if not result.success:
            return "", ""

        norm = result.text
        raw = svc.render(norm, use_base=True)
        ivs = svc.render(norm)

        return raw, ivs

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
    # Inverse Methods
    # ---------------------------------------------------------
    def _inverse_address(self):
        for rec in self:
            _logger.debug("=== [_inverse_address] Triggered for ID %s ===", rec.id)
            if rec.city:
                rec.city = rec._to_half_space(rec.city)
            if rec.street:
                rec.street = rec._to_half_space(rec.street)
            if rec.street2:
                rec.street2 = rec._to_half_space(rec.street2)

            if not rec.use_address_glyphtag:
                rec.city_glyphtag = rec._simplify(rec.city)
                rec.street_glyphtag = rec._simplify(rec.street)
                rec.street2_glyphtag = rec._simplify(rec.street2)

    # ---------------------------------------------------------
    # GlyphTag Validation
    # ---------------------------------------------------------
    def _validate_single_glyphtag(self, text):
        if not text:
            return
        svc = self.env['joo_tofurengo.glyph_service'].sudo()
        result = svc.normalize(text)
        if not result.success:
            raise ValidationError("Invalid GlyphTag")

    @api.constrains('city_glyphtag', 'street_glyphtag', 'street2_glyphtag')
    def _check_glyphtag_fields(self):
        for rec in self:
            for fname in ['city_glyphtag', 'street_glyphtag', 'street2_glyphtag']:
                val = getattr(rec, fname)
                if val:
                    rec._validate_single_glyphtag(val)

    # ---------------------------------------------------------
    # Compute Logic (store=True で保存されるため一覧表示時は再計算されない)
    # ---------------------------------------------------------
    @api.depends(
        'use_address_glyphtag',
        'city_glyphtag', 'street_glyphtag', 'street2_glyphtag',
        'city', 'street', 'street2'
    )
    def _compute_address_fields(self):
        for rec in self:
            _logger.debug("=== [_compute_address_fields] Triggered for ID %s ===", rec.id)

            if rec.use_address_glyphtag:
                # use_address_glyphtag が True の場合: *_glyphtag から取得・変換
                c_tag = rec._simplify(rec.city_glyphtag)
                s_tag = rec._simplify(rec.street_glyphtag)
                s2_tag = rec._simplify(rec.street2_glyphtag)

                raw_city, ivs_city = rec._convert_glyphtag_to_raw_ivs(c_tag)
                raw_street, ivs_street = rec._convert_glyphtag_to_raw_ivs(s_tag)
                raw_street2, ivs_street2 = rec._convert_glyphtag_to_raw_ivs(s2_tag)

                rec.city = raw_city
                rec.city_ivs = ivs_city
                rec.street = raw_street
                rec.street_ivs = ivs_street
                rec.street2 = raw_street2
                rec.street2_ivs = ivs_street2
            else:
                # use_address_glyphtag が False の場合: city, street, street2 から取得
                rec.city_ivs = rec.city or ""
                rec.street_ivs = rec.street or ""
                rec.street2_ivs = rec.street2 or ""

    def write(self, vals):
        stack = "".join(traceback.format_stack()[-4:-1])
        _logger.info("=== write called with vals: %s ===\nCallers:\n%s", vals, stack)
        return super().write(vals)
