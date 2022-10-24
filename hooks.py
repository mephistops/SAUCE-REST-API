from odoo import api, SUPERUSER_ID

def pre_init(cr):
  env = api.Environment(cr, SUPERUSER_ID, {})
  env['ir.model.data'].search([
    ('model', '=', 'supply.points'),
    ('model', '=', 'petrol.pumps')
  ]).unlink()

def post_init(cr, registry):
  env = api.Environment(cr, SUPERUSER_ID, {})
