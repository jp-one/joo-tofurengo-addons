from odoo import models
from odoo.exceptions import UserError

class JooPartnerGlyphtagEditorMixin(models.AbstractModel):
    _name = "joo.partner.glyphtag.editor.mixin"
    _description = "Glyphtag Editor Logic Mixin"

    def open_joo_partner_glyphtag_editor(self):
        self.ensure_one()

        action = self.env.ref(
            "joo_partner_glyphtag.action_partner_glyphtag_editor"
        ).read()[0]

        action["res_id"] = self.id

        return action
    
    def action_server_partner_glyphtag_editor(self):
        if len(self) <= 1:
            return self.open_joo_partner_glyphtag_editor()

        raise UserError(
            f"対象レコード（{len(self)}件）に対するウィザード機能は準備中です。"
        )
