from odoo import models


class GlyphtagEditorMixin(models.AbstractModel):
    _name = "joo.partner.glyphtag.editor.mixin"
    _description = "Glyphtag Editor Logic Mixin"

    def open_glyph_editor(self):
        self.ensure_one()

        ctx = {
            "default_partner_id": self.id,
            "default_use_glyphtag": self.use_glyphtag,

            "default_name": self.name,
            "default_city": self.city,
            "default_street": self.street,
            "default_street2": self.street2,

            "default_name_glyphtag": self.name_glyphtag,
            "default_city_glyphtag": self.city_glyphtag,
            "default_street_glyphtag": self.street_glyphtag,
            "default_street2_glyphtag": self.street2_glyphtag,

            "default_name_glyph": self.name_glyph,
            "default_city_glyph": self.city_glyph,
            "default_street_glyph": self.street_glyph,
            "default_street2_glyph": self.street2_glyph,
        }

        return {
            "type": "ir.actions.act_window",
            "name": "Glyph Editor",
            "res_model": "joo.partner.glyphtag.editor.wizard",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }
