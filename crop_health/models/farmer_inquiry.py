# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class FarmerInquiry(models.Model):
    _name = "farmer.inquiry"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "farmer inquiry details"
    _rec_name = 'problem'

    def inquiry(self):
        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'agriexpert.observation',
            'target': 'current',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }

    def button_new(self):
        for rec in self:
            # rec.state = 'new'
            rec.write({'state': 'new'})

    def button_confirm(self):
        for rec in self:
            rec.write({'state': 'confirm'})

    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})

    problem = fields.Text(string='Problem Name', required=True)
    crop_id = fields.Many2one(
        'crop.data', string='Crop', ondelete='cascade')
    image = fields.Binary()
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )
    farmer_id = fields.Many2one('farmer.data')
    expert_id = fields.Many2one(
        'agriexpert.data', ondelete='cascade', string='Select AgriExpert')
    color = fields.Integer()
    state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], required=True, default='new')
    farmer_name = fields.Char(string='Name', related="farmer_id.farmer_name")
    farmer_mobile_no = fields.Char(string='Mobile No', related="farmer_id.farmer_mobile_no")
    farmer_email = fields.Char(string='Email', related="farmer_id.farmer_email")
    farmer_address = fields.Text(string='Address', related="farmer_id.farmer_address")

    crop_name = fields.Char(string='Crop Name', related="crop_id.crop_name")
    seed_name = fields.Char(string='Seed Name', related="crop_id.seed_name")
    seed_no = fields.Char(string='Seed No', related="crop_id.seed_no")
