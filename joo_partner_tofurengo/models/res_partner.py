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
    name_glyphtag = fields.Char("Name GlyphTag")
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
    def _get_glyph_service(self):
        self.env['joo_tofurengo.glyph_service']
        
    def _normalize(self, svc, text):
        """
        normalize the GlyphTag text.
        """
        result = svc.normalize(text)
        if result.success:
            return result.text
        return ""
        
    def _render_b(self, svc, text):
        """
        render the GlyphTag text.
        """
        return svc.render(text, use_base=True)

    def _render_v(self, svc, text):
        """
        render the GlyphTag text.
        """
        return svc.render(text, use_base=False)

    def _split_name(self, text):
        if not text:
            return ("", "")
        parts = text.split(" ", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], ""

    # ---------------------------------------------------------
    # Compute IVS + name-based split
    # ---------------------------------------------------------
    @api.depends(
        'name', 'city', 'street', 'street2',
        'use_name_glyphtag', 'use_address_glyphtag',
        'name_glyphtag', 'city_glyphtag', 'street_glyphtag', 'street2_glyphtag'
    )
    def _compute_glyph_outputs(self):
        svc = rec._get_glyph_service().sudo()
        for rec in self:

            # raw_name and ivs_name are computed based on whether GlyphTag is used for the name.
            if rec.use_name_glyphtag:
                tagged = rec.name_glyphtag or ""
                norm = rec._normalize(svc, tagged)
                raw = rec._render_b(svc, norm)
                ivs = rec._render_v(svc, norm)
            else:
                raw = rec.name or ""
                ivs = raw

            rec.name = raw
            rec.name_ivs = ivs

            # Raw name split
            fam, giv = rec._split_name(raw)
            rec.family_name = fam
            rec.given_name = giv

            # IVS split
            fam, giv = rec._split_name(ivs)
            rec.family_name_ivs = fam
            rec.given_name_ivs = giv


            # Address IVS
            if rec.use_address_glyphtag:
                # city
                tagged = rec.city_glyphtag or ""
                norm = rec._normalize(svc, tagged)
                raw = rec._render_b(svc, norm)
                ivs = rec._render_v(svc, norm)
                rec.city = raw
                rec.city_ivs = ivs
                # street
                tagged = rec.street_glyphtag or ""
                norm = rec._normalize(svc, tagged)
                raw = rec._render_b(svc, norm)
                ivs = rec._render_v(svc, norm)
                rec.street = raw
                rec.street_ivs = ivs
                # street2
                tagged = rec.street2_glyphtag or ""
                norm = rec._normalize(svc, tagged)
                raw = rec._render_b(svc, norm)
                ivs = rec._render_v(svc, norm)
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
                
    # ---------------------------------------------------------
    # write(): GlyphTag state transition logic
    # ---------------------------------------------------------
    def write(self, vals):
        for rec in self:

            # Name GlyphTag: False → True
            if 'use_name_glyphtag' in vals:
                new_flag = vals['use_name_glyphtag']
                if not rec.use_name_glyphtag and new_flag:
                    if not rec.name_glyphtag:
                        vals.setdefault('name_glyphtag', rec.name)
                if rec.use_name_glyphtag and not new_flag:
                    vals.setdefault('name_glyphtag', "")

            # Address GlyphTag: False → True
            if 'use_address_glyphtag' in vals:
                new_flag = vals['use_address_glyphtag']
                if not rec.use_address_glyphtag and new_flag:
                    if not rec.city_glyphtag:
                        vals.setdefault('city_glyphtag', rec.city)
                    if not rec.street_glyphtag:
                        vals.setdefault('street_glyphtag', rec.street)
                    if not rec.street2_glyphtag:
                        vals.setdefault('street2_glyphtag', rec.street2)
                if rec.use_address_glyphtag and not new_flag:
                    vals.setdefault('city_glyphtag', "")
                    vals.setdefault('street_glyphtag', "")
                    vals.setdefault('street2_glyphtag', "")

        return super(ResPartner, self).write(vals)
