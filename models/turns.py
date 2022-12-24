# -*- coding: utf-8 -*-
from odoo import fields, models

class Turns(models.Model):
    _name = 'turns'
    _description = 'Turnos'
    _rec_name = 'IdTurno'

    IdTurno = fields.Char(string="Turno", index=True)
    IdEmpleado = fields.Many2one('hr.employee',string="Empleado")
    IdEstacion = fields.Many2one('petrol.pumps',string="Estación", required=True)
    Apertura = fields.Date(string="Fecha de Apertura")
    Cierre = fields.Date(string="Fecha de Cierre")
    NumeroTurno = fields.Char(string="NumeroTurno")
    FinalizaConsignacionSobre = fields.Boolean(string="FinalizaConsignacionSobre")
    AjustadoPorOperacion = fields.Boolean(string="Ajustado Por Operacion")
    EsConsolidado = fields.Boolean(string="Consolidado")
    Empleado = fields.Char(string="Empleado")
    EsVerificado = fields.Boolean(string="Verificado")
    EsCerrado = fields.Boolean(string="Cerrado")
    gas_api = fields.Many2one('gas.api','Venta desde Api')