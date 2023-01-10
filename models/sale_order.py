from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    IdRegistroVenta = fields.Char(string="Registro Venta")
    Recibo = fields.Char(string="Recibo")
    IdVehiculo = fields.Char(string="Vehiculo")
    Placa = fields.Char(string="Placa")
    IdIsla = fields.Many2one('supply.points',string="Isla")
    IdSurtidor = fields.Many2one('gas.suppliers',string="Surtidor")
    IdTurno = fields.Many2one('turns',string="Turno")
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
    FormaDePago = fields.Many2one('payments.types',string="Tipo de Pago")
    void = fields.Many2one('void','Voucher', compute='_computeVoid')
    void_imagen = fields.Binary(related='void.Binario')
    
    def _computeVoid(self):
        for unit in self:
            reservation_obj = unit.env['void']
            reservations_id = reservation_obj.search([('Numero', '=', unit.Recibo)], limit=1)  
            unit.void = reservations_id.id
    
    def prepare_sales_order_vals(self,value):
        self.default_get(value)
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft_or_cancel(self):
        for order in self:
            if order.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete a sent quotation or a confirmed sales order. You must first cancel it.'))
            if order.gas_api:
                raise UserError(_('No puede borrar una orden creada desde sauce'))

class AccountMove(models.Model):
    _inherit = "account.move"

    Print_void = fields.Boolean(string="Imprimir Voucher", default=False)
    sale_order_ids = fields.Many2many(
        comodel_name="sale.order",
        string="Related sale order",
        store=True,
        compute="_compute_sale_ids",
        help="Related sale order "
        "(only when the invoice has been generated from a sale order).",
    )

    @api.depends("invoice_line_ids", "invoice_line_ids.sale_line_ids")
    def _compute_sale_ids(self):
        for invoice in self:
            invoice.sale_order_ids = invoice.mapped(
                "invoice_line_ids.sale_line_ids.order_id"
            )
