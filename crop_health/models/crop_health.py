from odoo import api, fields, models
from odoo.exceptions import ValidationError
import base64
from odoo import modules
from datetime import datetime

class AgriExpert(models.Model):
	_name="agriexpert.data"
	_description="agri expert details"

	name = fields.Char(string='Enter name', required=True)
	degree = fields.Char(string='Enter your degree', required=True)
	license_no = fields.Char(digits=(9, 6), string='Enter your license Number', required=True)
	specialist = fields.Selection([
		('wheat-specialist','Wheat-Specialist'),
		('beans-specialist','Beans-Specialist'),
		('tomato-specialist','Tomato-Specialist'),
		('potato-specialist','Potato-Specialist'),
		('cron-specialist','Cron-specialist'),
		],'Specialist')
	description = fields.Text(string='Description', help="enter something more about farmer")
	schedule_ids = fields.One2many('agriexpert.schedule', inverse_name="schedule_id", string='Schedule', ondelete="cascade")
	company_id = fields.Many2one(
		'res.company', required=True, default=lambda self: self.env.company
		)
	
	@api.constrains('license_no')
	def _check_license_no(self):
		for record in self:
			if len(str(record.license_no)) >= 9:
				raise ValidationError("license no must be less then 9 digits: %s" % record.license_no)
			elif len(str(record.license_no)) <= 6:
				raise ValidationError("license no must be greater then 6 digits: %s" % record.license_no)


class ExpertSchedule(models.Model):
	_name = "agriexpert.schedule"
	_description = "expert schedule availability"
	
	day_from = fields.Selection([
		('monday','Monday'),
		('tuesday','Tuesday'),
		('wednesday','Wednesday'),
		('thursday','Thursday'),
		('friday','Friday'),
		('saturday','saturday'),
		],'Day From',default='Day From')
	time_from = fields.Float(string='Time from')
	day_to = fields.Selection([
		('monday','Monday'),
		('tuesday','Tuesday'),
		('wednesday','Wednesday'),
		('thursday','Thursday'),
		('friday','Friday'),
		('saturday','saturday'),
		],'Day To',default='Day To')
	time_to = fields.Float(string='Time to')
	schedule_id = fields.Many2one("agriexpert.data",string="Schedule", ondelete="cascade")
	company_id = fields.Many2one(
		'res.company', required=True, default=lambda self: self.env.company
		)

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


class ExpertObservation(models.Model):
	_name = "agriexpert.observation"
	_description = "Observation details"

	solution = fields.Boolean(string='Treatment')
	farmer_id = fields.Many2one(comodel_name='farmer.data', string='Farmer Name')
	treatment = fields.Char(string='Give Treatment')
	detail = fields.Text(string='Detail')
	phisical = fields.Boolean(string='Observation')
	observation = fields.Datetime(string='Observation Date & Time',store=True)
	description = fields.Char(string='Description')
	company_id = fields.Many2one(
		'res.company', required=True, default=lambda self: self.env.company
		)

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
				raise ValidationError("Mobile no must be in 10 digits: %s" % record.mobile_no)
			else:
				raise ValidationError("Mobile no should not be greater then 10 digits: %s" % record.mobile_no)

class FarmerInquiry(models.Model):
	_name = "farmer.inquiry"
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "farmer inquiry details"
	
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
	crop_id = fields.Many2one('crop.data', string='Crop Name', ondelete='cascade')
	image = fields.Binary()
	company_id = fields.Many2one(
		'res.company', required=True, default=lambda self: self.env.company
		)
	farmer_id = fields.Many2one('farmer.data')
	expert_id = fields.Many2one('agriexpert.data', ondelete='cascade', string='Select AgriExpert')
	color = fields.Integer()
	state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
        ], required=True, default='new')
	farmer_name = fields.Char(string='Name' ,related="farmer_id.farmer_name")
	farmer_mobile_no = fields.Char(string='Mobile No' ,related="farmer_id.farmer_mobile_no")
	farmer_email = fields.Char(string='Email' ,related="farmer_id.farmer_email")
	farmer_address = fields.Text(string='Address' ,related="farmer_id.farmer_address")


class PaymentDetail(models.Model):
	_name = "payment.data"
	_description = "payment details"

	amount = fields.Float(string='Treatment Charge')
	description = fields.Text(string='Description', required=True)
	company_id = fields.Many2one(
		'res.company', required=True, default=lambda self: self.env.company
		)