# -*- coding: utf-8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    IdCliente = fields.Char(string="Id de Cliente")
    NumeroDocumento = fields.Char(string="Numero de Documento")
    Codigo = fields.Char(string="Código")
    FechaNacimiento = fields.Date(string="Fecha de Nacimiento")
    TipoDescuento = fields.Char(string="Tipo de Descuento")
    ValorDescuento = fields.Char(string="Valor del Descuento")
    IndTelefono = fields.Char(string="Indicativo de Teléfono")
    