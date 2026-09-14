from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    """
    Configuration settings for joo_web_fonts module.
    Allows selecting the default font used for glyph rendering in the system.
    """
    _inherit = 'res.config.settings'

    joo_font = fields.Selection(
        [
            ('dwpiexmincho', 'DWPI Extended Mincho'),
            ('dwpimincho', 'DWPI Mincho'),
            ('ipamjm', 'IPAmj Mincho'),
        ],
        string="Glyph Font",
        default="dwpiexmincho",
        help="Select the default font used for glyph rendering."
    )

    # ------------------------------------------------------------
    # Save configuration values
    # ------------------------------------------------------------
    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].set_param(
            'joo_web_fonts.font',
            self.joo_font
        )

    # ------------------------------------------------------------
    # Load configuration values
    # ------------------------------------------------------------
    @api.model
    def get_values(self):
        res = super().get_values()
        conf = self.env['ir.config_parameter'].sudo()

        res.update(
            joo_font=conf.get_param(
                'joo_web_fonts.font',
                'dwpiexmincho'  # Default font key (matches joo_web_fonts.css and FontController)
            ),
        )
        return res
