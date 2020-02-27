# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AgriExpert(models.Model):
    _name = "agriexpert.data"
    _description = "agri expert details"

    name = fields.Char(string='Enter name', required=True)
    degree = fields.Char(string='Enter your degree', required=True)
    license_no = fields.Char(
        digits=(9, 6), string='Enter your license Number', required=True)
    specialist = fields.Selection([
        ('wheat_specialist', 'Wheat Specialist'),
        ('beans_specialist', 'Beans Specialist'),
        ('tomato_specialist', 'Tomato Specialist'),
        ('potato_specialist', 'Potato Specialist'),
        ('cron_specialist', 'Cron specialist'),
    ], 'Specialist')
    description = fields.Text(string='Description', help="enter something more about farmer")
    schedule_ids = fields.One2many(
        'agriexpert.schedule', inverse_name="schedule_id", string='Schedule', ondelete="cascade")
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )

    @api.constrains('license_no')
    def _check_license_no(self):
        for record in self:
            if len(str(record.license_no)) >= 9:
                raise ValidationError(
                    "license no must be less then 9 digits: %s" % record.license_no)
            elif len(str(record.license_no)) <= 6:
                raise ValidationError(
                    "license no must be greater then 6 digits: %s" % record.license_no)