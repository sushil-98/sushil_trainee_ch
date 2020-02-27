# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CropDetails(models.Model):
    _name = "crop.data"
    _description = "crop details"
    _rec_name = "crop_name"

    crop_name = fields.Char(string='Crop Name', required=True)
    seed_name = fields.Char(string='Seed Name', required=True)
    seed_no = fields. Char(string='Seed No', required=True)
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )
