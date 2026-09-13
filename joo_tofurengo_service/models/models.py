# from odoo import models, fields, api


# class joo_tofurengo_service(models.Model):
#     _name = 'joo_tofurengo_service.joo_tofurengo_service'
#     _description = 'joo_tofurengo_service.joo_tofurengo_service'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

