# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
from datetime import datetime
import json
from werkzeug import urls
from . import checksum

from odoo import http
from odoo.http import request


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
            Agriexpert = http.request.env['agriexpert.data'].sudo().search(
                [('specialist', 'in', [post.get('specialist')])])
        else:
            Agriexpert = http.request.env['agriexpert.data'].sudo().search([])
        return http.request.render("crop_health.index", {
            'agriexpert': Agriexpert
        })

    @http.route('/schedule/record/<int:expert_id>', auth='public', type="http", csrf=False)
    def schedule(self, expert_id=0, **kw):
        if expert_id:
            ag = http.request.env['agriexpert.data'].sudo().browse([expert_id])
            Schedule = http.request.env['agriexpert.schedule'].sudo().search(
                [('schedule_id', '=', ag.id)])
        return http.request.render("crop_health.schedule", {'schedule': Schedule, 'expert_id': expert_id})


class FarmerInquiry(http.Controller):
    @http.route('/inquiry/<int:expert_id>', auth='public', type="http", csrf=False)
    def inquiry(self, expert_id=0, **kw):
        Inquiries = http.request.env['farmer.inquiry'].sudo().search(
            [('create_uid', '=', request.session.uid)])
        return http.request.render('crop_health.inquiry_detail', {
            'inquiry': Inquiries,
            'expert_id': expert_id
        })

    @http.route(['/inquiry/edit/<int:expert_id>', '/inquiry/edit/<model("farmer.inquiry"):inq>'], auth="public", website=True, type="http", csrf=False)
    def update(self, inq=None, expert_id=0):
        if inq:
            inq = http.request.env['farmer.inquiry'].sudo().browse([inq.id])
        return http.request.render('crop_health.new_inquiry', {'inq': inq, 'expert_id': expert_id})

    @http.route('/inquirydata/<int:expert_id>', auth="public", website=True, type="http", csrf=False)
    def user_inquiry(self, expert_id=0, **kw):
        Inquiries = http.request.env['farmer.inquiry'].sudo().search(
            [('create_uid', '=', request.session.uid)])
        return http.request.render('crop_health.user_inquiry', {
            'inquiry': Inquiries,
            'expert_id': expert_id
        })

    @http.route(['/inquiry/create/<int:expert_id>', '/inquiry/create/<int:inq>'], auth='public', website=True, methods=['POST'], type="http", csrf=False)
    def create(self, inq=None, expert_id=0, **post):
        if expert_id:
            ai = request.env['agriexpert.data'].sudo().search([('id', '=', expert_id)])
            if post.get('image'):
                if inq:
                    http.request.env['crop.data'].sudo().browse([inq]).write({
                        'crop_name': post.get('crop_name'),
                        'seed_name': post.get('seed_name'),
                        'seed_no': post.get('seed_no'),
                        })
                    file_name = post.get('image')
                    path = '/home/sushil/Pictures/' + file_name
                    image = open(path, 'rb')
                    http.request.env['farmer.inquiry'].sudo().browse([inq]).write({
                        'problem': post.get('problem'),
                        'image': base64.encodestring(image.read()),
                        })
                else:
                    # if expert_id:
                    #     ai = request.env['agriexpert.data'].sudo().search([('id', '=', expert_id)])
                    fmr = request.env['farmer.data'].sudo().search([('user_id', '=', request.session.uid)])
                    file_name = post.get('image')
                    path = '/home/sushil/Pictures/' + file_name
                    image = open(path, 'rb')
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

    @http.route('/payment/<int:inq_id>', auth="public", website=True, type="http", csrf=False)
    def user_payment(self, inq_id=0, **post):
        if inq_id:
            inq = http.request.env['farmer.inquiry'].sudo().browse([inq_id])
            Payment = http.request.env['payment.data'].sudo().search(
                [('inquiry_id', '=', inq.id)])
        return http.request.render('crop_health.payment_data', {'payment': Payment})

    @http.route('/make_payment', auth="public", type="http", website=True, methods=['POST'], csrf=False)
    def payment(self, **kw):
        order = request.env['payment.data'].sudo().browse([int(kw.get('payment_id'))])
        print ("\n\n\n\n\n\n", order, "..............\n\n\n\n\n")
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        data_dict = {
            'MID': 'amitgo59443067266036',
            'WEBSITE': 'WEBSTAGING',  # fix value
            'ORDER_ID': order.order_id,
            'CUST_ID': str(request.uid),
            'INDUSTRY_TYPE_ID': 'Retail',  # fix value
            'CHANNEL_ID': 'WEB',  # fix value
            'TXN_AMOUNT': str(float(order.amount)),
            'CALLBACK_URL': urls.url_join(base_url, '/paytm_response')
            }
        data_dict['CHECKSUMHASH'] = checksum.generate_checksum(data_dict, 'bQfzzkKzeCbR7jOl')
        data_dict['redirection_url'] = " https://securegw-stage.paytm.in/order/process"
        return request.make_response(json.dumps(data_dict))

    @http.route('/paytm_response', auth="public", type="http", website=True, method='post', csrf=False)
    def paytm_response(self, **post):
        print ("\n\n\n\n\n\npayment", post, "\n\n\n\n\ndone")
        checksum_result = checksum.verify_checksum(post, "bQfzzkKzeCbR7jOl", post.get('CHECKSUMHASH'))
        print ("\n\n\n\nchecksum verified", checksum_result, "\n\n\ndone")
        payment = request.env['payment.data'].sudo().search([('order_id', '=', post.get('ORDERID'))])
        print ("\n\n\n\npayment process result", payment)
        if checksum_result:
            if post.get('STATUS') == "TXN_SUCCESS":
                payment.write({
                    'payment_status': 'done',
                    'acquirer_ref': post.get('TXNID'),
                    'transaction_current_date': datetime.today()
                    })
            elif post.get('STATUS') == "TXN_FAILURE":
                payment.write({
                    'payment_status': 'fail',
                    })
            elif post.get('STATUS') == "PENDING":
                payment.write({
                    'payment_status': 'pending',
                    })
        return request.render('crop_health.payment_process', {'payment': payment})
        # return utils.redirect('/homepage')"/payment/confirm/{{ payment.id }}"

    @http.route('/payment/confirm/<int:inq_id>', auth="public", website=True, type="http", csrf=False)
    def payment_confirm(self, inq_id=0, **post):
        if inq_id:
            inq = http.request.env['farmer.inquiry'].sudo().browse([inq_id])
            Payment = http.request.env['agriexpert.observation'].sudo().search(
                [('inquiry_id', '=', int(inq.id))])
        return http.request.render('crop_health.payment_confirm', {'treatment': Payment})
