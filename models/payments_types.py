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
    payment_term = fields.Many2one('account.payment.term', 'Termino de pagos')
    Cliente_final = fields.Many2one('res.partner', string="Cliente")