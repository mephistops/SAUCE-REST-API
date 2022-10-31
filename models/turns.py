# -*- coding: utf-8 -*-
from odoo import fields, models

class Turns(models.Model):
    _name = 'turns'
    _description = 'Turnos'
    _rec_name = 'IdTurno'

    IdTurno                   = fields.Char(string="Id Turno", index=True)
    IdEmpleado                = fields.Char(string="Id de Empleado")
    IdEstacion                = fields.Char(string="Id de Estacion")
    Apertura                  = fields.Date(string="Fecha de Apertura")
    Cierre                    = fields.Date(string="Fecha de Cierre")
    NumeroTurno               = fields.Char(string="NumeroTurno")
    FinalizaConsignacionSobre = fields.Boolean(string="FinalizaConsignacionSobre")
    AjustadoPorOperacion      = fields.Boolean(string="Ajustado Por Operacion")
    EsConsolidado             = fields.Boolean(string="Consolidado")
    Empleado                  = fields.Char(string="Empleado")
    EsVerificado              = fields.Boolean(string="Verificado")
    EsCerrado                 = fields.Boolean(string="Cerrado")