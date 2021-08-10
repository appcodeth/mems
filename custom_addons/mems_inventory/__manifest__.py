{
    'name': 'MEMs Inventory',
    'version': '0.1',
    'author': 'Appcode Technology',
    'website': 'http://www.appcode.co.th/mems',
    'category': 'Custom',
    'depends': ['base', 'mems_master'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/receive_view.xml',
        'views/issue_view.xml',
    ],
    'demo': [],
}
