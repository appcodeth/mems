{
    'name': 'MEMs Equipment',
    'version': '0.1',
    'author': 'Appcode Technology',
    'website': 'http://www.appcode.co.th/mems',
    'category': 'Custom',
    'depends': ['base', 'mems_master', 'mems_purchase'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/pm_checklist_data.xml',
        'data/ca_checklist_data.xml',
        'data/receive_type_data.xml',
        'data/equipment_reason_data.xml',
        # 'data/equipment_data.xml',
        'report/paper_format.xml',
        'report/equipment_form.xml',
        'report/equipment_qrcode.xml',
        'report/pm_form.xml',
        'report/calibrate_form.xml',
        'views/menu.xml',
        'views/equipment_view.xml',
        'views/equipment_reason_view.xml',
        'views/calibrate_view.xml',
        'views/pm_view.xml',
        'views/pm_checklist_view.xml',
        'views/ca_checklist_view.xml',
        'views/receive_type_view.xml',
        'wizard/equipment_adjust_wizard.xml',
        'wizard/equipment_cancel_wizard.xml',
        'wizard/pm_approve_wizard.xml',
        'wizard/pm_cancel_wizard.xml',
        'wizard/pm_complete_wizard.xml',
        'wizard/calibrate_approve_wizard.xml',
        'wizard/calibrate_cancel_wizard.xml',
        'wizard/calibrate_complete_wizard.xml',
    ],
    'demo': [],
}
