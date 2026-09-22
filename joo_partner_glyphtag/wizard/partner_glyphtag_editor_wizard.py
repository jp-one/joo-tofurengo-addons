# -*- coding: utf-8 -*-
from odoo import models, fields, api


class JooPartnerGlyphtagEditorWizard(models.TransientModel):
    _name = "joo.partner.glyphtag.editor.wizard"
    _description = "Partner GlyphTag Editor Wizard"

    partner_id = fields.Many2one("res.partner", string="Partner", required=True, ondelete="cascade")

    use_glyphtag = fields.Boolean("Use GlyphTag")

    name = fields.Char("Name")
    city = fields.Char("City")
    street = fields.Char("Street")
    street2 = fields.Char("Street2")

    name_glyphtag = fields.Char("Name (GlyphTag)")
    city_glyphtag = fields.Char("City (GlyphTag)")
    street_glyphtag = fields.Char("Street (GlyphTag)")
    street2_glyphtag = fields.Char("Street2 (GlyphTag)")

    name_glyph = fields.Char("Name (Glyph)")
    city_glyph = fields.Char("City (Glyph)")
    street_glyph = fields.Char("Street (Glyph)")
    street2_glyph = fields.Char("Street2 (Glyph)")

    def apply_glyph(self):
        self.ensure_one()
        self.partner_id.write({
            "use_glyphtag": self.use_glyphtag,

            "name": self.name,
            "city": self.city,
            "street": self.street,
            "street2": self.street2,

            "name_glyphtag": self.name_glyphtag,
            "city_glyphtag": self.city_glyphtag,
            "street_glyphtag": self.street_glyphtag,
            "street2_glyphtag": self.street2_glyphtag,
        })
        return {"type": "ir.actions.act_window_close"}
