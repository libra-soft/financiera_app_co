# -*- coding: utf-8 -*-

import openerp
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

	# Identidad
	app_identidad_validada = fields.Boolean("Identidad validada", compute="_compute_app_identidad_validada")
	app_identidad_validada_aprobacion_manual = fields.Boolean('Aprobacion manual', compute="_compute_app_identidad_validada_aprobacion_manual")
	# Datos Personales
	app_datos_personales = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], 'Datos personales')
	app_datos_personales_error = fields.Char('Error datos personales')
	app_nombre = fields.Char('Nombre')
	app_apellido = fields.Char('Apellido')
	app_documento = fields.Char('Documento')
	app_nacimiento = fields.Date('Nacimiento')
	# Datos Domicilio
	app_datos_domicilio = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], 'Datos domicilio')
	app_datos_domicilio_error = fields.Char('Error')
	app_direccion = fields.Char('Direccion')
	app_numero = fields.Char('Numero')
	app_cp = fields.Char('CP')
	app_telefono = fields.Char('Telefono fijo')
	app_localidad = fields.Char('Localidad')
	app_portal_provincia = fields.Many2one('res.country.state', "Provincia")
	app_provincia = fields.Char('Provincia')
	app_domicilio_documento = fields.Binary("Documentacion que confirme su domicilio", store=True, attachment=False)
	app_domicilio_documento_download = fields.Binary("", related="app_domicilio_documento")
	# app_domicilio_documento_download_name = fields.Char("", default="domicilio")
	# Datos Ingreso
	app_datos_ingreso = fields.Boolean('Datos de ingreso completos')
	app_ingreso = fields.Char("Ingreso")
	app_cuotas = fields.Char("Cuotas")
	app_ingreso_pareja = fields.Char("Ingreso de la pareja")
	app_otros_ingresos = fields.Char("Otros ingresos")
	app_asignaciones = fields.Char("Asignaciones")
	app_portal_ocupacion = fields.Selection([
		('empleado_privado', 'Empleado privado'),
		('empleado_publico', 'Empleado publico'),
		('autonomo', 'Autonomo'),
		('monotributo', 'Monotributo'),
		('pensionado', 'Pensionado'),
		('jubilado', 'Jubilado'),
		('desempleado', 'Desempleado'),
		], "Ocupacion")
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
	# DNI frente
	app_datos_dni_frontal = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos correctos de DNI frontal")
	app_datos_dni_frontal_error = fields.Char("Error")
	app_dni_frontal = fields.Binary("DNI frontal", store=True, attachment=False)
	app_dni_frontal_download = fields.Binary("", related="app_dni_frontal")
	app_dni_frontal_download_name = fields.Char("", default="dni-frontal.jpeg")
	# DNI dorso
	app_datos_dni_posterior = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos correctos de DNI dorso")
	app_datos_dni_posterior_error = fields.Char("Error")
	app_dni_posterior = fields.Binary("DNI dorso")
	app_dni_posterior_download = fields.Binary("", related="app_dni_posterior")
	app_dni_posterior_download_name = fields.Char("", default="dni-dorso.jpeg")
	# Selfie
	app_datos_selfie = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos correctos de selfie")
	app_datos_selfie_error = fields.Char("Error")
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
	# # requerimientos de perfil
	requiere_state_validado = fields.Boolean("Requiere estado validado", readonly=True, related='company_id.app_id.requiere_state_validado')
	requiere_datos_personales = fields.Boolean('Requiere datos personales completos', readonly=True, related='company_id.app_id.requiere_datos_personales')
	requiere_datos_dni_frontal = fields.Boolean('Requiere DNI frontal', readonly=True, related='company_id.app_id.requiere_datos_dni_frontal')
	requiere_datos_dni_dorso = fields.Boolean('Requiere DNI dorso', readonly=True, related='company_id.app_id.requiere_datos_dni_dorso')
	requiere_datos_selfie = fields.Boolean('Requiere selfie', readonly=True, related='company_id.app_id.requiere_datos_selfie')
	requiere_datos_domicilio = fields.Boolean('Requiere datos domicilio completos', readonly=True, related='company_id.app_id.requiere_datos_domicilio')
	requiere_datos_ingreso = fields.Boolean('Requiere datos de ingresos completos', readonly=True, related='company_id.app_id.requiere_datos_ingreso')
	requiere_datos_vivienda_transporte = fields.Boolean('Requiere datos de vivienda y transporte completos', readonly=True, related='company_id.app_id.requiere_datos_vivienda_transporte')
	requiere_cbu = fields.Boolean('Requiere CBU para deposito del capital', readonly=True, related='company_id.app_id.requiere_cbu')
	requiere_celular_validado = fields.Boolean('Requiere celular validado', readonly=True, related='company_id.app_id.requiere_celular_validado')
	

	@api.one
	def _compute_app_identidad_validada(self):
		self.app_identidad_validada = self.state == 'validated'

	@api.onchange('app_datos_personales', 'app_datos_dni_frontal', 'app_datos_dni_posterior', 'app_datos_selfie')
	def _onchange_identidad_validada(self):
		if self.app_datos_personales == 'aprobado' and self.app_datos_dni_frontal == 'aprobado' \
				and self.app_datos_dni_posterior == 'aprobado' and self.app_datos_selfie == 'aprobado':
			self.state = 'validated'
		elif self.state == 'validated':
			self.state = 'confirm'

	@api.one
	def _compute_app_identidad_validada_aprobacion_manual(self):
		rechazados = self.app_datos_personales == 'rechazado' or self.app_datos_dni_frontal == 'rechazado' \
			or self.app_datos_dni_posterior == 'rechazado' or self.app_datos_selfie == 'rechazado'
		self.app_identidad_validada_aprobacion_manual = self.state != 'validated' and not rechazados

	@api.one
	def button_regresar(self):
		self.app_portal_state = 'datos_validaciones'

	# Datos personales
	@api.one
	def button_editar_datos_validar_identidad(self):
		if self.app_datos_personales == 'rechazado':
			self.app_portal_state = 'datos_personales'
		elif self.app_datos_dni_frontal == 'rechazado':
			self.app_portal_state = 'datos_dni_frontal'
		elif self.app_datos_dni_posterior == 'rechazado':
			self.app_portal_state = 'datos_dni_dorso'
		elif self.app_datos_selfie == 'rechazado':
			self.app_portal_state = 'datos_selfie'
		else:
			if self.app_portal_state == 'datos_validaciones':
				self.app_portal_state = 'datos_personales'
				# raise UserError("Todos los datos estan completos.")
			else:
				# check si esta en aprobacion manual algun dato hay que generar el objeto
				self.app_portal_state = 'datos_validaciones'

	@api.one
	def button_confirmar_datos_personales(self):
		self.main_id_number = self.app_documento
		self.confirm()
		self.app_datos_personales = 'manual'
		self.button_editar_datos_validar_identidad()
		# self.app_portal_state = 'datos_dni_frontal'

	# @api.constrains('app_nombre', 'app_apellido', 'app_documento', 'app_nacimiento')
	# def _check_datos_personales(self):
	# 	if self.env.user.id != openerp.SUPERUSER_ID:
	# 		for record in self:
	# 			if not record.app_nombre or (record.app_nombre and len(record.app_nombre) <= 2):
	# 				raise UserError("Nombre es requerido y debe tener mas de 2 caracteres.")
	# 			if not record.app_apellido or (record.app_apellido and len(record.app_apellido) <= 2):
	# 				raise UserError("Apellido es requerido y debe tener mas de 2 caracteres.")
	# 			if not record.app_documento or (record.app_documento and not record.app_documento.isdigit()):
	# 				raise UserError("Documento es requerido y deben ser solo numeros.")
	# 			if not record.app_nacimiento:
	# 				raise UserError("Nacimiento es requerido.")
	
	# Datos DNI frontal
	@api.one
	def button_editar_datos_dni_frontal(self):
		self.app_portal_state = 'datos_dni_frontal'
	
	@api.one
	def button_confirmar_datos_dni_frontal(self):
		self.app_datos_dni_frontal = 'manual'
		self.button_editar_datos_validar_identidad()
	
	# Datos DNI posterior
	@api.one
	def button_editar_datos_dni_posterior(self):
		self.app_portal_state = 'datos_dni_dorso'
	
	@api.one
	def button_confirmar_datos_dni_posterior(self):
		self.app_datos_dni_posterior = 'manual'
		self.button_editar_datos_validar_identidad()

	# Datos selfie
	@api.one
	def button_editar_datos_selfie(self):
		self.app_portal_state = 'datos_selfie'
	
	@api.one
	def button_confirmar_datos_selfie(self):
		self.app_datos_selfie = 'manual'
		self.button_editar_datos_validar_identidad()
	
	# Datos domicilio
	@api.one
	def button_editar_datos_domicilio(self):
		self.app_portal_state = 'datos_domicilio'

	@api.one
	def button_confirmar_datos_domicilio(self):
		self.app_datos_domicilio = 'manual'
		self.app_portal_state = 'datos_validaciones'

	@api.one
	def button_modificar_domicilio(self):
		self.app_datos_domicilio = 'rechazado'
		self.app_domicilio_documento = False

	@api.onchange('app_portal_provincia')
	def _onchange_app_portal_provincia(self):
		self.app_provincia = self.app_portal_provincia.name
	
	# @api.onchange('app_direccion', 'app_numero', 'app_cp', 'app_localidad')
	# def _onchange_app_datos_domicilio(self):
	# 	direccion_correcta = self.app_direccion and len(self.app_direccion) > 3
	# 	numero_correcto = not self.app_numero or (self.app_numero != False and self.app_numero.isdigit())
	# 	cp_correcto = not self.app_cp or (self.app_cp != False and self.app_cp.isdigit())
	# 	localidad_correcta = self.app_localidad != False and len(self.app_localidad) > 3
	# 	provincia_correcta = self.app_provincia != False
	# 	self.app_datos_domicilio = direccion_correcta and numero_correcto and cp_correcto and localidad_correcta and provincia_correcta

	# Datos ingreso
	@api.one
	def button_editar_datos_ingreso(self):
		self.app_portal_state = 'datos_ingreso'

	@api.one
	def button_confirmar_datos_ingreso(self):
		self.app_datos_ingreso = True
		self.app_portal_state = 'datos_validaciones'

	# @api.constrains('app_ingreso')
	# def _check_app_ingreso(self):
	# 	if self.env.user.id != openerp.SUPERUSER_ID:
	# 		for record in self:
	# 			if not record.app_ingreso.isdigit():
	# 				raise UserError("Ingreso neto permite solo numeros.")

	@api.onchange('app_portal_ocupacion')
	def _onchange_app_portal_ocupacion(self):
		if self.app_portal_ocupacion:
			if self.app_portal_ocupacion == 'empleado_privado':
				self.app_ocupacion = 'Empleado privado'
			elif self.app_portal_ocupacion == 'empleado_publico':
				self.app_ocupacion = 'Empleado publico'
			else:
				self.app_ocupacion = self.app_portal_ocupacion.capitalize()
		else:
			self.app_ocupacion = False
	
	# Datos vivienda y transporte
	@api.one
	def button_editar_datos_vivienda_transporte(self):
		self.app_portal_state = 'datos_vivienda_transporte'

	@api.one
	def button_confirmar_datos_vivienda_transporte(self):
		self.app_datos_vivienda_transporte = True
		self.app_portal_state = 'datos_validaciones'

	# @api.constrains('app_ingreso', 'app_alquiler', 'app_hipoteca', 'app_vivienda_tiempo',
	# 	'app_vivienda_conviven', 'app_vivienda_hijos', 'app_prendario')
	# def _check_app_vivienda(self):
	# 	if self.env.user.id != openerp.SUPERUSER_ID:
	# 		for record in self:
	# 			if record.app_alquiler and not record.app_alquiler.isdigit():
	# 				raise UserError("Cuota paga de alquiler?\n Permite solo numeros.")
	# 			if record.app_hipoteca and not record.app_hipoteca.isdigit():
	# 				raise UserError("Cuanto paga de hipoteca?\n Permite solo numeros.")
	# 			if not record.app_vivienda_tiempo.isdigit():
	# 				raise UserError("Cuantos años hace que vivie ahí?\n Permite solo numeros.")
	# 			if not record.app_vivienda_conviven.isdigit():
	# 				raise UserError("Con cuantas personas convive?\n Permite solo numeros.")
	# 			if not record.app_vivienda_hijos.isdigit():
	# 				raise UserError("Con cuantos hijos conviven?\n Permite solo numeros.")
	# 			if record.app_prendario and not record.app_prendario.isdigit():
	# 				raise UserError("Tiene un prestamo prendario?\n Permite solo numeros, 0 si no corresponde.")

	@api.onchange('app_portal_vivienda')
	def _onchange_app_portal_vivienda(self):
		self.app_vivienda = self.app_portal_vivienda
	
	@api.onchange('app_portal_transporte')
	def _onchange_app_portal_transporte(self):
		self.app_transporte = self.app_portal_transporte

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