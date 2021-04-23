# -*- coding: utf-8 -*-

import openerp
from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging
import json
# from dateutil import relativedelta
# from cStringIO import StringIO
# import base64

_logger = logging.getLogger(__name__)

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_estado_portal = fields.Char("Estado portal")
	app_estado_bloqueado = fields.Boolean("Usuario bloqueado")
	app_ip_registro = fields.Char("IP al registrarse")
	app_ip_registro_no_confiable = fields.Boolean("IP no confiable")
	# obsoleto
	app_portal_state = fields.Selection([
		('datos_validaciones', 'Validaciones'),
		('datos_personales', 'Datos personales'),
		('datos_domicilio', 'Domicilio'),
		('datos_ingreso', 'Ingreso'),
		('datos_vivienda_transporte', 'Vivienda y transporte'),
		('datos_dni_selfie', 'Datos DNI y selfie'),
		('datos_dni_frontal', 'DNI frontal'),
		('datos_dni_dorso', 'DNI dorso'),
		('datos_selfie', 'Selfie'),
		('datos_cbu', 'CBU'),
		('datos_numero_celular', 'Numero celular')],
    'Estado', default='datos_personales')

	# Identidad
	app_identidad_validada = fields.Boolean("Identidad validada", compute="_compute_app_identidad_validada")
	app_identidad_validada_aprobacion_manual = fields.Boolean('Aprobacion manual', compute="_compute_app_identidad_validada_aprobacion_manual")
	# Datos Personales
	app_datos_personales = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], 'Datos personales', default='rechazado')
	app_datos_personales_error = fields.Char('Error datos personales')
	app_nombre = fields.Char('Nombre')
	app_apellido = fields.Char('Apellido')
	app_documento = fields.Char('Documento')
	app_nacimiento = fields.Date('Nacimiento')
	app_edad = fields.Integer('Edad')
	# Datos Domicilio
	app_datos_domicilio = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], 'Datos domicilio', default='rechazado')
	app_datos_domicilio_error = fields.Char('Error')
	app_direccion = fields.Char('Direccion')
	app_numero = fields.Char('Numero')
	app_cp = fields.Char('CP')
	app_telefono = fields.Char('Telefono fijo')
	app_localidad = fields.Char('Ciudad')
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
	], "Datos correctos de DNI frontal", default='rechazado')
	app_datos_dni_frontal_error = fields.Char("Error")
	app_dni_frontal = fields.Binary("DNI frontal", store=True, attachment=False)
	app_dni_frontal_download = fields.Binary("", related="app_dni_frontal")
	app_dni_frontal_download_name = fields.Char("", default="dni-frontal.jpeg")
	# DNI dorso
	app_datos_dni_posterior = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos correctos de DNI dorso", default='rechazado')
	app_datos_dni_posterior_error = fields.Char("Error")
	app_dni_posterior = fields.Binary("DNI dorso")
	app_dni_posterior_download = fields.Binary("", related="app_dni_posterior")
	app_dni_posterior_download_name = fields.Char("", default="dni-dorso.jpeg")
	# Selfie
	app_datos_selfie = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos correctos de selfie", default='rechazado')
	app_datos_selfie_error = fields.Char("Error")
	app_selfie = fields.Binary("Selfie", related='image')
	app_selfie_download = fields.Binary("", related="app_selfie")
	app_selfie_download_name = fields.Char("", default="selfie.jpeg")
	# CBU
	app_datos_cbu = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado'),
		('manual', 'Esperando aprobacion manual')
	], "Datos completos de CBU", default='rechazado')
	app_datos_cbu_error = fields.Char("Error")
	app_cbu_validado = fields.Char("CBU")
	app_alias_validado = fields.Char("Alias")
	app_cbu = fields.Char("CBU")
	app_alias = fields.Char("Alias")
	app_cbu_documento = fields.Binary("Documentacion que confirme su CBU", store=True, attachment=False)
	app_cbu_documento_download = fields.Binary("", related="app_cbu_documento")
	
	app_tarjeta_debito_digitos_fin = fields.Char("Ultimos 4 digitos de tu tarjeta de debito")
	app_tarjeta_debito_vencimiento_month = fields.Selection([
		(1, '01'), (2, '02'), (3, '03'), (4, '04'),
		(5, '05'), (6, '06'), (7, '07'), (8, '08'), 
		(9, '09'), (10, '10'), (11, '11'), (12, '12')], string='Mes')
	app_tarjeta_debito_vencimiento_year = fields.Selection([
		(2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'),
		(2025, '2025'), (2026, '2026'), (2027, '2027'), (2028, '2028'), (2029, '2029'),
		(2030, '2030'), (2031, '2031'), (2032, '2032'), (2033, '2033'), (2034, '2034'),
	], string='Año')
	app_tarjeta_debito_vencimiento = fields.Char("Vencimiento de tu tarjeta de debito (MMAA)")

	app_validacion_celular_activa = fields.Boolean("Validacion celular activa?", related="company_id.sms_configuracion_id.validacion_celular_codigo", readonly=True)
	app_numero_celular = fields.Char("Numero de celular", related='mobile')
	app_numero_celular_validado = fields.Boolean("Celular validado?")
	app_codigo_introducido_usuario = fields.Char("Codigo")
	app_codigo = fields.Char("Codigo generado")
	app_button_solicitar_codigo_fecha_reset = fields.Datetime("Fecha fin")
	app_primer_ingreso = fields.Boolean("Primer ingreso", default=True)
	# # requerimientos de perfil
	requiere_state_validado = fields.Boolean("Requiere estado validado", readonly=True, related='company_id.app_id.requiere_state_validado')
	requiere_datos_personales = fields.Selection('Requiere datos personales completos', readonly=True, related='company_id.app_id.requiere_datos_personales')
	requiere_datos_dni_frontal = fields.Selection('Requiere DNI frontal', readonly=True, related='company_id.app_id.requiere_datos_dni_frontal')
	requiere_datos_dni_dorso = fields.Selection('Requiere DNI dorso', readonly=True, related='company_id.app_id.requiere_datos_dni_dorso')
	requiere_datos_selfie = fields.Selection('Requiere selfie', readonly=True, related='company_id.app_id.requiere_datos_selfie')
	requiere_datos_domicilio = fields.Selection('Requiere datos domicilio completos', readonly=True, related='company_id.app_id.requiere_datos_domicilio')
	requiere_datos_domicilio_documento = fields.Boolean('Requiere documento para validar domicilio', readonly=True, related='company_id.app_id.requiere_datos_domicilio_documento')
	requiere_datos_ingreso = fields.Boolean('Requiere datos de ingresos completos', readonly=True, related='company_id.app_id.requiere_datos_ingreso')
	requiere_datos_vivienda_transporte = fields.Boolean('Requiere datos de vivienda y transporte completos', readonly=True, related='company_id.app_id.requiere_datos_vivienda_transporte')
	requiere_cbu = fields.Selection('Requiere CBU', readonly=True, related='company_id.app_id.requiere_cbu')
	requiere_cbu_documento = fields.Boolean('Requiere documento para validar CBU', readonly=True, related='company_id.app_id.requiere_cbu_documento')
	requiere_celular_validado = fields.Boolean('Requiere celular validado', readonly=True, related='company_id.app_id.requiere_celular_validado')
	requiere_tarjeta_debito = fields.Boolean('Requiere tarjeta de debito', readonly=True, related='company_id.app_id.requiere_tarjeta_debito')
	requiere_tarjeta_debito_vencimiento = fields.Integer('Porcentaje de cobertura de cuotas segun vencimiento de la tarjeta',
		readonly=True, related='company_id.app_id.requiere_tarjeta_debito_vencimiento')
	# menu del perfil a visualizar
	invisible_menu_datos_personales_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_datos_personales_incompletos')
	invisible_menu_datos_domicilio_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_datos_domicilio_incompletos')
	invisible_menu_datos_ingreso_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_datos_ingreso_incompletos')
	invisible_menu_datos_vivienda_transporte_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_datos_vivienda_transporte_incompletos')
	invisible_menu_cbu_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_cbu_incompletos')
	invisible_menu_celular_validado_incompletos = fields.Boolean(readonly=True, related='company_id.app_id.invisible_menu_celular_validado_incompletos')
	# Otros datos a adjuntar
	app_recibo_sueldo = fields.Binary("Recibo de sueldo")
	app_recibo_sueldo_download = fields.Binary("", related="app_recibo_sueldo")
	app_recibo_sueldo_download_name = fields.Char("", default="recibo.jpeg")
	
	app_servicio = fields.Binary("Servicio")
	app_servicio_download = fields.Binary("", related="app_servicio")
	app_servicio_download_name = fields.Char("", default="servicio.jpeg")
	app_observaciones = fields.Char("Observaciones")
	# alertas
	alerta_ultima_actualizacion = fields.Datetime("Alertas actualizadas al")
	alerta_ip_multiple_registros = fields.Integer('Registros desde la misma IP')
	alerta_ip_multiple_registros_ids = fields.Many2many('res.partner', 'alerta_ip_multiple_registros_rel', 'partner_id', 'partner2_id', string='Registros desde la misma IP')

	alerta_celular_multiple_partner = fields.Integer('Clientes con el mismo celular')
	alerta_celular_multiple_partner_ids = fields.Many2many('res.partner', 'alerta_celular_multiple_partner_rel', 'partner_id', 'partner2_id', string='Clientes con el mismo celular')

	alerta_celular_como_contacto = fields.Integer('Contactos con el mismo celular')
	alerta_celular_como_contacto_ids = fields.Many2many('res.partner.contacto', 'alerta_celular_como_contacto_rel', 'partner_id', 'partner2_id', string='Contactos con el mismo celular')

	alerta_domicilio_similar = fields.Integer('Clientes con domicilio similar')
	alerta_domicilio_similar_ids = fields.Many2many('res.partner', 'alerta_domicilio_similar_rel', 'partner_id', 'partner2_id', string='Clientes con domicilio similar')

	alerta_prestamos_activos = fields.Integer('Prestamos activos', store=True, compute='_compute_alerta_prestamos_activos')
	alerta_prestamos_cobrados = fields.Integer('Prestamos cobrados', store=True, compute='_compute_alerta_prestamos_cobrados')
	
	alerta_cuotas_activas = fields.Integer('Cuotas activas', store=True, compute='_compute_alerta_cuotas_activas')
	alerta_cuotas_cobradas = fields.Integer('Cuotas cobradas', store=True, compute='_compute_alerta_cuotas_cobradas')
	alerta_cuotas_normal = fields.Integer('Cuotas en preventiva', store=True, compute='_compute_alerta_cuotas_normal')
	alerta_cuotas_preventivas = fields.Integer('Cuotas en preventiva', store=True, compute='_compute_alerta_cuotas_preventivas')
	alerta_cuotas_temprana = fields.Integer('Cuotas en mora temprana', store=True, compute='_compute_alerta_cuotas_mora_temprana')
	alerta_cuotas_media = fields.Integer('Cuotas en mora media', store=True, compute='_compute_alerta_cuotas_mora_media')
	alerta_cuotas_tardia = fields.Integer('Cuotas en mora tardia', store=True, compute='_compute_alerta_cuotas_mora_tardia')
	alerta_cuotas_incobrable = fields.Integer('Cuotas incobrable', store=True, compute='_compute_alerta_cuotas_mora_incobrable')
	# Datos compartidos entre financieras
	alerta_ver_y_compartir = fields.Boolean('Ver y compartir', related='company_id.app_id.app_ver_y_compartir_riesgo_cliente')
	alerta_registrado_financieras = fields.Integer('Registros')
	alerta_prestamos_activos_financieras = fields.Integer('Prestamos activos')
	alerta_cuotas_vencidas_financieras = fields.Integer('Cuotas en mora')
	alerta_compromiso_mensual_financieras = fields.Float('Compromiso mensual')
	alerta_ip_no_confiable_financieras = fields.Integer('IP no confiable')

	@api.model
	def create(self, values):
		rec = super(ExtendsResPartner, self).create(values)
		rec.update({
			'app_portal_state': 'datos_validaciones',
			'app_datos_personales': 'rechazado',
			'app_datos_domicilio': 'rechazado',
			'app_datos_dni_frontal': 'rechazado',
			'app_datos_dni_posterior': 'rechazado',
			'app_datos_selfie': 'rechazado',
			'app_datos_cbu': 'rechazado',
		})
		return rec

	@api.multi
	def ver_partner_perfil_portal(self):
		view_id = self.env.ref('financiera_app.financiera_perfil_portal_form', False)
		return {
			'name': 'Mi perfil',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.env.user.partner_id.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'inline',
		}
	
	@api.one
	def button_primer_ingreso_siguiente(self):
		self.app_primer_ingreso
		if self.app_portal_state == 'datos_personales':
			self.button_confirmar_datos_personales()
			self.app_portal_state = 'datos_dni_selfie'
		elif self.app_portal_state == 'datos_dni_selfie':
			self.button_confirmar_datos_dni_selfie_upload()
			self.app_portal_state = 'datos_domicilio'
		elif self.app_portal_state == 'datos_domicilio':
			self.button_confirmar_datos_domicilio()
			if self.requiere_datos_ingreso:
				self.app_portal_state = 'datos_ingreso'
			elif self.requiere_datos_vivienda_transporte:
				self.app_portal_state = 'datos_vivienda_transporte'
			else:
				self.app_portal_state = 'datos_cbu'
		elif self.app_portal_state == 'datos_ingreso':
			self.button_confirmar_datos_ingreso()
			if self.requiere_datos_vivienda_transporte:
				self.app_portal_state = 'datos_vivienda_transporte'
			else:
				self.app_portal_state = 'datos_cbu'
		elif self.app_portal_state == 'datos_vivienda_transporte':
			self.button_confirmar_datos_vivienda_transporte()
			self.app_portal_state = 'datos_cbu'
		elif self.app_portal_state == 'datos_cbu':
			self.button_confirmar_datos_cbu()
			self.app_portal_state = 'datos_numero_celular'
		elif self.app_portal_state == 'datos_numero_celular':
			self.button_confirmar_datos_numero_celular()
			self.app_portal_state = 'datos_validaciones'
			self.app_primer_ingreso = False

	@api.one
	def _compute_app_identidad_validada(self):
		self.app_identidad_validada = self.state == 'validated'

	@api.one
	def _compute_app_identidad_validada_aprobacion_manual(self):
		rechazados = self.app_datos_personales == 'rechazado' or self.app_datos_dni_frontal == 'rechazado' \
			or self.app_datos_dni_posterior == 'rechazado' or self.app_datos_selfie == 'rechazado'
		self.app_identidad_validada_aprobacion_manual = self.state != 'validated' and not rechazados

	@api.one
	def button_regresar(self):
		if self.app_portal_state == 'datos_numero_celular':
			self.app_numero_celular = self.mobile
		self.app_portal_state = 'datos_validaciones'

	@api.one
	def button_confirmar_datos_personales(self):
		self.main_id_number = self.app_documento
		self.confirm()
		self.app_datos_personales = 'manual'
		self.app_portal_state = 'datos_validaciones'
	
	# Datos DNI frontal
	@api.one
	def button_editar_datos_dni_frontal(self):
		self.app_portal_state = 'datos_dni_frontal'

	@api.one
	def button_confirmar_datos_dni_selfie_upload(self):
		self.app_datos_dni_frontal = 'manual'
		self.app_datos_dni_posterior = 'manual'
		self.app_datos_selfie = 'manual'
		self.app_portal_state = 'datos_validaciones'

	@api.multi
	def button_confirmar_datos_dni_frontal(self):
		self.app_datos_dni_frontal = 'manual'
		return self.wizard_datos_dni_posterior()
	
	# Datos DNI posterior
	@api.one
	def button_editar_datos_dni_posterior(self):
		self.app_portal_state = 'datos_dni_dorso'
	
	@api.multi
	def button_confirmar_datos_dni_posterior(self):
		self.app_datos_dni_posterior = 'manual'
		return self.wizard_datos_selfie()

	# Datos selfie
	@api.one
	def button_editar_datos_selfie(self):
		self.app_portal_state = 'datos_selfie'
	
	@api.one
	def button_confirmar_datos_selfie(self):
		self.app_datos_selfie = 'manual'
	
	# Datos domicilio
	@api.one
	def button_editar_datos_domicilio(self):
		self.app_portal_state = 'datos_domicilio'

	@api.one
	def button_confirmar_datos_domicilio(self):
		self.app_datos_domicilio = 'manual'
		self.app_portal_state = 'datos_validaciones'

	@api.multi
	def button_modificar_domicilio(self):
		self.app_datos_domicilio = 'rechazado'
		self.app_domicilio_documento = False

	@api.onchange('app_portal_provincia')
	def _onchange_app_portal_provincia(self):
		self.app_provincia = self.app_portal_provincia.name
	
	# Datos ingreso
	@api.one
	def button_editar_datos_ingreso(self):
		self.app_portal_state = 'datos_ingreso'

	@api.one
	def button_confirmar_datos_ingreso(self):
		self.app_datos_ingreso = True
		self.app_portal_state = 'datos_validaciones'

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
		self.app_datos_cbu = 'manual'
		self.app_portal_state = 'datos_validaciones'
	
	@api.multi
	def button_modificar_cbu(self):
		self.app_datos_cbu = 'rechazado'
		self.app_cbu_documento = False

	# Datos numero celular
	@api.one
	def button_editar_datos_numero_celular(self):
		self.app_portal_state = 'datos_numero_celular'
	
	@api.one
	def button_confirmar_datos_numero_celular(self):
		if not self.app_numero_celular_validado:
			if self.app_codigo_introducido_usuario and self.app_codigo_introducido_usuario == self.app_codigo:
				self.app_numero_celular_validado = True
				self.mobile = self.app_numero_celular
				# self.app_codigo = None
			else:
				raise UserError("El codigo no coincide.")
		self.app_portal_state = 'datos_validaciones'

	@api.one
	def button_modificar_celular(self):
		self.app_numero_celular_validado = False

	# @api.onchange('mobile')
	# def _onchange_validar_celular_cambiar_movil(self):
	# 	self.app_numero_celular_validado = False

	@api.multi
	def button_solicitar_codigo_portal(self):
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
	
	@api.one
	def wizard_datos_personales(self):
		self.app_portal_state = 'datos_personales'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_personales_form', False)
		# return {
		# 	'name': 'Datos personales',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	@api.one
	def wizard_datos_dni_selfie_upload(self):
		self.app_portal_state = 'datos_dni_selfie'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_dni_selfie_upload_form', False)
		# return {
		# 	'name': 'Validacion identidad',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	# @api.multi
	# def wizard_datos_dni_selfie(self):
	# 	if self.app_datos_dni_frontal == 'rechazado':
	# 		return self.wizard_datos_dni_frontal()
	# 	if self.app_datos_dni_posterior == 'rechazado':
	# 		return self.wizard_datos_dni_posterior()
	# 	if self.app_datos_selfie == 'rechazado':
	# 		return self.wizard_datos_selfie()

	# @api.multi
	# def wizard_datos_dni_frontal(self):
	# 	self.ensure_one()
	# 	view_id = self.env.ref('financiera_app.datos_dni_frontal_form', False)
	# 	return {
	# 		'name': 'Datos DNI frontal',
	# 		'type': 'ir.actions.act_window',
	# 		'view_type': 'form',
	# 		'view_mode': 'form',
	# 		'res_model': 'res.partner',
	# 		'res_id': self.id,
	# 		'views': [(view_id.id, 'form')],
	# 		'view_id': view_id.id,
	# 		'target': 'new',
	# 	}
	
	# @api.multi
	# def wizard_datos_dni_posterior(self):
	# 	self.ensure_one()
	# 	view_id = self.env.ref('financiera_app.datos_dni_posterior_form', False)
	# 	return {
	# 		'name': 'Datos DNI dorso',
	# 		'type': 'ir.actions.act_window',
	# 		'view_type': 'form',
	# 		'view_mode': 'form',
	# 		'res_model': 'res.partner',
	# 		'res_id': self.id,
	# 		'views': [(view_id.id, 'form')],
	# 		'view_id': view_id.id,
	# 		'target': 'new',
	# 	}
	
	# @api.multi
	# def wizard_datos_selfie(self):
	# 	self.ensure_one()
	# 	view_id = self.env.ref('financiera_app.datos_selfie_form', False)
	# 	return {
	# 		'name': 'Datos selfie',
	# 		'type': 'ir.actions.act_window',
	# 		'view_type': 'form',
	# 		'view_mode': 'form',
	# 		'res_model': 'res.partner',
	# 		'res_id': self.id,
	# 		'views': [(view_id.id, 'form')],
	# 		'view_id': view_id.id,
	# 		'target': 'new',
	# 	}

	@api.multi
	def wizard_datos_domicilio(self):
		self.app_portal_state = 'datos_domicilio'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_domicilio_form', False)
		# return {
		# 	'name': 'Datos domicilio',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	@api.multi
	def wizard_datos_ingreso(self):
		self.app_portal_state = 'datos_ingreso'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_ingreso_form', False)
		# return {
		# 	'name': 'Datos ingreso',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	@api.multi
	def wizard_datos_vivienda_transporte(self):
		self.app_portal_state = 'datos_vivienda_transporte'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_vivienda_transporte_form', False)
		# return {
		# 	'name': 'Datos de vivienda y transporte',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	@api.multi
	def wizard_datos_cbu(self):
		self.app_portal_state = 'datos_cbu'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_cbu_form', False)
		# return {
		# 	'name': 'Datos de CBU y medios de pago',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }
	
	@api.multi
	def wizard_datos_celular_validado(self):
		self.app_codigo_introducido_usuario = False
		self.app_portal_state = 'datos_numero_celular'
		# self.ensure_one()
		# view_id = self.env.ref('financiera_app.datos_celular_validado_form', False)
		# return {
		# 	'name': 'Validar celular',
		# 	'type': 'ir.actions.act_window',
		# 	'view_type': 'form',
		# 	'view_mode': 'form',
		# 	'res_model': 'res.partner',
		# 	'res_id': self.id,
		# 	'views': [(view_id.id, 'form')],
		# 	'view_id': view_id.id,
		# 	'target': 'new',
		# }

	@api.multi
	def wizard_datos_celular_validado_manual(self):
		self.ensure_one()
		self.app_codigo_introducido_usuario = False
		view_id = self.env.ref('financiera_app.datos_celular_validado_form', False)
		return {
			'name': 'Validar celular',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'new',
		}

	@api.multi
	def do_nothing(self):
		return {'type': 'ir.actions.do_nothing'}

	# Docuementada en la API - Para simulacion real de prestamo
	def obtener_datos_simulador(self):
		ret = []
		cr = self.env.cr
		uid = self.env.uid
		app_id = self.company_id.app_id
		planes_obj = self.pool.get('financiera.prestamo.plan')
		planes_ids = planes_obj.search(cr, uid, [
			('state', '=', 'confirmado'),
			('es_refinanciacion', '=', False),
			# ('id', 'in', planes_disponibles_ids),
			# '|', ('prestamo_tipo_ids', '=', False), ('prestamo_tipo_ids.id', '=', self.prestamo_tipo_id.id),
			'|', ('partner_tipo_ids', '=', False), ('partner_tipo_ids.id', '=', self.partner_tipo_id.id),
			'|', ('recibo_de_sueldo', '=', False), ('recibo_de_sueldo', '=', self.recibo_de_sueldo),
			('company_id', '=', self.company_id.id)], order="cuotas asc")
		seguros_obj = self.pool.get('financiera.prestamo.seguro')
		seguros_ids = seguros_obj.search(cr, uid, [
			('state', '=', 'confirmado'),
			('company_id', '=', self.company_id.id)])
		planes_disponibles_ids = [g.id for g in app_id.planes_disponibles_ids]
		for _id in planes_ids:
			if len(planes_disponibles_ids) == 0 or _id in planes_disponibles_ids:
				plan_id = self.env['financiera.prestamo.plan'].browse(_id)
				if plan_id.seguro_calcular:
					for i in seguros_ids:
						seguro_id = self.env['financiera.prestamo.seguro'].browse(i)
						# Compute indice
						indice = self.simular_indice_plan(plan_id, seguro_id)
						ret.append({
							'plan_id': plan_id.id,
							'nombre': plan_id.name,
							'cuotas': plan_id.cuotas,
							'indice': indice,
							'seguro_id': seguro_id.id,
						})
				else:
						indice = self.simular_indice_plan(plan_id, False)
						ret.append({
							'plan_id': plan_id.id,
							'nombre': plan_id.name,
							'cuotas': plan_id.cuotas,
							'indice': indice,
							'seguro_id': False,
						})
		return ret
	
	@api.multi
	def button_wizard_set_password(self):
		return self.wizard_set_password(False)

	@api.multi
	def wizard_set_password(self, password=None):
		params = {
			'partner_id': self.id,
			'nuevo_password': password,
		}
		view_id = self.env['res.partner.set.password.wizard']
		new = view_id.create(params)
		return {
			'type': 'ir.actions.act_window',
			'name': 'Nueva contraseña',
			'res_model': 'res.partner.set.password.wizard',
			'view_type': 'form',
			'view_mode': 'form',
			'res_id': new.id,
			'view_id': self.env.ref('financiera_app.set_password', False).id,
			'target': 'new',
		}

	@api.one
	def button_send_mail_password_generate(self):
		nuevo_password = self.password_generate()
		self.send_mail_password_generate(nuevo_password)

	@api.one
	def alerta_actualizar(self):
		self.alerta_ultima_actualizacion = datetime.now()
		self.compute_alerta_ip_multiple_registros()
		self.compute_alerta_celular_multiple_partner()
		self.compute_alerta_celular_como_contacto()
		self.compute_alerta_domicilio_similar()
		self.compute_alerta_registrado_financieras()
		self.compute_alerta_prestamos_activos_financieras()
		self.compute_alerta_cuota_vencidas_financieras()
		self.compute_alerta_compromiso_mensual_financieras()
		self.compute_alerta_ip_no_confiable_financieras()

	@api.one
	def compute_alerta_ip_multiple_registros(self):
		if self.app_ip_registro:
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('app_ip_registro', '=', self.app_ip_registro),
				('main_id_number', '!=', False),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				'|', ('active', '=', True), ('active', '=', False),
				('company_id', '=', self.company_id.id)])
			self.alerta_ip_multiple_registros = len(partner_ids)
			self.alerta_ip_multiple_registros_ids = [(6, 0, partner_ids)]
	
	@api.one
	def button_app_ip_registro_no_confiable(self):
		self.app_ip_registro_no_confiable = True
		self.compute_alerta_ip_multiple_registros()
		for partner_id in self.alerta_ip_multiple_registros_ids:
			partner_id.app_ip_registro_no_confiable = True

	@api.one
	def button_app_ip_registro_confiable(self):
		self.app_ip_registro_no_confiable = False
		self.compute_alerta_ip_multiple_registros()
		for partner_id in self.alerta_ip_multiple_registros_ids:
			partner_id.app_ip_registro_no_confiable = False


	@api.one
	def button_app_estado_bloqueado(self):
		self.app_estado_bloqueado = True
		self.app_estado_portal = "Bloqueado por ip no confiable."

	@api.one
	def button_app_estado_no_bloqueado(self):
		self.app_estado_bloqueado = False
		self.app_estado_portal = ""

	@api.one
	def compute_alerta_celular_multiple_partner(self):
		if self.mobile and self.dni:
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('mobile', '=', self.mobile),
				('id', '!=', self.id),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				('company_id', '=', self.company_id.id)])
			self.alerta_celular_multiple_partner = len(partner_ids)
			self.alerta_celular_multiple_partner_ids = [(6, 0, partner_ids)]
	
	@api.one
	def compute_alerta_celular_como_contacto(self):
		if self.mobile and self.dni:
			contacto_obj = self.pool.get('res.partner.contacto')
			contacto_ids = contacto_obj.search(self.env.cr, self.env.uid, [
				'|', ('telefono', '=', self.mobile), ('movil', '=', self.mobile),
				('company_id', '=', self.company_id.id)])
			self.alerta_celular_como_contacto = len(contacto_ids)
			self.alerta_celular_como_contacto_ids = [(6, 0, contacto_ids)]

	@api.one
	def compute_alerta_domicilio_similar(self):
		if self.street and self.state_id and self.zip:
			street = self.street.split(" ")[0]
			partner_obj = self.pool.get('res.partner')
			partner_ids = partner_obj.search(self.env.cr, self.env.uid, [
				('street', '=ilike', street+'%'),
				('state_id', '=', self.state_id.id),
				('zip', '=', self.zip),
				('id', '!=', self.id),
				('main_id_number', '!=', self.main_id_number),
				('main_id_number', '!=', self.dni),
				('company_id', '=', self.company_id.id)])
			self.alerta_domicilio_similar = len(partner_ids)
			self.alerta_domicilio_similar_ids = [(6, 0, partner_ids)]

	@api.one
	@api.depends('prestamo_ids.state')
	def _compute_alerta_prestamos_activos(self):
		if self.prestamo_ids:
			prestamo_obj = self.pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'acreditado'),
				('company_id', '=', self.company_id.id)])
			self.alerta_prestamos_activos = len(prestamo_ids)

	@api.one
	@api.depends('prestamo_ids.state')
	def _compute_alerta_prestamos_cobrados(self):
		if self.prestamo_ids:
			prestamo_obj = self.pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'pagado'),
				('company_id', '=', self.company_id.id)])
			self.alerta_prestamos_cobrados = len(prestamo_ids)

	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_activas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_activas = len(cuota_ids)

	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_cobradas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				'|', ('state', '=', 'cobrada'), ('state', '=', 'precancelada'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_cobradas = len(cuota_ids)

	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_normal(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'normal'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_normal = len(cuota_ids)


	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_preventivas(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'preventiva'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_preventivas = len(cuota_ids)
	
	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_mora_temprana(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraTemprana'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_temprana = len(cuota_ids)

	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_mora_media(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraMedia'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_media = len(cuota_ids)
	
	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_mora_tardia(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'moraTardia'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_tardia = len(cuota_ids)

	@api.depends('cuota_ids.state_mora')
	def _compute_alerta_cuotas_mora_incobrable(self):
		if self.cuota_ids:
			cuota_obj = self.pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.env.cr, self.env.uid, [
				('partner_id', '=', self.id),
				('state', '=', 'activa'),
				('state_mora', '=', 'incobrable'),
				('company_id', '=', self.company_id.id)])
			self.alerta_cuotas_incobrable = len(cuota_ids)

	# Alertas compartidas

	@api.one
	def button_alerta_ver_y_compartir(self):
		self.alerta_ver_y_compartir = True

	@api.one
	def compute_alerta_registrado_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.id)])
		if len(company_ids) > 0:
			prestamo_obj = self.sudo().pool.get('res.partner')
			prestamo_ids = prestamo_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('main_id_number', '=', self.main_id_number), ('main_id_number', '=', self.dni),
				('company_id', 'in', company_ids)])
			self.alerta_registrado_financieras = len(prestamo_ids)

	@api.one
	def compute_alerta_prestamos_activos_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			prestamo_obj = self.sudo().pool.get('financiera.prestamo')
			prestamo_ids = prestamo_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('partner_id.main_id_number', '=', self.main_id_number), ('partner_id.main_id_number', '=', self.dni),
				('state', '=', 'acreditado'),
				('company_id', 'in', company_ids)])
			self.alerta_prestamos_activos_financieras = len(prestamo_ids)

	@api.one
	def compute_alerta_cuota_vencidas_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			cuota_obj = self.sudo().pool.get('financiera.prestamo.cuota')
			cuota_ids = cuota_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('partner_id.main_id_number', '=', self.main_id_number), ('partner_id.main_id_number', '=', self.dni),
				('state', 'in', ['activa','judicial','incobrable']),
				('state_mora', 'in', ['moraTemprana','moraMedia','moraTardia','incobrable']),
				('company_id', 'in', company_ids)])
			self.alerta_cuotas_vencidas_financieras = len(cuota_ids)

	@api.one
	def compute_alerta_compromiso_mensual_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			partner_obj = self.sudo().pool.get('res.partner')
			partner_ids = partner_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				'|', ('main_id_number', '=', self.main_id_number), ('main_id_number', '=', self.dni),
				('cuota_ids.state', '=', 'activa'),
				('company_id', 'in', company_ids)])
			alerta_compromiso_mensual_financieras = 0
			for _id in partner_ids:
				partner_id = self.sudo().env['res.partner'].browse(_id)
				if partner_id.saldo > 0 and partner_id.capacidad_pago_mensual > 0:
					alerta_compromiso_mensual_financieras += partner_id.capacidad_pago_mensual-partner_id.capacidad_pago_mensual_disponible
			self.alerta_compromiso_mensual_financieras = alerta_compromiso_mensual_financieras
	
	@api.one
	def compute_alerta_ip_no_confiable_financieras(self):
		company_obj = self.sudo().pool.get('res.company')
		company_ids = company_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
			('app_id.app_ver_y_compartir_riesgo_cliente', '=', True),
			('id', '!=', self.company_id.id)])
		if len(company_ids) > 0:
			partner_obj = self.sudo().pool.get('res.partner')
			partner_ids = partner_obj.search(self.sudo().env.cr, self.sudo().env.uid, [
				('app_ip_registro', '=', self.app_ip_registro),
				('app_ip_registro_no_confiable', '=', True),
				('company_id', 'in', company_ids)])
			company_alerta_ip_no_confiable = []
			for _id in partner_ids:
				partner_id = self.sudo().env['res.partner'].browse(_id)
				if partner_id.company_id.id not in company_alerta_ip_no_confiable:
					company_alerta_ip_no_confiable.append(partner_id.company_id.id)
			self.alerta_ip_no_confiable_financieras = len(company_alerta_ip_no_confiable)

	@api.model
	def _actualizar_alerta_partners_prestamo_y_cuotas_tmp(self):
		cr = self.env.cr
		uid = self.env.uid
		partner_obj = self.pool.get('res.partner')
		partner_ids = partner_obj.search(cr, uid, [])
		_logger.info('Init Actualizar alerta partners sobre prestamos y cuotas')
		count = 0
		for _id in partner_ids:
			partner_id = partner_obj.browse(cr, uid, _id)
			partner_id._compute_alerta_prestamos_activos()
			partner_id._compute_alerta_prestamos_cobrados()
			partner_id._compute_alerta_cuotas_activas()
			partner_id._compute_alerta_cuotas_cobradas()
			partner_id._compute_alerta_cuotas_normal()
			partner_id._compute_alerta_cuotas_preventivas()
			partner_id._compute_alerta_cuotas_mora_temprana()
			partner_id._compute_alerta_cuotas_mora_media()
			partner_id._compute_alerta_cuotas_mora_tardia()
			partner_id._compute_alerta_cuotas_mora_incobrable()
			count += 1
		_logger.info('Finish Actualizar alerta partners: %s partners actualizadas sobre prestamos y cuotas', count)

	@api.model
	def _actualizar_alerta_partners(self):
		cr = self.env.cr
		uid = self.env.uid
		partner_obj = self.pool.get('res.partner')
		partner_ids = partner_obj.search(cr, uid, [])
		_logger.info('Init Actualizar alerta partners')
		count = 0
		for _id in partner_ids:
			partner_id = partner_obj.browse(cr, uid, _id)
			partner_id.alerta_actualizar()
			count += 1
		_logger.info('Finish Actualizar alerta partners: %s partners actualizadas', count)