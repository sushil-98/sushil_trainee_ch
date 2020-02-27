# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.addons.web.controllers.main import Home
from odoo.http import request


class Home(Home):
    def _login_redirect(self, uid, redirect=None):
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('crop_health.group_agriexpert'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_user'):
            return '/web/'
        if request.session.uid and request.env['res.users'].sudo().browse(request.session.uid).has_group('base.group_portal'):
            return '/homepage'
        return super(AgriexpertRegister, self)._login_redirect(uid, redirect=redirect)


class AgriexpertRegister(http.Controller):
    @http.route('/home/', auth="public", type="http", csrf=False)
    def user_home(self, **kw):
        return http.request.render('crop_health.crophealth_home', {})

    @http.route('/userregister/', auth="public", type="http", csrf=False)
    def agriexpert_register(self, **kw):
        currency = http.request.env['res.currency'].sudo().search([])
        return http.request.render('crop_health.user_register', {'currency': currency})

    @http.route('/userregister/form', auth="public", type="http", csrf=False)
    def user_login(self, **post):
        groups_id_name = [(6, 0, [request.env.ref('crop_health.group_agriexpert').id, request.env.ref('base.group_user').id])]

        currency_name = post.get('currency')
        currency = request.env['res.currency'].sudo().search([('name', '=', currency_name)], limit=1)
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email')
            })
        company = request.env['res.company'].sudo().create({
            'name': post.get('name'),
            'partner_id': partner.id,
            'currency_id': currency.id,
            })

        request.env['res.users'].sudo().create({
            'partner_id': partner.id,
            'login': post.get('name'),
            'password': post.get('password'),
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'groups_id': groups_id_name,
            })
        return http.local_redirect('/web/login')
