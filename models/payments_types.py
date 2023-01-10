# -*- coding: utf-8 -*-
from odoo import fields, models

class PaymentsTypes(models.Model):
    _name = 'payments.types'
    _description = 'Tipos de Pago'
    _rec_name = 'Descripcion'

    IdFormaPago = fields.Char(string="Id", required=True, index=True)
    CodigoTerpel = fields.Char(string="Codigo Terpel", required=True)
    Descripcion = fields.Char(string="Descripcion")
    gas_api = fields.Many2one('gas.api','Venta desde Api')