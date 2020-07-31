# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AppConfig(models.Model):
	_name = 'app.config'

	name = fields.Char('Nombre')
	# Parametros de la solicitud
	monto_minimo_solicitud = fields.Float('Monto minimo de solicitud')
	monto_maximo_solicitud = fields.Float('Monto maximo de solicitud')
	monto_incremento = fields.Integer('Monto incremento')
	monto_inicial = fields.Float('Monto inicial')
	cuotas_minimas_solicitud = fields.Float('Cantidad minima de cuotas en solicitud')
	cuotas_maximas_solicitud = fields.Float('Cantidad maxima de cuotas en solicitud')
	cuotas_incremento = fields.Integer('Cantidad de incremento')
	cuotas_inicial = fields.Float('Cantidad de cuotas inicial')
	# Opciones movil
	app_sucursal_id = fields.Many2one('financiera.entidad', 'Sucursal')
	app_comercio_id = fields.Many2one('financiera.entidad', 'Comercio')
	app_responsable_id = fields.Many2one('res.users', 'Responsable')
	app_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en movil')
	# Opciones portal
	portal_sucursal_id = fields.Many2one('financiera.entidad', 'Sucursal')
	portal_comercio_id = fields.Many2one('financiera.entidad', 'Comercio')
	portal_responsable_id = fields.Many2one('res.users', 'Responsable')
	portal_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en portal')
	# unique_documentation_report = fields.Char('Nombre del reporte unico a firmar por el cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False)
	# Requerimientos para solicitud
	requiere_state_validado = fields.Boolean("Requiere validar identidad")
	# para esta validado son las siguientes validaciones parciales
	requiere_datos_personales = fields.Boolean('Requiere datos personales completos')
	requiere_datos_dni_frontal = fields.Boolean('Requiere DNI frontal')
	requiere_datos_dni_dorso = fields.Boolean('Requiere DNI dorso')
	requiere_datos_selfie = fields.Boolean('Requiere selfie')
	# Otros requerimientos
	requiere_datos_domicilio = fields.Boolean('Requiere datos domicilio completos')
	requiere_datos_ingreso = fields.Boolean('Requiere datos de ingresos completos')
	requiere_datos_vivienda_transporte = fields.Boolean('Requiere datos de vivienda y transporte completos')
	requiere_cbu = fields.Boolean('Requiere CBU para deposito del capital')
	requiere_celular_validado = fields.Boolean('Requiere celular validado')
	
	# condiciones
	metodo_confirmacion_tc = fields.Selection([
		('manual', 'Manual'),
		('sms', 'Terminos y Condiciones por SMS'),
		('email', 'Terminos y Condiciones por Email'),
		('email_sms', 'Terminos y Condiciones por Email y codigo por SMS'),
	], "Metodo de confirmacion de TC", default="manual")
	comprobar_codigo_prestamo = fields.Boolean("Comprobar codigo del prestamo adjunto en email o sms")
	comprobar_mensaje_original = fields.Boolean("Comprobar si la respuesta por mail contiene el mensaje original")

	@api.onchange('requiere_state_validado')
	def _onchange_requiere_state_validado(self):
		if self.requiere_state_validado == True:
			self.requiere_datos_personales = True
			self.requiere_datos_dni_frontal = True
			self.requiere_datos_dni_dorso = True
			self.requiere_datos_selfie = True
		else:
			self.requiere_datos_personales = False
			self.requiere_datos_dni_frontal = False
			self.requiere_datos_dni_dorso = False
			self.requiere_datos_selfie = False
	
	@api.onchange('requiere_datos_personales', 'requiere_datos_dni_frontal', 
		'requiere_datos_dni_dorso', 'requiere_datos_selfie')
	def _onchange_requiere_state_validado_parametros(self):
		if self.requiere_datos_personales and self.requiere_datos_dni_frontal \
			and self.requiere_datos_dni_dorso and self.requiere_datos_selfie:
			self.requiere_state_validado = True
		else:
			self.requiere_state_validado = False
