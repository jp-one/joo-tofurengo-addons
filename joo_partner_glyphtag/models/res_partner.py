from odoo import api, models


class ResPartner(models.Model):
    """
    Partner Extension with GlyphTag Features.

    This model integrates GlyphTag functionality into `res.partner` by combining:
    1. `joo.partner.glyphtag.editor.mixin`: Action handling (e.g., opening custom view/editor).
    2. `joo.partner.glyphtag.mixin`: Core field definitions, compute methods, and payload sync logic.
    """
    
    _inherit = [
        "joo.partner.glyphtag.editor.mixin",
        "joo.partner.glyphtag.mixin",
        "res.partner",
    ]
    _name = 'res.partner'
    
    # ---------------------------------------------------------
    # Validations & Synchronizations (Save / Create / Write)
    # ---------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override `create` to process and synchronize GlyphTag fields before record generation.
        Intersects payload values to ensure standard text and GlyphTag formats are aligned.
        """
        for vals in vals_list:
            self._sync_glyphtag_payload(record=None, vals=vals)
        return super().create(vals_list)

    def write(self, vals):
        """
        Override `write` to update and synchronize GlyphTag fields on existing records.
        Evaluates each record individually against input changes in `vals`.
        """
        for record in self:
            record._sync_glyphtag_payload(record=record, vals=vals)
        return super().write(vals)
