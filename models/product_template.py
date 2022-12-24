# -*- coding: utf-8 -*-
from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    CodProducto = fields.Char(string="CodProducto")
    IdUnidadMedida = fields.Char(string="Id Unidad de Medida")
    IdProducto = fields.Char(string="Id Producto")
    EsLiquido = fields.Boolean(string="Es Liquido")
    gas_api = fields.Many2one('gas.api','Venta desde Api')
    