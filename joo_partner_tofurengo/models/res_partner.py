from curses import raw

import jaconv
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = "family_name_kana, given_name_kana, family_name, given_name, id"

    # ---------------------------------------------------------
    # Kana fields
    # Half-width Katakana → Full-width Katakana → Hiragana
    # ---------------------------------------------------------
    family_name_kana = fields.Char("Family Name Kana", index=True)
    given_name_kana = fields.Char("Given Name Kana", index=True)

    # ---------------------------------------------------------
    # GlyphTag usage flags
    # ---------------------------------------------------------
    use_name_glyphtag = fields.Boolean("Use GlyphTag for Name")
    use_address_glyphtag = fields.Boolean("Use GlyphTag for Address")

    # ---------------------------------------------------------
    # GlyphTag input fields
    # ---------------------------------------------------------
    name_glyphtag = fields.Char("Name GlyphTag", tracking=True)
    city_glyphtag = fields.Char("City GlyphTag")
    street_glyphtag = fields.Char("Street GlyphTag")
    street2_glyphtag = fields.Char("Street2 GlyphTag")

    # ---------------------------------------------------------
    # IVS output fields
    # ---------------------------------------------------------
    name_ivs = fields.Char("Name (IVS)", compute="_compute_glyph_outputs", store=True)
    city_ivs = fields.Char("City (IVS)", compute="_compute_glyph_outputs", store=True)
    street_ivs = fields.Char("Street (IVS)", compute="_compute_glyph_outputs", store=True)
    street2_ivs = fields.Char("Street2 (IVS)", compute="_compute_glyph_outputs", store=True)

    # ---------------------------------------------------------
    # Name-based split fields (raw name)
    # ---------------------------------------------------------
    family_name = fields.Char("Family Name", index=True)
    given_name = fields.Char("Given Name", index=True)

    # ---------------------------------------------------------
    # IVS-based name split
    # ---------------------------------------------------------
    family_name_ivs = fields.Char("Family Name (IVS)", compute="_compute_glyph_outputs", store=True)
    given_name_ivs = fields.Char("Given Name (IVS)", compute="_compute_glyph_outputs", store=True)

    # ---------------------------------------------------------
    # Kana conversion
    # ---------------------------------------------------------
    def _katakana_to_hiragana(self, text):
        if not text:
            return ""
        zenkaku = jaconv.h2z(text, kana=True)
        return jaconv.kata2hira(zenkaku)

    @api.onchange('family_name_kana', 'given_name_kana')
    def _onchange_furigana(self):
        if self.family_name_kana:
            self.family_name_kana = self._katakana_to_hiragana(self.family_name_kana)
        if self.given_name_kana:
            self.given_name_kana = self._katakana_to_hiragana(self.given_name_kana)

    # ---------------------------------------------------------
    # Glyph service helpers
    # ---------------------------------------------------------
    def _rende_b_v(self, text):
        """
        normalize and render the GlyphTag text.
        """
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
        """
        Simplify the GlyphTag text.
        """
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
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""

    # ---------------------------------------------------------
    # Compute IVS + name-based split
    # ---------------------------------------------------------
    @api.depends(
        'is_company',
        'name', 'city', 'street', 'street2',
        'use_name_glyphtag', 'use_address_glyphtag',
        'name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag'
    )
    def _compute_glyph_outputs(self):
        for rec in self:

            # raw_name and ivs_name are computed based on whether GlyphTag is used for the name.
            rec.name_glyphtag = rec._simplify(rec.name_glyphtag)
            if rec.use_name_glyphtag:
                tagged = rec.name_glyphtag or ""
                raw, ivs = rec._rende_b_v(tagged)
            else:
                raw = rec.name or ""
                ivs = raw
            rec.name = self._to_half_space(raw)
            rec.name_ivs = self._to_half_space(ivs)

            # Address IVS
            rec.city_glyphtag = rec._simplify(rec.city_glyphtag)
            rec.street_glyphtag = rec._simplify(rec.street_glyphtag)
            rec.street2_glyphtag = rec._simplify(rec.street2_glyphtag)
            if rec.use_address_glyphtag:
                # city
                tagged = rec.city_glyphtag or ""
                raw, ivs = rec._rende_b_v(tagged)
                rec.city = raw
                rec.city_ivs = ivs
                # street
                tagged = rec.street_glyphtag or ""
                raw, ivs = rec._rende_b_v(tagged)
                rec.street = raw
                rec.street_ivs = ivs
                # street2
                tagged = rec.street2_glyphtag or ""
                raw, ivs = rec._rende_b_v(tagged)
                rec.street2 = raw
                rec.street2_ivs = ivs
            else:
                # city
                city = rec.city or ""
                rec.city_ivs = city
                # street
                street = rec.street or ""
                rec.street_ivs = street
                # street2
                street2 = rec.street2 or ""
                rec.street2_ivs = street2

            # Raw name split
            if rec.is_company:
                rec.family_name = rec.name
                rec.given_name = ""
            else:
                fam, giv = rec._split_name(rec.name)
                rec.family_name = fam
                rec.given_name = giv

            # IVS split
            if rec.is_company:
                rec.family_name_ivs = rec.name_ivs
                rec.given_name_ivs = ""
            else:
                fam, giv = rec._split_name(rec.name_ivs)
                rec.family_name_ivs = fam
                rec.given_name_ivs = giv                
    # ---------------------------------------------------------
    # write(): GlyphTag state transition logic
    # ---------------------------------------------------------
    def write(self, vals):
        for rec in self:

            # Name GlyphTag:
            if 'name' in vals:
                if not rec.name_glyphtag:
                    vals.setdefault('name_glyphtag', rec.name)

            # Address GlyphTag
            if 'city' in vals:
                if not rec.city_glyphtag:
                    vals.setdefault('city_glyphtag', rec.city)
            if 'street' in vals:
                if not rec.street_glyphtag:
                    vals.setdefault('street_glyphtag', rec.street)
            if 'street2' in vals:
                if not rec.street2_glyphtag:
                    vals.setdefault('street2_glyphtag', rec.street2)

        return super(ResPartner, self).write(vals)
