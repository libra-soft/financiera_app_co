# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from dateutil import relativedelta
from cStringIO import StringIO
import base64

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_portal_state = fields.Selection([
		('datos_validaciones', 'Validaciones'),
		('datos_personales', 'Datos personales'),
		('datos_domicilio', 'Domicilio'),
		('datos_ingreso', 'Ingreso'),
		('datos_vivienda_transporte', 'Vivienda y transporte'),
		('datos_dni_frontal', 'DNI frontal'),
		('datos_dni_dorso', 'DNI dorso'),
		('datos_selfie', 'Selfie'),
		('datos_cbu', 'CBU'),
		('datos_numero_celular', 'Numero celular')],
    'Estado', default='datos_validaciones')

	app_datos_personales = fields.Boolean('Datos personales completos')
	app_nombre = fields.Char('Nombre')
	app_apellido = fields.Char('Apellido')
	app_documento = fields.Char('Documento')
	app_nacimiento = fields.Date('Nacimiento')
	# Datos Domicilio
	app_datos_domicilio = fields.Boolean('Datos domicilio completos')
	app_direccion = fields.Char('Direccion')
	app_numero = fields.Char('Numero')
	app_cp = fields.Char('CP')
	app_telefono = fields.Char('Telefono fijo')
	app_localidad = fields.Char('Localidad')
	app_provincia = fields.Char('Provincia')
	# Datos Ingreso
	app_datos_ingreso = fields.Boolean('Datos de ingreso completos')
	app_ingreso = fields.Char("Ingreso")
	app_cuotas = fields.Char("Cuotas")
	app_ingreso_pareja = fields.Char("Ingreso de la pareja")
	app_otros_ingresos = fields.Char("Otros ingresos")
	app_asignaciones = fields.Char("Asignaciones")
	app_ocupacion = fields.Char("ocupacion")
	app_puesto = fields.Char("Puesto")
	# Datos vivienda y transporte
	app_datos_vivienda_transporte = fields.Boolean("Datos de vivienda y transporte completos")
	app_vivienda = fields.Char("Vivienda")
	app_portal_vivienda = fields.Selection([
		('alquilada', 'Alquilada'),
		('propia', 'Propia')
	], "Vivienda")
	app_alquiler = fields.Char("Monto alquiler")
	app_hipoteca = fields.Char("Credito hipotecario")
	app_vivienda_tiempo = fields.Char("Anos que vive ahi")
	app_vivienda_conviven = fields.Char("Personas que conviven")
	app_vivienda_hijos = fields.Char("Hijos que conviven")
	app_transporte = fields.Char("Transporte")
	app_portal_transporte = fields.Selection([
		('publico', 'Publico'),
		('auto', 'Auto'),
		('moto', 'Moto')
	], "Medio de transporte")
	app_prendario = fields.Char("Credito prendario")
	# DNI y selfie
	app_datos_dni_frontal = fields.Boolean("Datos completos de DNI frontal")
	app_dni_frontal = fields.Binary("DNI frontal", store=True, attachment=False)
	app_dni_frontal_download = fields.Binary("", related="app_dni_frontal")
	app_dni_frontal_download_name = fields.Char("", default="dni-frontal.jpeg")
	app_datos_dni_posterior = fields.Boolean("Datos completos de DNI dorso")
	app_dni_posterior = fields.Binary("DNI dorso")
	app_dni_posterior_download = fields.Binary("", related="app_dni_posterior")
	app_dni_posterior_download_name = fields.Char("", default="dni-dorso.jpeg")
	app_datos_selfie = fields.Boolean("Datos completos de selfie")
	app_selfie = fields.Binary("Selfie")
	app_selfie_download = fields.Binary("", related="app_selfie")
	app_selfie_download_name = fields.Char("", default="selfie.jpeg")
	# CBU
	app_datos_cbu = fields.Boolean("Datos completos de CBU")
	app_cbu = fields.Char("CBU")
	app_alias = fields.Char("Alias")
	
	app_validacion_celular_activa = fields.Boolean("Validacion celular activa?", related="company_id.sms_configuracion_id.validacion_celular_codigo", readonly=True)
	app_numero_celular = fields.Char("Numero de celular")
	app_numero_celular_validado = fields.Boolean("Celular validado?")
	app_codigo_introducido_usuario = fields.Char("Codigo")
	app_codigo = fields.Char("Codigo generado")
	app_button_solicitar_codigo_fecha_reset = fields.Datetime("Fecha fin")

	@api.one
	@api.onchange('app_portal_vivienda')
	def _onchange_app_portal_vivienda(self):
		self.app_vivienda = self.app_portal_vivienda
	
	@api.one
	@api.onchange('app_portal_transporte')
	def _onchange_app_portal_transporte(self):
		self.app_transporte = self.app_portal_transporte

	# Datos personales
	@api.one
	def button_editar_datos_personales(self):
		self.app_portal_state = 'datos_personales'

	@api.one
	def button_confirmar_datos_personales(self):
		self.app_datos_personales = True
		self.app_portal_state = 'datos_validaciones'

	# Datos domicilio
	@api.one
	def button_editar_datos_domicilio(self):
		self.app_portal_state = 'datos_domicilio'

	@api.one
	def button_confirmar_datos_domicilio(self):
		self.app_datos_domicilio = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos ingreso
	@api.one
	def button_editar_datos_ingreso(self):
		self.app_portal_state = 'datos_ingreso'

	@api.one
	def button_confirmar_datos_ingreso(self):
		self.app_datos_ingreso = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos vivienda y transporte
	@api.one
	def button_editar_datos_vivienda_transporte(self):
		self.app_portal_state = 'datos_vivienda_transporte'

	@api.one
	def button_confirmar_datos_vivienda_transporte(self):
		self.app_datos_vivienda_transporte = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos DNI frontal
	@api.one
	def button_editar_datos_dni_frontal(self):
		self.app_portal_state = 'datos_dni_frontal'
	
	@api.one
	def button_confirmar_datos_dni_frontal(self):
		self.app_datos_dni_frontal = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos DNI posterior
	@api.one
	def button_editar_datos_dni_posterior(self):
		self.app_portal_state = 'datos_dni_dorso'
	
	@api.one
	def button_confirmar_datos_dni_posterior(self):
		self.app_datos_dni_posterior = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos selfie
	@api.one
	def button_editar_datos_selfie(self):
		self.app_portal_state = 'datos_selfie'
	
	@api.one
	def button_confirmar_datos_selfie(self):
		self.app_datos_selfie = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos cbu
	@api.one
	def button_editar_datos_cbu(self):
		self.app_portal_state = 'datos_cbu'
	
	@api.one
	def button_confirmar_datos_cbu(self):
		self.app_datos_cbu = True
		self.app_portal_state = 'datos_validaciones'
	
	# Datos numero celular
	@api.one
	def button_editar_datos_numero_celular(self):
		self.app_portal_state = 'datos_numero_celular'
	
	@api.one
	def button_confirmar_datos_numero_celular(self):
		if self.app_codigo == self.app_codigo_introducido_usuario:
			self.app_numero_celular_validado = True
			self.mobile = self.app_numero_celular
			self.app_codigo = None
		else:
			raise UserError("El codigo no coincide.")
		self.app_portal_state = 'datos_validaciones'

	@api.one
	def button_solicitar_codigo_portal(self):
		print("app_button_solicitar_codigo_fecha_reset:: ", self.app_button_solicitar_codigo_fecha_reset)
		if self.app_button_solicitar_codigo_fecha_reset == False or self.app_button_solicitar_codigo_fecha_reset == None:
			self.sudo().button_solicitar_codigo()
			self.app_button_solicitar_codigo_fecha_reset = datetime.now() + timedelta(seconds=+120)
		else:
			fecha_fin = datetime.strptime(self.app_button_solicitar_codigo_fecha_reset, '%Y-%m-%d %H:%M:%S')
			if datetime.now() < fecha_fin:
				diferencia = fecha_fin - datetime.now()
				raise UserError("Vuelva a intentarlo en: "+str(diferencia.seconds // 60)+":"+str(diferencia.seconds % 60).zfill(2)+" segundos")
			else:
				self.app_button_solicitar_codigo_fecha_reset = None
				self.app_codigo = None
				self.button_solicitar_codigo_portal()