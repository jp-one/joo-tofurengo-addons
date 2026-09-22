from odoo import models, api


class ResPartner(models.Model):
    _inherit = [
        "joo.partner.glyphtag.editor.mixin",
        "joo.partner.glyphtag.mixin",
        "res.partner",
    ]

    # ---------------------------------------------------------
    # Validations & Synchronizations (Save / Create / Write)
    # ---------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._sync_glyphtag_payload(record=None, vals=vals)
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            record._sync_glyphtag_payload(record=record, vals=vals)
        return super().write(vals)
