# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ExpertObservation(models.Model):
    _name = "agriexpert.observation"
    _description = "Observation details"
    _rec_name = 'inquiry_id'

    solution = fields.Boolean(string='Treatment')
    # farmer_id = fields.Many2one(
    #     comodel_name='farmer.data', string='Farmer Name')
    treatment = fields.Char(string='Give Treatment')
    detail = fields.Text(string='Detail')
    physical = fields.Boolean(string='Observation')
    observation = fields.Datetime(string='Observation Date & Time', store=True)
    description = fields.Char(string='Description')
    inquiry_id = fields.Many2one("farmer.inquiry", string='Problem')
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

    @api.onchange('inquiry_id')
    def _onchange_GetData(self):
        if self.env.context.get('current_id'):
            self.inquiry_id = self.env.context.get('current_id')

    def inquiry_charge(self):
        return{
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'payment.data',
            'target': 'current',
            'res_id': False,
            'type': 'ir.actions.act_window',
            'context': {'current_id': self.id}
        }
