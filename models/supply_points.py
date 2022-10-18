# -*- coding: utf-8 -*-
from odoo import fields, models

class SupplyPoints(models.Model):
  _name = 'supply.points'

  IdIsla = fields.Char(string="Id")
  Codigo = fields.Char(string="Código")
  Nombre = fields.Char(string="Nombre")
  IdEstacion = fields.Char(string="Id Estación")
  Estado = fields.Boolean(string="Estado")
