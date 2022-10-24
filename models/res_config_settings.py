# -*- coding: utf-8 -*-
from odoo import fields, models
import requests, json, logging

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    psa_url = fields.Char(
        string="url",
        config_parameter='invoice_config.url_body',
        default='https://api2.sauce.online/api',
    )
    psa_username = fields.Char(
        string="username",
        config_parameter='invoice_config.username',
        default='Consultastamaria',
    )
    psa_password = fields.Char(
        string="password",
        config_parameter='invoice_config.password',
        default='123456789',
    )
    
    def get_data(self, data):
        _logger.info('get_data')
        url = '%s/%s' % ('https://api2.sauce.online/api', data)

        response = requests.get(url,
                                auth=('Consultastamaria', '123456789'),
                                headers={'Content-Type': 'application/json'},
                                )                    
        return json.loads(response.text)

    def petrol_pumps(self):
        data = self.get_data('Estaciones')
        petrolPumps = self.env['petrol.pumps']

        for petrolPump in data['Resultado']:
            domain = [
                ('IdEstacion', '=', petrolPump['IdEstacion'])
            ]

            exists = petrolPumps.search(domain)
            if len(exists) == 0:
                petrolPumps.create({
                    "IdEstacion": petrolPump['IdEstacion'],
                    "Codigo": petrolPump['Codigo'],
                    "Nombre": petrolPump['Nombre'],
                    "Direccion": petrolPump['Direccion'],
                    "Telefono": petrolPump['Telefono'],
                    "Url": petrolPump['Url'],
                    "RazonSocial": petrolPump['RazonSocial'],
                    "Activa": petrolPump['Activa'],
                    "Rut": petrolPump['Rut'],
                    "Email": petrolPump['Email'],
                    "NombreGerente": petrolPump['NombreGerente'],
                    "IdCiudad": petrolPump['IdCiudad'],
                    "Nit": petrolPump['Nit']
                })
            else:
                _logger.info("Esta estación ya existe")

    def supply_points(self):
        data = self.get_data('Estaciones')
        petrolPumps = self.env['petrol.pumps']
        supplyPoints = self.env['supply.points']

        for petrolPump in data['Resultado']:
            domain = [
                ('IdEstacion', '=', petrolPump['IdEstacion'])
            ]

            dataSP = self.get_data('%s/%s/islas' % ('Estaciones', petrolPump['IdEstacion']))

            exists = petrolPumps.search(domain)
            if len(exists) != 0:
                for supplyPoint in dataSP['Resultado']:
                    supplyPoints.create({
                        'IdIsla': supplyPoint['IdIsla'],
                        'Codigo': supplyPoint['Codigo'],
                        'Nombre': supplyPoint['Nombre'],
                        'IdEstacion': supplyPoint['IdEstacion'],
                        'Estado': supplyPoint['Estado'],
                    })
