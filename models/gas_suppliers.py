# -*- coding: utf-8 -*-
from odoo import fields, models

class GasSuppliers(models.Model):
    _name = 'gas.suppliers'
    _description = 'Surtidores'
    _rec_name = 'Descripcion'

    IdEstacion = fields.Many2one('petrol.pumps',string="Estación", required=True)
    IdSurtidor = fields.Char(string="Surtidor", index=True)
    CodSurtidor = fields.Char(string="Surtidor")
    Descripcion = fields.Char(string="Descripcion")
    IdIsla = fields.Many2one('supply.points',string="IdIsla")
    CodigoPCC = fields.Char(string="CodigoPCC")

class PaymentsTypes(models.Model):
    _name = 'payments.types'
    _description = 'Tipos de Pago'
    _rec_name = 'Descripcion'

    IdFormaPago = fields.Char(string="Id", required=True, index=True)
    CodigoTerpel = fields.Char(string="Codigo Terpel", required=True)
    Descripcion = fields.Char(string="Descripcion")