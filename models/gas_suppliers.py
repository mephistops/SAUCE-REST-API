# -*- coding: utf-8 -*-
from odoo import fields, models

class GasSuppliers(models.Model):
    _name = 'gas.suppliers'
    _description = 'Surtidores'
    _rec_name = 'Descripcion'

    IdEstacion = fields.Char(string="Id Estación", required=True)
    IdSurtidor = fields.Char(string="IdSurtidor", index=True)
    CodSurtidor = fields.Char(string="CodSurtidor")
    Descripcion = fields.Char(string="Descripcion")
    IdIsla = fields.Char(string="IdIsla")
    CodigoPCC = fields.Char(string="CodigoPCC")