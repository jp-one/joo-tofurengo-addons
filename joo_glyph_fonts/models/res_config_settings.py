from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_glyph_fonts module.
    Configures the primary web font applied to elements with the 'joo-font' class.
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
        help="Select the font applied to UI elements using the 'joo-font' class.",
    )
