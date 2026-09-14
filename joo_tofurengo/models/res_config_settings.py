from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_tofurengo module.
    Configures the Glyph System Identifier used by the tofurengo normalization service.
    Documentation: https://jp-rad.github.io/tofurengo/
    """
    _inherit = 'res.config.settings'

    joo_set = fields.Selection(
        selection=[
            ('mj_plusx', 'Extended MJ+ (mj_plusx)'),
            ('mj_plus', 'MJ+ (mj_plus)'),
            ('mj', 'MJ (mj)'),
            ('mj_onka', 'MJ with Onka (mj_onka)'),
        ],
        string="Glyph System Identifier",
        default="mj_plusx",
        config_parameter='joo_tofurengo.set',
        help="Determines the Glyph System Identifier used by GlyphService for normalization. "
             "Ref: https://jp-rad.github.io/tofurengo/"
    )
