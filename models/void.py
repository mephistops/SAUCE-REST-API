# -*- coding: utf-8 -*-
from odoo import fields, models

class Void(models.Model):
    _name = 'Void'
    _description = 'Void'

    Binario = fields.Binary('Binario')
    Numero = fields.Char(string="Numero")
