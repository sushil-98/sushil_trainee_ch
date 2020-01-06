from odoo import api, fields, models


class HeaderDemo(models.Model):
    _name = "header.demo"
    _description = "header description"


    def button_confirmed(self):
        for rec in self:
            rec.write({'state': 'confirmed'})

    def button_draft(self):
        for rec in self:
            rec.state = 'draft'

    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})

    name = fields.Char(string='Name', required=True)
    mobile_no = fields.Char(string='Mobile No', required=True)
    date_of_birth = fields.Date(string='Date Of Birth', required=True)
    start_date = fields.Date(string='starting date', required=True)
    end_date = fields.Date(string='end date', required=True)

    state = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], required=True, default='confirmed')
        