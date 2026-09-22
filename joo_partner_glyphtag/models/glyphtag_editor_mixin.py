from odoo import models
from odoo.exceptions import UserError

class JooPartnerGlyphtagEditorMixin(models.AbstractModel):
    _name = "joo.partner.glyphtag.editor.mixin"
    _description = "Glyphtag Editor Logic Mixin"

    def _action_open_glyph_editor(self):
        self.ensure_one()

        action = self.env.ref(
            "joo_partner_glyphtag.action_partner_glyph_editor_dialog"
        ).read()[0]

        # 現在開いているレコードのIDを割り当て
        action["res_id"] = self.id

        return action
    
    def action_open_glyph_editor_wizard(self):
        if len(self) <= 1:
            return self._action_open_glyph_editor()

        # ウィザード初期化用の Context を作成
        ctx = dict(self.env.context, active_ids=self.ids, active_model=self._name)

        # 例: ウィザード（TransientModel）のアクションを呼び出す構成
        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'Glyph Editor Wizard',
        #     'res_model': 'partner.glyph.editor.wizard',
        #     'view_mode': 'form',
        #     'target': 'new',
        #     'context': ctx,
        # }

        raise UserError(
            f"対象レコード（{len(self)}件）に対するウィザード機能は準備中です。"
        )
