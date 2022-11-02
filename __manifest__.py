# -*- coding: utf-8 -*-
{
    'name': "API SAUCE",
    'summary': """Importación de Datos desde API SAUCE""",
    'description': """Importación de Datos desde API SAUCE""",
    'author': "David Alejandro Soluciones",
    'website': "##",
    'category': 'Products',
    'version': '1.0',
    'depends': [
        'hr',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/petrol_pumps.xml',
        'views/gas_suppliers.xml',
        'views/supply_points.xml',
        'views/turns.xml',
    ],
}
