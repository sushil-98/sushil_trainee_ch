from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import Home
import base64

class CustomerRegister(http.Controller):
    @http.route('/customer/', auth="public", type="http", csrf=False)
    def portal_user(self, **kw):
        return http.request.render('crop_health.portal_user', {})

    @http.route('/customer/form', auth="public", type="http", csrf=False)
    def customer_register(self, **post):
        groups_id_name = [(6, 0, [request.env.ref('base.group_portal').id])]

        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email')
            })
        fid = request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('name'),
            'password': post.get('password'),
            'groups_id': groups_id_name,
            })
        request.env['farmer.data'].sudo().create({
            'farmer_name': post.get('name'),
            'farmer_mobile_no': post.get('mobile_no'),
            'farmer_email': post.get('email'),
            'farmer_address': post.get('address'),
            'user_id': fid.id
            })
        return http.local_redirect('/web/login')

    @http.route(['/homepage', '/search/<string:spec>'], auth='public', type="http", csrf=False)
    def render_home(self, spec=None, **post):
        if spec:
            Agriexpert = http.request.env['agriexpert.data'].sudo().search([('specialist', 'in', [post.get('specialist')])])
        else:
            Agriexpert = http.request.env['agriexpert.data'].sudo().search([])
        return http.request.render("crop_health.index", {
            'agriexpert': Agriexpert
            })

    @http.route('/schedule/record/<int:expert_id>', auth='public', type="http", csrf=False)
    def schedule(self, expert_id=0, **kw):
        if expert_id:
            ag = http.request.env['agriexpert.data'].sudo().browse([expert_id])
            Schedule = http.request.env['agriexpert.schedule'].sudo().search([('schedule_id','=',ag.id)])
        return http.request.render("crop_health.schedule", {'schedule': Schedule, 'expert_id':expert_id})


class FarmerInquiry(http.Controller):
    @http.route('/inquiry/<int:expert_id>', auth='public', type="http", csrf=False)
    def inquiry(self, expert_id=0, **kw):
        Inquiries = http.request.env['farmer.inquiry'].sudo().search([('create_uid','=',request.session.uid)])
        return http.request.render('crop_health.inquiry_detail', {
            'inquiry': Inquiries,
            'expert_id' : expert_id
            })

    @http.route(['/inquiry/edit/<int:expert_id>','/inquiry/edit/<model("farmer.inquiry"):inq>'], auth="public", website=True, type="http", csrf=False)
    def update(self, inq=None, expert_id=0):
        Inquiries = http.request.env['farmer.inquiry'].sudo().search([])
        if inq:
            inq = http.request.env['farmer.inquiry'].sudo().browse([inq.id])
        return http.request.render('crop_health.new_inquiry',{'inq':inq,'expert_id':expert_id})

    @http.route('/inquirydata/<int:expert_id>', auth="public", website=True, type="http", csrf=False)
    def user_inquiry(self, expert_id=0, **kw):
        Inquiries = http.request.env['farmer.inquiry'].sudo().search([('create_uid','=',request.session.uid)])
        return http.request.render('crop_health.user_inquiry',{
            'inquiry': Inquiries,
            'expert_id' : expert_id
            })

    @http.route('/inquiry/create/<int:expert_id>', auth='public', website=True, method='post', type="http", csrf=False)
    def create(self, inq=None, expert_id=0, **post):
        file = []
        if expert_id:
            ai = request.env['agriexpert.data'].sudo().search([('id','=',expert_id)])
        fmr = request.env['farmer.data'].sudo().search([('user_id','=',request.session.uid)])
        file_name = post.get('image')
        path = '/home/sushil/Pictures/' + file_name
        image = open(path,'rb')
        crop = http.request.env['crop.data'].sudo().create({
            'crop_name': post.get('crop_name'),
            'seed_name': post.get('seed_name'),
            'seed_no': post.get('seed_no'),
            'company_id': ai.company_id.id,
            })
        http.request.env['farmer.inquiry'].sudo().create({
            'problem': post.get('problem'),
            'company_id': ai.company_id.id,
            'expert_id': ai.id,
            'farmer_id': fmr.id,
            'crop_id': crop.id,
            'image': base64.encodestring(image.read()),
            })
        return http.request.redirect('/inquirydata/'+str(expert_id))

    @http.route(['/inquiry/delete/<model("farmer.inquiry"):inq>'], auth='public', website=True, type="http", csrf=False)
    def delete(self, inq, expert_id=0):
        inq.sudo().unlink()
        return http.request.redirect('/inquirydata/'+str(expert_id))