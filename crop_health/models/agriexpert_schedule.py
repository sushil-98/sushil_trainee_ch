# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ExpertSchedule(models.Model):
    _name = "agriexpert.schedule"
    _description = "expert schedule availability"

    day_from = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'saturday'),
    ], 'Day From', default='Day From')
    time_from = fields.Float(string='Time from')
    day_to = fields.Selection([
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'saturday'),
    ], 'Day To', default='Day To')
    time_to = fields.Float(string='Time to')
    schedule_id = fields.Many2one(
        "agriexpert.data", string="Schedule", ondelete="cascade")
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda self: self.env.company
    )
