from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AgriExpert(models.Model):
	_name="agriexpert.data"
	_description="agri expert details"

	name = fields.Char(string='Enter name', required=True)
	degree = fields.Char(string='Enter your degree', required=True)
	license_no = fields.Char(digits=(9, 6), string='Enter your license Number', required=True)
	specialist = fields.Selection([
		('wheet-specialist','Wheet-Specialist'),
		('beans-specialist','Beans-Specialist'),
		('cron-specialist','Cron-specialist'),
		],'Specialist')
	description = fields.Text(string='Description', help="enter something more about farmer")
	color = fields.Integer()

	@api.constrains('license_no')
	def _check_license_no(self):
		for record in self:
			if len(str(record.license_no)) >= 9:
				raise ValidationError("license no must be less then 9 digits: %s" % record.license_no)
			elif len(str(record.license_no)) <= 6:
				raise ValidationError("license no must be greater then 6 digits: %s" % record.license_no)


class CropDetails(models.Model):
	_name = "crop.data"
	_description = "crop details"

	name = fields.Char(string='Crop Name', required=True)
	seed_name = fields.Char(string='Seed Name', required=True)
	seed_no = fields. Char(string='Seed No', required=True)

class ExpertSchedule(models.Model):
	_name = "agriexpert.schedule"
	_description = "expert schedule availability"

	day_from = fields.Selection([
		('monday','Monday'),
		('tuesday','Tuesday'),
		('wednesday','Wednesday'),
		('thirsday','Thirsday'),
		('friday','Friday'),
		('saturday','saturday'),
		],'Day From',default='Day From')
	time_from = fields.Datetime(string='Time From', default=fields.Datetime.now, required=True)
	day_to = fields.Selection([
		('monday','Monday'),
		('tuesday','Tuesday'),
		('wednesday','Wednesday'),
		('thirsday','Thirsday'),
		('friday','Friday'),
		('saturday','saturday'),
		],'Day To',default='Day To')
	time_to = fields.Datetime(string='Time To', default=fields.Datetime.now, required=True)



class ExpertObservation(models.Model):
	_name = "agriexpert.observation"
	_description = "Observation details"

	treatment = fields.Char(string='Treatment', required=True)
	detail = fields.Text(string='Detail', required=True)
	observation = fields.Datetime(string='Observation Date & Time', required=True)
		

class FarmerDetails(models.Model):
	_name = "farmer.data"
	_description = "farmer details"	

	name = fields.Char(string='Enter your name', required=True)
	mobile_no = fields.Char(string='Enter your mobile no', required=True)
	email = fields.Char(string='Email', required=True)
	address = fields.Text(string='Enter your address', required=True)

	@api.constrains('mobile_no')
	def _check_mobile_no(self):
		for record in self:
			if len(str(record.mobile_no)) < 10:
				raise ValidationError("Mobile no must be in 10 digits: %s" % record.mobile_no)
			elif len(str(record.mobile_no)) > 10:
				raise ValidationError("Mobile no must not be greater then 10 digits: %s" % record.mobile_no)


class FarmerInquiry(models.Model):
	_name = "farmer.inquiry"
	_description = "farmer inquiry details"	

	def button_newinq(self):
		for rec in self:
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
	crop_id = fields.Many2many(comodel_name='crop.data', string='Crop Name', ondelete='cascade', required=True)
	image = fields.Binary()

	expert_id = fields.Many2one(comodel_name='agriexpert.data', ondelete='cascade', string='Select AgriExpert')

	state = fields.Selection([
        ('new', 'New'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
        ], default="new")
