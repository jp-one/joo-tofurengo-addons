from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_glyph_fonts module.
    Allows selecting the default font used for glyph rendering in the system.
    """
    _inherit = 'res.config.settings'

    joo_font = fields.Selection(
        selection=[
            ('dwpiexmincho', 'DWPI Extended Mincho'),
            ('dwpimincho', 'DWPI Mincho'),
            ('ipamjm', 'IPAmj Mincho'),
        ],
        string="Glyph Font",
        default="dwpiexmincho",
        config_parameter='joo_glyph_fonts.font',
        help="Select the default font used for glyph rendering.",
    )
