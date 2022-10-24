# -*- coding: utf-8 -*-
from odoo import fields, models

class SupplyPoints(models.Model):
  _name = 'supply.points'
  _description = 'Islas'

  IdIsla = fields.Char(string="Id", required=True)
  Codigo = fields.Char(string="Código", required=True)
  Nombre = fields.Char(string="Nombre")
  IdEstacion = fields.Char(string="Id Estación", required=True)
  Estado = fields.Boolean(string="Estado")
