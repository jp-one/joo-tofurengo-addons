from odoo import http
from odoo.http import request


class FontController(http.Controller):
    """
    Controller for retrieving the configured web font for the joo_glyph_fonts module.
    This endpoint is called by font_loader.js to dynamically apply the selected font
    to elements using the 'joo-font' CSS class.
    """

    @http.route('/joo_glyph_fonts/font', type='jsonrpc', auth='user')
    def get_font(self):
        """
        Return the configured font key stored in ir.config_parameter.
        Only authenticated users can access this value as part of system configuration.
        """
        return request.env['ir.config_parameter'].sudo().get_param(
            'joo_glyph_fonts.font',
            'dwpiexmincho'  # Default font key (matches default font-family defined in joo_glyph_fonts.css)
        )
