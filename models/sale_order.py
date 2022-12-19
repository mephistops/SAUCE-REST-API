from odoo import models, fields, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _name = 'Ventas'
    
    IdRegistroVenta = fields.Char(string="Registro Venta")
    Recibo = fields.Char(string="Recibo")
    IdVehiculo = fields.Char(string="Vehiculo")
    Placa = fields.Char(string="Placa")
    IdTurno = fields.Many2one('turns',string="Turno")
    IdManguera = fields.Many2one('turns',string="Manguera")
    IdEstacion = fields.Many2one('petrol.pumps',string="Estacion")
    LecturaInicial = fields.Char(string="Lectura Inicial")
    LecturaFinal = fields.Char(string="Lectura Final")
    ROM = fields.Char(string="ROM")
    CodSurtidor =  fields.Char(string="Surtidor ")
    CodCara = fields.Char(string="Cara") 
    Prefijo = fields.Char(string="Prefijo")
    Consecutivo = fields.Char(string="Consecutivo ")
    EsAnulado = fields.Boolean(tring="Anulado")
    FechaProximoMantenimiento = fields.Char(string="Fecha Proximo Mantenimiento")
    gas_api = fields.Many2one('gas.api','Venta desde Api')
    IdEmpleado = fields.Many2one('hr.employee',string="Empleado")
    FormaDePago = fields.Char(string="Tipo de Pago")
    
    def prepare_sales_order_vals(self,value):
        self.default_get(value)
