{
	'name' : 'Crop Health',
	'version' : '1.1',
	'summary' : 'Agriculture Application',

	'depends': ['portal','web_dashboard'],

	'data' : [
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/crop_health_details.xml',
		'views/crop_health_template.xml',
		'views/user_portal.xml',
		'report/report.xml',
		# 'wizard/farmerinquiry_wizard.xml',
	],

	'demo': [
        # 'demo/demo_data.xml',
    ],
}
