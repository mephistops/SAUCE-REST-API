# -*- coding: utf-8 -*-
from odoo import fields, models

class Void(models.Model):
    _name = 'void'
    _description = 'Void'

    Binario = fields.Binary('Binario')
    Numero = fields.Char(string="Numero")
