# -*- coding: utf-8 -*-
{
    'name': "Lavish SAUCE Connect API",
    'summary': """Importación de Datos desde API SAUCE""",
    'description': """Importación de Datos desde API SAUCE""",
    'author': "Lavish Soft",
    'website': "##",
    'category': 'Products',
    'version': '1.0',
    'depends': [
        'hr',
        'sale',
        'sale_automatic_workflow',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/petrol_pumps.xml',
        'views/gas_suppliers.xml',
        'views/supply_points.xml',
        'views/turns.xml',
        'views/sale_order.xml',
        'views/void.xml',
    ],
}
