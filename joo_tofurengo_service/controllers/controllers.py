# from odoo import http


# class JooTofurengoService(http.Controller):
#     @http.route('/joo_tofurengo_service/joo_tofurengo_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/joo_tofurengo_service/joo_tofurengo_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('joo_tofurengo_service.listing', {
#             'root': '/joo_tofurengo_service/joo_tofurengo_service',
#             'objects': http.request.env['joo_tofurengo_service.joo_tofurengo_service'].search([]),
#         })

#     @http.route('/joo_tofurengo_service/joo_tofurengo_service/objects/<model("joo_tofurengo_service.joo_tofurengo_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('joo_tofurengo_service.object', {
#             'object': obj
#         })

