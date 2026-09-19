from odoo import models, fields

PARAM_FURIGANA_TYPE = 'joo_partner_furigana.furigana_type'
DEFAULT_FURIGANA_TYPE = 'hiragana'

class ResConfigSettings(models.TransientModel):
    """
    Extend ResConfigSettings to expose furigana normalization setting in the UI.
    """
    _inherit = 'res.config.settings'

    joo_furigana_type = fields.Selection(
        selection=[
            ('none', 'None'),
            ('hiragana', 'HIRAGANA'),
            ('katakana', 'KATAKANA'),
        ],
        string="Furigana Normalization Type",
        config_parameter=PARAM_FURIGANA_TYPE,
        default=DEFAULT_FURIGANA_TYPE,
        help="Choose the default normalization format for partner furigana."
    )

# ----------------------------------------------------------------------
# System Settings Helper
# ----------------------------------------------------------------------
def get_furigana_type_setting(model: models.Model) -> str:
    """
    Fetch the furigana normalization type from system parameters.
    Possible values: 'hiragana', 'katakana', 'none'.
    """
    param = model.env['ir.config_parameter'].sudo().get_param(
        PARAM_FURIGANA_TYPE, DEFAULT_FURIGANA_TYPE
    )
    return param if param in ('hiragana', 'katakana', 'none') else DEFAULT_FURIGANA_TYPE
