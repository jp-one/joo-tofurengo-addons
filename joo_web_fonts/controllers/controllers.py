# from odoo import http


# class JooWebFonts(http.Controller):
#     @http.route('/joo_web_fonts/joo_web_fonts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/joo_web_fonts/joo_web_fonts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('joo_web_fonts.listing', {
#             'root': '/joo_web_fonts/joo_web_fonts',
#             'objects': http.request.env['joo_web_fonts.joo_web_fonts'].search([]),
#         })

#     @http.route('/joo_web_fonts/joo_web_fonts/objects/<model("joo_web_fonts.joo_web_fonts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('joo_web_fonts.object', {
#             'object': obj
#         })

