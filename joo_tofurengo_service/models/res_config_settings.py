from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_tofurengo module.
    Allows selecting the glyph set used for glyph tag normalization.
    """
    _inherit = 'res.config.settings'

    joo_set = fields.Selection(
        selection=[
            ('mj_plusx', 'Extended MJ+'),
            ('mj_plus', 'MJ+'),
            ('mj', 'MJ'),
        ],
        string="Glyph Set",
        default="mj_plusx",
        config_parameter='joo_tofurengo.set',
        help="Select the glyph set used for glyph tag normalization."
    )
