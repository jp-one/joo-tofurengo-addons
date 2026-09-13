# from odoo import http


# class JooPartnerTofurengo(http.Controller):
#     @http.route('/joo_partner_tofurengo/joo_partner_tofurengo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/joo_partner_tofurengo/joo_partner_tofurengo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('joo_partner_tofurengo.listing', {
#             'root': '/joo_partner_tofurengo/joo_partner_tofurengo',
#             'objects': http.request.env['joo_partner_tofurengo.joo_partner_tofurengo'].search([]),
#         })

#     @http.route('/joo_partner_tofurengo/joo_partner_tofurengo/objects/<model("joo_partner_tofurengo.joo_partner_tofurengo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('joo_partner_tofurengo.object', {
#             'object': obj
#         })

