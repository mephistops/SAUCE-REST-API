from odoo import fields, models, _
import logging
import requests
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
_logger = logging.getLogger(__name__)


class gasApi(models.Model):
    _name = 'gas.api'
    _description = 'GAS API'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    username = fields.Char(string="Usuario", required=True)
    password = fields.Char(string="Clave", required=True)
    IdEstacion = fields.Many2one('petrol.pumps', string="Estación")
    Cliente_final = fields.Many2one('res.partner', string="Cliente")
    fechainicio = fields.Date('Fecha de Inicio')
    fechafinal = fields.Date('Fecha Final')
    #flow = fields.Many2one('sale.workflow.process', string="Flujo")
    IdTurno = fields.Many2many('turns', string="Turno")
    sale_count= fields.Integer(compute='_sale_count',string='Reservation Count',)
    estaciones_count= fields.Integer(compute='_estaciones_count',string='Reservation Count',)
    suplier_count= fields.Integer(compute='_gas_count',string='Reservation Count',)
    
    def _estaciones_count(self):
        reservation_obj = self.env['petrol.pumps']
        for unit in self:
            reservations_ids = reservation_obj.search([('gas_api', '=', unit.id)])  
            unit.estaciones_count = len(reservations_ids)
            
    def _sale_count(self):
        reservation_obj = self.env['sale.order']
        for unit in self:
            reservations_ids = reservation_obj.search([('gas_api', '=', unit.id)])  
            unit.sale_count = len(reservations_ids)
    
    def name_get(self):
        rec = []
        for recs in self:
            name = '%s - %s ' % (recs.IdEstacion.Nombre or '',
                                recs.username or '')
            rec += [(recs.id, name)]
        return rec
    
    def view_reservations(self):
        reservation_obj = self.env['sale.order']
        reservations_ids = reservation_obj.search([('gas_api', '=', self.ids)])
        reservations=[]
        for obj in reservations_ids: reservations.append(obj.id)
        return {
            'name': _('Ventas'),
            'domain': [('id', 'in', reservations)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'sale.order',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }
    def _gas_count(self):
        reservation_obj = self.env['gas.suppliers']
        for unit in self:
            reservations_ids = reservation_obj.search([('gas_api', '=', unit.id)])  
            unit.suplier_count = len(reservations_ids) 

    def view_supplier(self):
        reservation_obj = self.env['gas.suppliers']
        reservations_ids = reservation_obj.search([('gas_api', '=', self.ids)])
        reservations=[]
        for obj in reservations_ids: reservations.append(obj.id)
        return {
            'name': _('Surtidores'),
            'domain': [('id', 'in', reservations)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'gas.suppliers',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }       
    def view_estaciones(self):
        reservation_obj = self.env['petrol.pumps']
        reservations_ids = reservation_obj.search([('gas_api', '=', self.ids)])
        reservations=[]
        for obj in reservations_ids: reservations.append(obj.id)
        return {
            'name': _('Estaciones'),
            'domain': [('id', 'in', reservations)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'petrol.pumps',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }
        
    def view_empleados(self):
        reservation_obj = self.env['hr.employee']
        reservations_ids = reservation_obj.search([('gas_api', '=', self.ids)])
        reservations=[]
        for obj in reservations_ids: reservations.append(obj.id)
        return {
            'name': _('Empleados'),
            'domain': [('id', 'in', reservations)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'hr.employee',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }
        
    def view_islas(self):
        reservation_obj = self.env['supply.points']
        reservations_ids = reservation_obj.search([('gas_api', '=', self.ids)])
        reservations=[]
        for obj in reservations_ids: reservations.append(obj.id)
        return {
            'name': _('Islas'),
            'domain': [('id', 'in', reservations)],
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model':'supply.points',
            'type':'ir.actions.act_window',
            'nodestroy':True,
            'view_id': False,
            'target':'current',
        }
    """Connect to API SAUCE"""

    def get_data(self, data):
        url = f"https://api2.sauce.online/api/{data}"

        response = requests.get(url,
                                #auth=("Consultastamaria", "123456789"),
                                auth=(self.username, self.password),
                                headers={'Content-Type': 'application/json'},
                                )
        return json.loads(response.text)

    """Create Petrol Pumps (Estaciones de Bombeo)"""

    def petrol_pumps(self):
        data = self.get_data('Estaciones')
        petrolPumps = self.env['petrol.pumps']

        for petrolPump in data['Resultado']:
            exists = petrolPumps.search(
                [('IdEstacion', '=', petrolPump['IdEstacion'])])
            if len(exists) == 0:
                petrolPumps.create({
                    'IdEstacion': petrolPump['IdEstacion'],
                    'Codigo': petrolPump['Codigo'],
                    'Nombre': petrolPump['Nombre'],
                    'Direccion': petrolPump['Direccion'],
                    'Telefono': petrolPump['Telefono'],
                    'Url': petrolPump['Url'],
                    'RazonSocial': petrolPump['RazonSocial'],
                    'Activa': petrolPump['Activa'],
                    'Rut': petrolPump['Rut'],
                    'Email': petrolPump['Email'],
                    'gas_api': self.id,
                    'NombreGerente': petrolPump['NombreGerente'],
                    'IdCiudad': petrolPump['IdCiudad'],
                    'Nit': petrolPump['Nit']
                })

    """Create Supply Points (Islas)"""

    def supply_points(self):
        petrolPumps = self.env['petrol.pumps']
        supplyPoints = self.env['supply.points']
        all_records = petrolPumps.search([(1, '=', 1)])

        for item in all_records:
            data = self.get_data('Estaciones/%s/islas' % (item['IdEstacion']))
            for supplyPoint in data['Resultado']:
                exists = petrolPumps.search(
                    [('IdEstacion', '=', supplyPoint['IdEstacion'])])
                estacion = self._get_estaciones((supplyPoint['IdEstacion']))
                if len(exists) > 0:
                    supplyPoints.create({
                        'IdIsla': supplyPoint['IdIsla'],
                        'Codigo': supplyPoint['Codigo'],
                        'Nombre': supplyPoint['Nombre'],
                        'IdEstacion': estacion,
                        'gas_api': self.id,
                        'Estado': supplyPoint['Estado'],
                    })

    """Create Gas Suppliers (Surtidores)"""

    def gas_suppliers(self):
        supplyPoints = self.env['supply.points']
        gasSuppliers = self.env['gas.suppliers']
        all_records = supplyPoints.search([(1, '=', 1)])

        for item in all_records:
            data = self.get_data('%s/%s/surtidores' %
                                 ('Islas', item['IdIsla']))

            for gasSupplier in data['Resultado']:
                exists = gasSuppliers.search(
                    [('IdSurtidor', '=', gasSupplier['IdSurtidor'])])
                estacion_id = gasSupplier['IdEstacion'] or ''
                islas_id = gasSuppliers['IdIsla'] or ''
                if len(exists) == 0:
                    estacion = self.env['petrol.pumps'].search_read(
                        [('IdEstacion', '=', estacion_id)]) or ''
                    islas = self.env['supply.points'].search_read(
                        [('IdIsla', '=', islas_id)]) or ''
                    gasSuppliers.create({
                        'IdSurtidor': gasSupplier['IdSurtidor'],
                        'CodSurtidor': gasSupplier['CodSurtidor'],
                        'IdEstacion': estacion[0].get('id'),
                        'gas_api': self.id,
                        'Descripcion': gasSupplier['Descripcion'],
                        # 'IdIsla': islas[0].get('id') or '',
                        'CodigoPCC': gasSupplier['CodigoPCC']
                    })

    """Create Employees (Empleados)"""

    def employees_sauce(self):
        petrolPumps = self.env['petrol.pumps']
        employees = self.env['hr.employee']
        all_records = petrolPumps.search([(1, '=', 1)])

        for item in all_records:
            data = self.get_data(
                f"Estaciones/{item['IdEstacion']}/ventas/date/2022-10-28")

            for employee in data['Resultado']:
                exists = employees.search(
                    [('name', '=', employee['Empleado']['Nombre'])])
                if len(exists) == 0:
                    employees.create({
                        'name': employee['Empleado']['Nombre'],
                        'IdEmpleado': employee['Empleado']['IdEmpleado'],
                        'Cedula': employee['Empleado']['Cedula'],
                        'EsActivo': employee['Empleado']['EsActivo'],
                        'Codigo': employee['Empleado']['Codigo'],
                        'gas_api': self.id,
                        'IdCargo': employee['Empleado']['Idcargo'],
                        'EsAdministrador': employee['Empleado']['EsAdministrador']
                    })

    """Create Turns (Turnos)"""

    def turns(self):
        employees = self.env['hr.employee']
        turns = self.env['turns']
        all_records = employees.search([(1, '=', 1)])

        for item in all_records:
            data = self.get_data(f"Turnos/empleado/{item['IdEmpleado']}")
            if "Resultado" in data:
                for turnos in data['Resultado']:
                    estacion_id = turnos['IdEstacion'] or ''
                    estacion = self.env['petrol.pumps'].search_read(
                        [('IdEstacion', '=', estacion_id)])
                    empleado = self.env['hr.employee'].search_read(
                        [('IdEmpleado', '=', turnos['IdEmpleado'])])
                    exists = turns.search(
                        [('IdTurno', '=', turnos['IdTurno'])])
                    if len(exists) == 0:

                        turns.create({
                            'IdTurno': turnos['IdTurno'],
                            'IdEmpleado': empleado[0].get('id'),
                            'IdEstacion': estacion[0].get('id'),
                            'Apertura': turnos['Apertura'],
                            'Cierre': turnos['Cierre'],
                            'gas_api': self.id,
                            'NumeroTurno': turnos['NumeroTurno'],
                            'FinalizaConsignacionSobre': turnos['FinalizaConsignacionSobre'],
                            'AjustadoPorOperacion': turnos['AjustadoPorOperacion'],
                            'EsConsolidado': turnos['EsConsolidado'],
                            'Empleado': turnos['Empleado'],
                            'EsVerificado': turnos['EsVerificado'],
                            'EsCerrado': turnos['EsCerrado']
                        })

    """Create Clients (Clientes)"""

    def clients(self):
        clients = self.env['res.partner']

        data = self.get_data(f"clientes")
        for client in data['Resultado']:
            exists = clients.search([('vat', '=', client['NumeroDocumento'])])
            if len(exists) == 0:
                tipo = 1 if (client['TipoDocumento'] == "Cedula") else 2
                clients.create({
                    'vat': client['NumeroDocumento'],
                    'name': '%s %s' % (client['Nombre'], client['Apellidos']),
                    'street': client['Direccion'],
                    'phone': client['Telefono'],
                    'mobile': client['Celular'],
                    'email': client['Email'],
                    'city': client['Ciudad'],
                    'l10n_latam_identification_type_id': tipo
                })

    """Create Products (Producto)"""

    def products(self):
        products = self.env['product.template']

        data = self.get_data(f"Productos")
        for product in data['Resultado']:
            exists = products.search(
                [('CodProducto', '=', product['CodProducto'])])
            if len(exists) == 0:

                products.create({
                    'name': product['Nombre'],
                    'CodProducto': product['CodProducto'],
                    'IdUnidadMedida': product['IdUnidadMedida'],
                    'IdProducto': product['IdProducto'],
                    'EsLiquido': product['EsLiquido']
                })
                
    def sale_orders(self):
        fechainicio = self.fechainicio
        fechafinal = self.fechafinal    

        estaciones_code = self.IdEstacion.IdEstacion
        turnos = self.get_data(
            f"/Estaciones/{estaciones_code}/turnos/date/apertura/{fechainicio}/{fechafinal}")
        values = ''
        sale_order = self.env['sale.order'].sudo()
        default_order = sale_order.default_get(values)

        for turno in turnos['Resultado']:
            ventas = self.get_data(f"/Turnos/{turno['IdTurno']}/ventas")
            if "Resultado" in ventas:
                for venta in ventas['Resultado']:
                    order = self.env['sale.order'].search([('IdRegistroVenta', '=', venta['IdRegistroVenta'])])
                    if not order:
                        empleado = self._get_empl(venta['Empleado'].get('IdEmpleado'),
                                                venta['Empleado'].get('Nombre'),
                                                venta['Empleado'].get('Cedula'),
                                                venta['Empleado'].get('EsActivo'),
                                                venta['Empleado'].get('Codigo'),
                                                venta['Empleado'].get('Idcargo'),
                                                venta['Empleado'].get('EsAdministrador'),
                                                )
                        turnos_ = self._get_turnos_ve(venta['IdTurno'])
                        product = self.env['product.template'].search([('CodProducto', '=', venta['Producto']['CodProducto'])])
                        date_order = venta['HoraInicio'].split('T')
                        #fecha = date_order[0]
                        hora = date_order[1].split('.')
                        date_formatted = date_order[0] + " " + hora[0]
                        date_formatted = datetime.strptime(date_formatted, '%Y-%m-%d %H:%M:%S') + timedelta(hours=5)
                        payment_type = self.env['payments.types'].search([('IdFormaPago', '=', venta['Pagos'][0].get('IdFormaPago'))])
                        partner = ''
                        if venta['Cliente'] == None:
                            partner = self.Cliente_final.id
                        else:
                            partner = self._get_partner(
                                venta['Cliente'].get('NumeroDocumento'))
                        isla = ''
                        if venta['IdIsla']:
                            isla = self.env['supply.points'].search([('IdIsla', '=', venta['IdIsla'])])
                        else:
                            isla = False
                        surtidor = ''
                        if venta['IdSurtidor']:
                            surtidor = self.env['gas.suppliers'].search([('IdSurtidor', '=', venta['IdSurtidor'])])
                        else:
                            surtidor = False
                        values = dict(default_order)
                        values.update({
                            'partner_id': payment_type.Cliente_final.id or partner,
                            'IdRegistroVenta': venta['IdRegistroVenta'],
                            'Recibo': venta['Recibo'],
                            'Placa': venta['Placa'],
                            'date_order': date_formatted,
                            'gas_api': self.id,
                            'ROM': venta['ROM'],
                            'IdIsla': isla.id,
                            'CodSurtidor': venta['CodSurtidor'],
                            'IdVehiculo': venta['IdVehiculo'],
                            'IdSurtidor': surtidor.id,
                            'payment_term_id': payment_type.payment_term.id,
                            'LecturaInicial': venta['LecturaInicial'],
                            'LecturaFinal': venta['LecturaFinal'],
                            'IdEstacion': self.IdEstacion.id,
                            'IdEmpleado': empleado,
                            'order_line': [(0, 0, {
                                'product_id': product['id'],
                                'name': product['name'],
                                'product_uom': product['uom_id'].id,
                                'price_subtotal': venta['Valor'],
                                'product_uom_qty': venta['Cantidad'],
                                'price_unit': venta['Precio'],
                            })],
                            'FormaDePago': payment_type.id,
                            'IdTurno': turnos_,
                        })
                        sale_order.create(values)
                    else:
                        self.message_post(body=_("El recibo <b>%s<b> Ya existen en Ventas Como la orden <b>%s<b>", order.Recibo, order.name))
            else:
                self.message_post(body=_("No se pudo generar la ventas de este turno <b>%s<b> No existen Ventas", turno['IdTurno'] ))

    def _get_partner(self, vat):
        partner = self.env['res.partner'].search_read([('vat', '=', vat)])
        if partner:
            return partner[0].get('id')
        else:
            return False
        
    def _get_turnos_ve(self, IdTurno):
        if IdTurno:
            Turno = self.env['turns'].search_read([('IdTurno', '=', IdTurno)])
            if Turno:
                return Turno[0].get('id')
            else:
                turns = self.env['turns']
                data = self.get_data(f"Turnos/{IdTurno}")
                estacion_id = data['IdEstacion'] or ''
                estacion = self.env['petrol.pumps'].search_read([('IdEstacion', '=', estacion_id)])
                empleado = self.env['hr.employee'].search_read([('IdEmpleado', '=', data['IdEmpleado'])])
                exists = turns.search([('IdTurno', '=', data['IdTurno'])])
                if len(exists) == 0:
                    turns.create({
                        'IdTurno': data['IdTurno'],
                        #'IdEmpleado': empleado[0].get('id'),
                        'IdEstacion': estacion[0].get('id'),
                        'Apertura': data['Apertura'],
                        'Cierre': data['Cierre'],
                        'gas_api': self.id,
                        'NumeroTurno': data['NumeroTurno'],
                        'FinalizaConsignacionSobre': data['FinalizaConsignacionSobre'],
                        'AjustadoPorOperacion': data['AjustadoPorOperacion'],
                        'EsConsolidado': data['EsConsolidado'],
                        'Empleado': data['Empleado'],
                        'EsVerificado': data['EsVerificado'],
                        #'EsCerrado': data['EsCerrado']
                    })
            return turns.id
        else:
            turns = self.env['turns']
            data = self.get_data(f"Turnos/{IdTurno}")
            if "Resultado" in data:
                for turnos in data['Resultado']:
                    estacion_id = turnos['IdEstacion'] or ''
                    estacion = self.env['petrol.pumps'].search_read(
                        [('IdEstacion', '=', estacion_id)])
                    empleado = self.env['hr.employee'].search_read(
                        [('IdEmpleado', '=', turnos['IdEmpleado'])])
                    exists = turns.search(
                        [('IdTurno', '=', turnos['IdTurno'])])
                    if len(exists) == 0:
                        turns.create({
                            'IdTurno': turnos['IdTurno'],
                            'IdEmpleado': empleado[0].get('id'),
                            'IdEstacion': estacion[0].get('id'),
                            'Apertura': turnos['Apertura'],
                            'Cierre': turnos['Cierre'],
                            'gas_api': self.id,
                            'NumeroTurno': turnos['NumeroTurno'],
                            'FinalizaConsignacionSobre': turnos['FinalizaConsignacionSobre'],
                            'AjustadoPorOperacion': turnos['AjustadoPorOperacion'],
                            'EsConsolidado': turnos['EsConsolidado'],
                            'Empleado': turnos['Empleado'],
                            'EsVerificado': turnos['EsVerificado'],
                            'EsCerrado': turnos['EsCerrado']
                        })
            return turns.id
        
    def _get_empl(self, empleado, Nombre, Cedula, EsActivo, Codigo, Idcargo, EsAdministrador):
        employees = self.env['hr.employee']
        partner = self.env['hr.employee'].search_read([('IdEmpleado', '=', empleado)])
        if partner:
            return partner[0].get('id')
        else:
            exists = employees.search([('name', '=', Nombre)])
            if len(exists) == 0:
                employees.create({
                    'name': Nombre,
                    'IdEmpleado': empleado,
                    'Cedula': Cedula ,
                    'EsActivo': EsActivo,
                    'Codigo': Codigo,
                    'gas_api': self.id,
                    'IdCargo': Idcargo,
                    'EsAdministrador': EsAdministrador,
                })
            return employees.id

    def _get_isla(self, isla):
        partner = self.env['hr.employee'].search_read(
            [('IdEmpleado', '=', isla)])
        if partner:
            return partner[0].get('id')
        else:
            return False

    def _get_order_lines(self, lines):
        data = []
        for l in lines:
            product = self.env['product.template'].search(
                [('name', '=', l['Producto'])])
            vals = {
                'product_id': product['id'],
                'price_subtotal': l['Valor'],
                'product_uom_qty': l['Cantidad'],
                'price_unit': l['Precio'],
            }
            data.append((0, 0, vals))
        return data

    def _get_estaciones(self, IdEstacion):
        Estacion = self.env['petrol.pumps'].search_read(
            [('IdEstacion', '=', IdEstacion)])
        if Estacion:
            return Estacion[0].get('id')
        else:
            return False

    def _get_islas(self, IdIsla):
        islas = self.env['supply.points'].search_read(
            [('IdIsla', '=', IdIsla)])
        if islas:
            return islas[0].get('id')
        else:
            return False

    """Create Payments Types (Tipos de Pago)"""

    def payments_types(self):
        data = self.get_data('FormasDePago')
        paymentsTypes = self.env['payments.types']

        for paymentType in data['Resultado']:
            exists = paymentsTypes.search(
                [('IdFormaPago', '=', paymentType['IdFormaPago'])])
            if len(exists) == 0:
                paymentsTypes.create({
                    'IdFormaPago': paymentType['IdFormaPago'],
                    'CodigoTerpel': paymentType['CodigoTerpel'],
                    'Descripcion': paymentType['Descripcion'],
                })
