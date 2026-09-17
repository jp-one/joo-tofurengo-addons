from odoo import models


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = [
        'res.partner',
        'joo.tofurengo.partner.kana.mixin',
        'joo.tofurengo.partner.name.mixin',
        'joo.tofurengo.partner.address.mixin',
    ]
    _order = "family_kana, given_kana, name, id"
