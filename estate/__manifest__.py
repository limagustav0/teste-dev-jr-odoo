{
    'name': 'Real Estate',
    'version': '1.2',
    'category': 'Marketing',
    'sequence': 15,
    'description': "Odoo dev",
    'author' : 'Gustavo C Lima',
    'depends': [
  
    ],
    'data': [
        'security/ir.model.access.csv',
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_offer_views.xml",
        "views/estate_property_views.xml",
        'views/estate_menus.xml'
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False
}