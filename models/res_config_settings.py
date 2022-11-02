# -*- coding: utf-8 -*-
from odoo import fields, models
import logging, requests, json

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    """Connect to API SAUCE"""
    def get_data(self, data):
        url = f"https://api2.sauce.online/api/{data}"

        response = requests.get(url,
            auth=("Consultastamaria", "123456789"),
            headers={'Content-Type': 'application/json'},
        )                 
        return json.loads(response.text)

    """Create Petrol Pumps (Estaciones de Bombeo)"""
    def petrol_pumps(self):    
        data = self.get_data('Estaciones')
        petrolPumps = self.env['petrol.pumps']

        for petrolPump in data['Resultado']:
            exists = petrolPumps.search([('IdEstacion', '=', petrolPump['IdEstacion'])])
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
                exists = petrolPumps.search([('IdEstacion', '=', supplyPoint['IdEstacion'])])
                
                if len(exists) > 0:
                    supplyPoints.create({
                        'IdIsla': supplyPoint['IdIsla'],
                        'Codigo': supplyPoint['Codigo'],
                        'Nombre': supplyPoint['Nombre'],
                        'IdEstacion': item['IdEstacion'],
                        'Estado': supplyPoint['Estado'],
                    })

    """Create Gas Suppliers (Surtidores)"""
    def gas_suppliers(self):
        supplyPoints = self.env['supply.points']
        gasSuppliers = self.env['gas.suppliers']
        all_records = supplyPoints.search([(1, '=', 1)])
        
        for item in all_records:
            data = self.get_data('%s/%s/surtidores' % ('Islas', item['IdIsla']))
                       
            for gasSupplier in data['Resultado']:
                exists = gasSuppliers.search([('IdSurtidor', '=', gasSupplier['IdSurtidor'])])
                if len(exists) == 0:    
                    gasSuppliers.create({
                        'IdSurtidor': gasSupplier['IdSurtidor'],
                        'CodSurtidor': gasSupplier['CodSurtidor'],
                        'IdEstacion': gasSupplier['IdEstacion'],
                        'Descripcion': gasSupplier['Descripcion'],
                        'IdIsla': gasSupplier['IdIsla'],
                        'CodigoPCC': gasSupplier['CodigoPCC']
                    })

    """Create Employees (Empleados)"""
    def employees_sauce(self):
        petrolPumps = self.env['petrol.pumps']
        employees = self.env['hr.employee']
        all_records = petrolPumps.search([(1, '=', 1)])

        for item in all_records:
            data = self.get_data(f"Estaciones/{item['IdEstacion']}/ventas/date/2022-10-28")

            for employee in data['Resultado']:
                exists = employees.search([('name', '=', employee['Empleado']['Nombre'])])
                if len(exists) == 0:
                    employees.create({
                        'name': employee['Empleado']['Nombre'],
                        'IdEmpleado': employee['Empleado']['IdEmpleado'],
                        'Cedula': employee['Empleado']['Cedula'],
                        'EsActivo': employee['Empleado']['EsActivo'],
                        'Codigo': employee['Empleado']['Codigo'],
                        'IdCargo': employee['Empleado']['Idcargo'],
                        'EsAdministrador': employee['Empleado']['EsAdministrador']
                    })

    """Create Turns (Turnos)"""
    def turns(self):
        employees = self.env['hr.employee']
        turns = self.env['turns']
        all_records = employees.search([('1', '==', '1')])
        
        for item in all_records:
            data = self.get_data(f"Turnos/empleado/{item['IdEmpleado']}")       
            for turnos in data['Resultado']:         
                exists = turns.search([('IdTurno', '=', turnos['IdTurno'])])
                if len(exists) == 0:         
                    turns.create({
                        'IdTurno': turnos['IdTurno'],
                        'IdEmpleado': turnos['IdEmpleado'],
                        'IdEstacion': turnos['IdEstacion'],
                        'Apertura': turnos['Apertura'],
                        'Cierre': turnos['Cierre'],
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
                tipo = 1 if (client['TipoDocumento'] == "Cedula") else 2;
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
            exists = products.search([('CodProducto', '=', product['CodProducto'])])
            if len(exists) == 0:
                
                products.create({
                    'name': product['Nombre'],
                    'CodProducto': product['CodProducto'],
                    'IdUnidadMedida': product['IdUnidadMedida'],
                    'IdProducto': product['IdProducto'],
                    'EsLiquido': product['EsLiquido']
                })

    def sale_orders(self):
        fecha = "2022-10-28"        
        data = self.get_data(f"/Estaciones/2215/ventas/date/{fecha}")

        for venta in data['Resultado']:   
            product = self.env['product.template'].search([('name', '=', venta['Producto']['Nombre'])])

            date_order = venta['HoraInicio'].split('T')

            self.env['sale.order'].sudo().create({
                    'partner_id': 392,
                    'date_order': date_order[0],
                    'order_line': [(0, 0, {
                        'product_id': product['id'],
                        'price_unit': venta['Pagos'][0]['Valor'],
                    })]
                })

                