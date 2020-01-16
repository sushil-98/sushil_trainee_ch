from odoo import http
from odoo.http import request

class Agriexpert(http.Controller):
    @http.route('/agri/', auth="public", website=True, csrf=False)
    def index(self, **kw):
        Agriexperts = http.request.env['agriexpert.detail']
        return http.request.render('agri_app.index', {
    		'agriexpert': Agriexperts.search([])
    		})

    @http.route(['/agriexpert/edit/','/agriexpert/edit/<model("agriexpert.detail"):expert>'], auth="public", website=True, csrf=False)
    def update(self, expert=None):
        if expert:
            expert = http.request.env['agriexpert.detail'].browse([expert.id])
        return http.request.render('agri_app.create_record',{'expert':expert})
        
    @http.route(['/agriexpert/create/','/agriexpert/create/<int:expert>'], auth='public', website='True', method='post', csrf=False)
    def create(self, expert=None, **post):
        if post:
            if expert:
                http.request.env['agriexpert.detail'].browse([expert]).write(post)
            else:
                http.request.env['agriexpert.detail'].create(post)
        return http.request.redirect("/agri/")

    @http.route(['/agriexpert/delete/<model("agriexpert.detail"):expert>',], auth='public', website=True, csrf=False)
    def delete(self, expert):
        expert.unlink()
        return http.request.redirect('/agri/')

class FarmerInquiry(http.Controller):
    @http.route('/inquiry/', auth="public", website=True, csrf=False)
    def inquiry(self, **kW):
        Inquiries = http.request.env['farmer.inquiry.detail']
        return http.request.render('agri_app.inquiry', {
            'inquiry': Inquiries.search([])
            })
    
        
