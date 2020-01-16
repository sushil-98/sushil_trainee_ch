from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

class AgriExpert(models.Model):
	_name="agriexpert.detail"
	_description="agri expert details"
	# _rec_name="specialist"

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


class FarmerDetails(models.Model):
	_name = "farmer.detail"
	_description = "farmer details"	

	name = fields.Char(string='Enter your name', required=True)
	mobile_no = fields.Char(string='Enter your mobile no', required=True)
	email = fields.Char(string='Email', required=True)
	address = fields.Char(string='Enter your address', required=True)

	@api.constrains('mobile_no')
	def _check_mobile_no(self):
		for record in self:
			if len(str(record.mobile_no)) < 10:
				raise ValidationError("Mobile no must be in 10 digits: %s" % record.mobile_no)
			elif len(str(record.mobile_no)) > 10:
				raise ValidationError("Mobile no must not be greater then 10 digits: %s" % record.mobile_no)


class CropDetails(models.Model):
	_name = "crop.detail"
	_description = "crop details"

	name = fields.Char(string='Crop Name', required=True)
	seed_name = fields.Char(string='Seed Name', required=True)
	seed_no = fields. Char(string='Seed No', required=True)
		

class FarmerInquiry(models.Model):
	_name = "farmer.inquiry.detail"
	_description = "farmer inquiry details"	
			

	problem = fields.Text(string='Problem Name', required=True)
	crop_id = fields.Many2many(comodel_name='crop.detail', string='Crop Name', ondelete='cascade', required=True)
	image = fields.Binary()

	expert_id = fields.Many2one(comodel_name='agriexpert.detail', ondelete='cascade', string='Select AgriExpert')
	

class ExpertSchedule(models.Model):
	_name = "agriexpert.availability"
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

			
class FarmerInquiryWizard(models.TransientModel):
    _name = 'farmer.inquiry.wizard'
    _description = "farmer inquiry wizard view"


    def _default_inquiry(self):
        return self.env['farmer.inquiry.detail'].browse(self._context.get('active_id'))

    inquiry_id = fields.Many2one(comodel_name='farmer.inquiry.detail', string='Add inquiry', ondelete='cascade', required=True)
    expert_ids = fields.Many2one(comodel_name='agriexpert.detail', string="Send inquiry to", ondelete='cascade', required=True)

    def subscribe(self):
        # self.inquiry_id
        self.inquiry_id.expert_ids |= self.expert_ids
        return {}
