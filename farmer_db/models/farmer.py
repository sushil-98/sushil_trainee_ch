from odoo import api, fields, models
from odoo.exceptions import ValidationError

class AgriExpert(models.Model):
	_name="agriexpert.agriexpert.type"
	_description="farmer_description"
	# _rec_name="specialist"

	name = fields.Char(string='Enter name', required=True)
	degree = fields.Char(string='Enter your degree', required=True)
	license = fields.Char(digits=(9, 6), string='Enter your license Number', required=True)
	specialist = fields.Char(string='Specialist', required=True)
	description = fields.Text(string='Description', help="enter something more about farmer")

	@api.constrains('license')
	def _check_license(self):
		for record in self:
			if len(str(record.license)) >= 9:
				raise ValidationError("license no must be less then 9 digits: %s" % record.license)
			elif len(str(record.license)) <= 6:
				raise ValidationError("license no must be greater then 6 digits: %s" % record.license)

class FarmerDetails(models.Model):
	_name = "farmer.details"

	name = fields.Char(string='Enter your name', required=True)
	crop_name = fields.Char(string='Crop Name', required=True)
	biaran_name = fields.Char(string='Biaran Name', required=True)
	biaran_no = fields.Integer(digits=(8,6), string='Enter biaran no', required=True)

	@api.constrains('biaran_no')
	def _check_biaran_no(self):
		for record in self:
			if len(str(record.biaran_no)) <= 8:
				raise ValidationError("biaran no must be in digits: %s" % record.biaran_no)


class FarmerInquiry(models.Model):
	_name = "farmer.inquiry"
	# _inherit = "agriexpert.agriexpert.type"
	_description = "description"				

	problem = fields.Char(string='Problem Name', required=True)
	crop_name = fields.Char(string='Crop Name', required=True)
	image = fields.Binary()
	description = fields.Text(string='Description', required=True)
	# specialist = fields.Char(string='Specialist', required=True)

	agri_ex_id = fields.Many2one(comodel_name='agriexpert.agriexpert.type', ondelete='cascade', string='Select AgriExpert')
	agri_specialist = fields.Char(string='specialist', compute='_compute_agri_specialist')

	@api.depends('agri_ex_id')
	def _compute_agri_specialist(self):
		for record in self:
			record.agri_specialist = "specialist of: %s" % record.agri_ex_id

