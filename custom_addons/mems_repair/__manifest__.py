{
    'name': 'MEMs Repair',
    'summary': 'Medical Equipment Repair',
    'description': '',
    'category': 'Custom',
    'version': '0.1',
    'author': 'Appcode Technology',
    'website': 'http://www.appcode.co.th/mems',
    'depends': ['base', 'mail', 'mems_equipment'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/paper_format.xml',
        'report/workorder_form.xml',
        'report/sr_form.xml',
        'data/sequence.xml',
        'data/email_data.xml',
        'views/menu.xml',
        'views/sr_view.xml',
        'views/workorder_view.xml',
        'views/workorder_tracking_view.xml',
        'wizard/wo_approve_wizard.xml',
        'wizard/wo_cancel_wizard.xml',
        'wizard/wo_close_wizard.xml',
        'wizard/wo_revise_wizard.xml',
        'wizard/sr_cancel_wizard.xml',
        'wizard/sr_approve_wizard.xml',
    ],
    'demo': [],
}
