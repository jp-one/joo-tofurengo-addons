from odoo import _, models
from odoo.exceptions import UserError


class JooPartnerGlyphtagEditorMixin(models.AbstractModel):
    _name = "joo.partner.glyphtag.editor.mixin"
    _description = "Glyphtag Editor Logic Mixin"

    def open_joo_partner_glyphtag_editor(self):
        """Open the Glyphtag Editor view/action for a single record."""
        self.ensure_one()

        action = self.env.ref(
            "joo_partner_glyphtag.action_partner_glyphtag_editor"
        ).read()[0]

        action["res_id"] = self.id

        return action

    def action_server_partner_glyphtag_editor(self):
        """Server action entry point to open the Glyphtag Editor."""
        if len(self) <= 1:
            return self.open_joo_partner_glyphtag_editor()

        raise UserError(
            _(
                "The feature for multiple records (%s records) is currently under development.",
                len(self),
            )
        )
