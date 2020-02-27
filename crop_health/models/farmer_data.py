# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FarmerDetails(models.Model):
    _name = "farmer.data"
    _description = "farmer details"
    _rec_name = "farmer_name"

    user_id = fields.Many2one('res.users')
    farmer_name = fields.Char(string='Name')
    farmer_mobile_no = fields.Char(string='Mobile No')
    farmer_email = fields.Char(string='Email')
    farmer_address = fields.Text(string='Address')

    @api.constrains('mobile_no')
    def _check_mobile_no(self):
        for record in self:
            if len(str(record.mobile_no)) < 10:
                raise ValidationError(
                    "Mobile no must be in 10 digits: %s" % record.mobile_no)
            else:
                raise ValidationError(
                    "Mobile no should not be greater then 10 digits: %s" % record.mobile_no)
