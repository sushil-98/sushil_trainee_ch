{
    'name': 'Crop Health',
    'version': '1.1',
    'summary': 'Agriculture Application',

    'depends': ['base', 'portal', 'web_dashboard'],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/crop_data.xml',
        'views/farmer_data.xml',
        'views/agriexpert_data.xml',
        'views/agriexpert_schedule.xml',
        'views/agriexpert_observation.xml',
        'views/farmer_inquiry.xml',
        'views/payment_data.xml',
        'views/crop_health_menu.xml',
        'views/crop_health_template.xml',
        'views/res_config_settings_views.xml',
        'views/user_portal.xml',
        # 'report/report.xml',
        # 'wizard/farmerinquiry_wizard.xml',
    ],

    'demo': [
        # 'demo/demo_data.xml',
    ],
}
