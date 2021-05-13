# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AppConfig(models.Model):
	_name = 'app.config'

	name = fields.Char('Nombre')
	# Parametros de la solicitud
	monto_minimo_solicitud = fields.Float('Monto minimo de solicitud')
	monto_maximo_solicitud = fields.Float('Monto maximo de solicitud')
	mensaje_sin_ofertas = fields.Text('Mensaje sin ofertas')
	numero_whatsapp_soporte = fields.Char('Numero whatsapp para soporte')
	app_ver_y_compartir_riesgo_cliente = fields.Boolean("Ver y compartir riesgo cliente")
	# deprecate
	monto_incremento = fields.Integer('Monto incremento')
	# deprecate
	monto_inicial = fields.Float('Monto inicial')
	# deprecate
	cuotas_minimas_solicitud = fields.Float('Cantidad minima de cuotas en solicitud')
	# deprecate
	cuotas_maximas_solicitud = fields.Float('Cantidad maxima de cuotas en solicitud')
	# deprecate
	cuotas_incremento = fields.Integer('Cantidad de incremento')
	# deprecate
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
	# Ver menu
	invisible_menu_datos_personales_incompletos = fields.Boolean('Ocultar menu datos personales incompletos')
	invisible_menu_datos_domicilio_incompletos = fields.Boolean('Ocultar menu datos domicilio incompletos')
	invisible_menu_datos_ingreso_incompletos = fields.Boolean('Ocultar menu datos de ingreso incompletos')
	invisible_menu_datos_vivienda_transporte_incompletos = fields.Boolean('Ocultar menu datos de vivienda y transporte incompletos')
	invisible_menu_cbu_incompletos = fields.Boolean('Ocultar menu CBU incompleto')
	invisible_menu_celular_validado_incompletos = fields.Boolean('Ocultar menu validar celular incompleto')
	# Planes disponibles
	planes_disponibles_ids = fields.Many2many('financiera.prestamo.plan', 'financiera_config_plan_rel', 'plan_id', 'config_id', string='Planes disponibles')
	# Requerimientos para solicitud
	requiere_state_validado = fields.Boolean("Requiere validar identidad")
	# para esta validado son las siguientes validaciones parciales
	requiere_datos_personales = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere datos personales completos')
	requiere_datos_dni_frontal = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere DNI frontal')
	requiere_datos_dni_dorso = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere DNI dorso')
	requiere_datos_selfie = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere selfie')
	# Otros requerimientos
	requiere_datos_domicilio = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere datos domicilio completos')
	requiere_datos_domicilio_documento = fields.Boolean('Requiere documento para validar domicilio')
	requiere_datos_ingreso = fields.Boolean('Requiere datos de ingresos completos')
	requiere_datos_vivienda_transporte = fields.Boolean('Requiere datos de vivienda y transporte completos')
	requiere_cbu = fields.Selection([
		('completo', 'Completos'),
		('validado', 'Validado'),
	], 'Requiere CBU')
	requiere_cbu_documento = fields.Boolean('Requiere documento para validar CBU')
	requiere_celular_validado = fields.Boolean('Requiere celular validado')
	requiere_tarjeta_debito = fields.Boolean('Requiere tarjeta de debito')
	requiere_tarjeta_debito_vencimiento = fields.Integer('Porcentaje de cobertura de cuotas segun vencimiento de la tarjeta',
		help="Ej: 100 el vencimiento de la tajeta debera ser posterior al vencimiento de la ultima cuota.")
	# condiciones
	metodo_confirmacion_tc = fields.Selection([
		('manual', 'Manual'),
		('sms', 'Terminos y Condiciones por SMS'),
		('email', 'Terminos y Condiciones por Email'),
		('email_sms', 'Terminos y Condiciones por Email y codigo por SMS'),
	], "Metodo de confirmacion de TC", default="manual")
	metodo_confirmacion_tc_agregar_mobbex_suscripcion = fields.Boolean("TC requiere suscripcion exitosa de tarjeta de debito")
	comprobar_codigo_prestamo = fields.Boolean("Comprobar codigo del prestamo adjunto en email o sms")
	comprobar_mensaje_original = fields.Boolean("Comprobar si la respuesta por mail contiene el mensaje original")
	# Requisitos prestamo portal
	app_requiere_direccion = fields.Boolean("Requiere direccion")
	app_requiere_cbu = fields.Boolean("Requiere CBU")
	app_requiere_trabajo_actual = fields.Boolean("Requiere trabajo actual")
	app_requiere_contactos = fields.Integer("Requiere contactos")
	app_requeire_tarjeta_debito = fields.Boolean("Requiere trajeta de debito")
	app_requiere_dni_frontal = fields.Boolean("requiere DNI frontal")
	app_requiere_dni_dorso = fields.Boolean("requiere DNI dorso")
	app_requiere_selfie = fields.Boolean("Requiere selfie")
	app_requiere_recibo_sueldo = fields.Boolean("Requiere recibo de sueldo")
	app_requiere_servicio = fields.Boolean("Requiere servicio")
	app_requiere_firma = fields.Boolean("Requiere firma")

	@api.onchange('requiere_state_validado')
	def _onchange_requiere_state_validado(self):
		if self.requiere_state_validado == True:
			self.requiere_datos_personales = 'validado'
			self.requiere_datos_dni_frontal = 'validado'
			self.requiere_datos_dni_dorso = 'validado'
			self.requiere_datos_selfie = 'validado'
		else:
			self.requiere_datos_personales = False
			self.requiere_datos_dni_frontal = False
			self.requiere_datos_dni_dorso = False
			self.requiere_datos_selfie = False
	
	@api.onchange('requiere_datos_personales', 'requiere_datos_dni_frontal', 
		'requiere_datos_dni_dorso', 'requiere_datos_selfie')
	def _onchange_requiere_state_validado_parametros(self):
		if self.requiere_datos_personales == 'validado' and self.requiere_datos_dni_frontal == 'validado' \
			and self.requiere_datos_dni_dorso == 'validado' and self.requiere_datos_selfie == 'validado':
			self.requiere_state_validado = True
		else:
			self.requiere_state_validado = False
