# -*- coding: utf-8 -*-
from odoo import fields, models

class SupplyPoints(models.Model):
    _name = 'supply.points'
    _description = 'Islas'
    _rec_name = 'Nombre'

    IdIsla = fields.Char(string="Id", required=True, index=True)
    Codigo = fields.Char(string="Código", required=True)
    Nombre = fields.Char(string="Nombre")
    IdEstacion = fields.Many2one('petrol.pumps',string="Estación")
    Estado = fields.Boolean(string="Estado")