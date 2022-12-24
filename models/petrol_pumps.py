# -*- coding: utf-8 -*-
from odoo import fields, models

class PetrolPumps(models.Model):
    _name = 'petrol.pumps'
    _description = 'Estación de Bombeo'
    _rec_name = 'Nombre'

    IdEstacion = fields.Char(string="Id", required=True, index=True)
    Codigo = fields.Char(string="Codigo", required=True)
    Nombre = fields.Char(string="Nombre")
    Direccion = fields.Char(string="Dirección")
    Telefono = fields.Char(string="Teléfono")
    Url = fields.Char(string="Url")
    RazonSocial = fields.Char(string="Razón social")
    Activa = fields.Boolean(string="Estado")
    Rut = fields.Char(string="RUT")
    Email = fields.Char(string="Correo electrónico")
    NombreGerente = fields.Char(string="Nombre de Gerente")
    IdCiudad = fields.Char(string="Ciudad")
    Nit = fields.Char(string="NIT")
    gas_api = fields.Many2one('gas.api','Venta desde Api')