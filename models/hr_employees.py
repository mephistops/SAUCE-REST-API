# -*- coding: utf-8 -*-
from odoo import fields, models

class HrEmployees(models.Model):
    _inherit = 'hr.employee'

    IdEmpleado = fields.Char(string="Id de Empleado")
    Cedula = fields.Integer(string="Documento Identidad")
    EsActivo = fields.Boolean(string="Activo")
    Codigo = fields.Integer(string="Código")
    IdCargo = fields.Integer(string="Cargo")
    EsAdministrador = fields.Boolean(string="Administrador")