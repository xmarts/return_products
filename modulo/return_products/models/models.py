# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, time, timedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class fecha_limit(models.Model):
	_inherit = 'sale.order'

	fecha_limit = fields.Date(string="date limtit return")


class opciondevolucion(models.Model):

	_inherit ='stock.picking.type'

	client_devo = fields.Boolean(string="Return client")
	provee_devo =fields.Boolean(string="supplier return")



class devolucion_produ(models.Model):
	_name = 'return.clien'

	num_clie = fields.Char(string="Number client")
	nombre_clien =fields.Many2one('res.partner',string="Name client")
	estado_clien = fields.Many2one('res.country.state',string="State")
	cuidad_clien = fields.Char(string="City")
	codi_pos_clien = fields.Char(string="Postal client")
	fecha_actual = fields.Date(string="Date",default=fields.Date.today())
	busqueda = fields.Char(string="Buscar serie")
	state = fields.Selection([('draft','Draft'),('approve','Approved'),('review','Review piece'),('state','good condition'),('default','manufacturing'),('process','Processing'),('reject','Rejected')],default='draft')
	tabla = fields.One2many('product.validar', 'tabla_1')
	tablados = fields.One2many('product.rechazado','tabla_2')
	rel = fields.Char(string="relacion")

	@api.one
	def buscar(self):
		res = self.env['stock.move.line'].search([('lot_id', '=', self.busqueda)], limit=1)

		if res:
			self.rel = res.reference
			inv_obj = self.env['product.validar']
			self.ensure_one()
			invoice = inv_obj.create({'producto': res.product_id.id,
									'serie':res.lot_id.id,
									'pedido_venta': res.reference,
									'fecha_compra': res.date,
									'estatus':res.state,
									'tabla_1': self.id
									})

			if invoice:
				datos = self.env['stock.picking'].search([('name', '=', self.rel)], limit=1)
				self.nombre_clien = datos.partner_id.id
				self.cuidad_clien = datos.partner_id.city
				self.estado_clien = datos.partner_id.state_id.id
				self.codi_pos_clien = datos.partner_id.zip

		if self.busqueda == False:
			raise ValidationError('!Registre una serie el campo esta basio¡')

		if self.picking_id.sale_id.fecha_limit:
           # if self.picking_id.sale_id.fecha_limit > self.fecha_actual:
            #    self.write({'state':'approve'})
            #else:
             #   self.write({'state':'reject'})	

	
	@api.one
	def confirmar(self):
		self.write({'state':'approve'})
	@api.one
	def rev(self):
		self.write({'state':'review'})
	@api.one
	def ste(self):
		self.write({'state':'state'})

	@api.one
	def defa(self):
		self.write({'state':'default'})
		
								
	('process','Processing'),('reject','Rejected')],default='draft')

class tabla(models.Model):
	_name= 'product.validar'

	tabla_1 = fields.Many2one('return.clien',ondelete='cascade')
	producto = fields.Many2one('product.product',string="Product")
	talla  = fields.Char(string="Talla")
	serie = fields.Many2one('stock.production.lot',string="Serie")
	pedido_venta = fields.Char(string="Pedido ")
	fecha_compra = fields.Datetime(string="Fecha ")
	estatus = fields.Char(string="Estatus")
	motivo = fields.Char(string="Motivo")
	pregresar_proveedor = fields.Boolean(string="Regresar ", default=False)
	total_acept  = fields.Integer(string="Total aceptados")
	total_recha = fields.Integer(string="Total rechazados")



class tablados(models.Model):
	_name = 'product.rechazado'

	tabla_2 = fields.Many2one('return.clien',ondelete='cascade')
	producto_r = fields.Char(string="Product")
	talla_r  = fields.Float(string="Talla")
	serie_r = fields.Integer(string="Serie")
	pedido_venta_r = fields.Char(string="Pedido de venta")
	fecha_compra_r = fields.Date(string="Fecha de compra")
	estatus_r = fields.Char(string="Estatus")
	motivo_r = fields.Char(string="Motivo")
	total_recha_por_cal = fields.Integer(string="Total aceptados")
	total_prod_esc = fields.Integer(string="Total rechazados")	




						
