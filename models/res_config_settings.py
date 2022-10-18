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
        url = '%s/%s' % ( self.psa_url, data)

        response = requests.get(url,
                                auth=(self.psa_username, self.psa_password),
                                headers={'Content-Type': 'application/json'},
                                )                    
        return json.loads(response.text)

    # Crear Paises 
    # En revisión, a pesar de que se confirma la no existencia
    # del País, Odoo considera que existe y no lo crea
    def create_countries(self):
        data = self.get_data('Paises')
        country = self.env['res.country']

        for countries in data['Resultado']:
            exists = country.name_search(name=''.join(countries['Nombre']))
            _logger.info(''.join(countries['Nombre']))
            _logger.info(exists)
            if len(exists) == 0:
                country.create({
                    'name': countries['Nombre']
                })
            else:
                _logger.info("si existe")

    # Crear Productos
    def create_products(self):
        data = self.get_data('Productos')
        product = self.env['product.product']

        for products in data['Resultado']:
            domain = [
                ('name', '=', ''.join(products['Nombre']))
            ]

            exists = product.search_count(domain)
            _logger.info(exists)
            if exists == 0:
                _logger.info("Este producto no existe")
                #product.create({
                 #   'name': 
                #})
            else:
                _logger.info("si existe")

    # Crear Petrol Pump (Estaciones)
    def create_petrol_pump(self):
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
