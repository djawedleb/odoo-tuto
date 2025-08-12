{
    'name': 'Estate',
    'version': '1.0',
    'depends': ['base'],
    'author': 'DJAWED',
    'category': 'Sales',
    'description': """
        Estate Tutorial Module
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}