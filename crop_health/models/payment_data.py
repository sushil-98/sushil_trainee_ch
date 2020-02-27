# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime
import uuid


class PaymentDetail(models.Model):
    _name = "payment.data"
    _description = "payment details"
    _rec_name = 'inquiry_id'

    # active = fields.Boolean(default=True)
    name = fields.Char(string='Charge for')
    amount = fields.Float(string='Amount')
    description = fields.Text(string='Description', required=True)
    order_id = fields.Char(default=str(uuid.uuid4()))
    acquirer_ref = fields.Char()
    inquiry_id = fields.Many2one("farmer.inquiry", string='Problem')
    payment_status = fields.Selection([('done', 'Done'), ('fail', 'Fail'), ('pending', 'Pending')])
    transaction_current_date = fields.Date(default=datetime.today())
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

    @api.onchange('inquiry_id')
    def _onchange_GetData(self):
        if self.env.context.get('current_id'):
            self.inquiry_id = self.env.context.get('current_id')

    # @api.returns('self', lambda value: value.id)
    # def copy(self, default=None):
    #     default = dict(default or {}, name=("%s (Copy)") % self.name)
    #     return super(PaymentDetail, self).copy(default=default)
