from odoo import models


class ResPartner(models.Model):
    _inherit = [
        'res.partner',
        'joo.tofurengo.partner.name.mixin',
        'joo.tofurengo.partner.address.mixin',
    ]
