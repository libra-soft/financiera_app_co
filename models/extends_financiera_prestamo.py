# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
import base64
import re
class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	state_portal = fields.Selection([
		('requisitos', 'Requisitos'),
		('simulacion', 'Simulacion'),
		('condiciones', 'Condiciones'),
		('aceptacion', 'Aceptacion'),
		('confirmado', 'Confirmado'),
	], 'Estado en portal', default='requisitos')
	respuesta_email_codigo_prestamo = fields.Boolean("Codigo correcto en la respuesta por mail")
	respuesta_email_mensaje_original = fields.Boolean("Mensaje original en la respuesta por mail")
	partner_main_id_number = fields.Char(related='partner_id.main_id_number', realdonly=True)
	partner_email = fields.Char(related='partner_id.email', readonly=True)
	app_calle = fields.Char("Calle")
	app_altura = fields.Char("Altura")
	app_piso = fields.Char("Piso")
	app_departamento = fields.Char("Departamento")
	app_cp = fields.Char("CP")
	app_ciudad = fields.Char("Ciudad")
	app_provincia = fields.Char("Provincia")
	app_banco_haberes_numero_entidad = fields.Char("Numero entidad bancaria")
	app_banco_haberes = fields.Char('Banco', compute='_compute_app_banco_haberes')
	app_dia_cobro = fields.Integer("Dia de cobro")

	app_cbu = fields.Char('CBU para depositar el capital')
	app_fecha_primer_vencimiento = fields.Char("Dia vencimiento")
	# Servicio
	app_servicio = fields.Binary("Servicio")
	app_servicio_completo = fields.Boolean("Servicio completo", compute='_compute_app_servicio_completo')
	app_servicio_download = fields.Binary("", related="app_servicio")
	app_servicio_download_name = fields.Char("", default="servicio")
	# Recibo de sueldo
	app_recibo_sueldo = fields.Binary("Recibo de sueldo")
	app_recibo_sueldo_completo = fields.Boolean("Servicio completo", compute='_compute_app_recibo_sueldo_completo')
	app_recibo_sueldo_download = fields.Binary("", related="app_recibo_sueldo")
	app_recibo_sueldo_download_name = fields.Char("", default="recibo")
	# Firma solicitud
	app_firma = fields.Binary("Firma")
	app_firma_preview = fields.Binary(related="app_firma")
	app_firma_completo = fields.Boolean("Firma completo", compute='_compute_app_firma_completo')
	app_aclaracion = fields.Char("Aclaracion")
	app_dni = fields.Char("DNI")
	# Terminos y condiciones
	app_tyc = fields.Binary("Terminos y condiciones", compute='_compute_app_tyc')
	app_tyc_download_name = fields.Char("", default="TyC.pdf")

	# alertas
	app_estado_bloqueado = fields.Boolean(related='partner_id.app_estado_bloqueado')
	app_ip_registro_no_confiable = fields.Boolean(related='partner_id.app_ip_registro_no_confiable')
	alerta_show = fields.Boolean('Ver alertas', default=True)
	alerta_ultima_actualizacion = fields.Datetime(related='partner_id.alerta_ultima_actualizacion', readonly=True)
	alerta_ip_multiple_registros = fields.Integer(related='partner_id.alerta_ip_multiple_registros', readonly=True)
	alerta_celular_multiple_partner = fields.Integer(related='partner_id.alerta_celular_multiple_partner', readonly=True)
	alerta_celular_como_contacto = fields.Integer(related='partner_id.alerta_celular_como_contacto', readonly=True)
	alerta_domicilio_similar = fields.Integer(related='partner_id.alerta_domicilio_similar', readonly=True)

	alerta_prestamos_activos = fields.Integer(related='partner_id.alerta_prestamos_activos', readonly=True)
	alerta_prestamos_cobrados = fields.Integer(related='partner_id.alerta_prestamos_cobrados', readonly=True)
	
	alerta_cuotas_activas = fields.Integer(related='partner_id.alerta_cuotas_activas', readonly=True)
	alerta_cuotas_cobradas = fields.Integer(related='partner_id.alerta_cuotas_cobradas', readonly=True)
	alerta_cuotas_normal = fields.Integer(related='partner_id.alerta_cuotas_normal', readonly=True)
	alerta_cuotas_preventivas = fields.Integer(related='partner_id.alerta_cuotas_preventivas', readonly=True)
	alerta_cuotas_temprana = fields.Integer(related='partner_id.alerta_cuotas_temprana', readonly=True)
	alerta_cuotas_media = fields.Integer(related='partner_id.alerta_cuotas_media', readonly=True)
	alerta_cuotas_tardia = fields.Integer(related='partner_id.alerta_cuotas_tardia', readonly=True)
	alerta_cuotas_incobrable = fields.Integer(related='partner_id.alerta_cuotas_incobrable', readonly=True)
	# Datos compartidos entre financieras
	alerta_ver_y_compartir = fields.Boolean('Ver y compartir', related='company_id.app_id.app_ver_y_compartir_riesgo_cliente', readonly=True)
	alerta_registrado_financieras = fields.Integer(related='partner_id.alerta_registrado_financieras', readonly=True)
	alerta_prestamos_activos_financieras = fields.Integer(related='partner_id.alerta_prestamos_activos_financieras', readonly=True)
	alerta_cuotas_vencidas_financieras = fields.Integer(related='partner_id.alerta_cuotas_vencidas_financieras', readonly=True)
	alerta_compromiso_mensual_financieras = fields.Float(related='partner_id.alerta_compromiso_mensual_financieras', readonly=True)
	alerta_ip_no_confiable_financieras = fields.Integer(related='partner_id.alerta_ip_no_confiable_financieras', readonly=True)

	# Requerimientos automaticos
	app_requerimientos_completos_porcentaje = fields.Float("Cumplimiento de requerimientos", store=True, compute='change_app_requerimientos_porcentaje')
	app_requerimientos_cumplidos = fields.Char("Requerimientos cumplidos", store=True, compute='change_app_requerimientos_porcentaje')
	app_requerimientos_pendientes = fields.Char("Requerimientos pendientes", store=True, compute='change_app_requerimientos_porcentaje')

	# Docuementada en la API - Para conocer los ids de los planes
	def obtener_planes_prestamo(self):
		ret = []
		cr = self.env.cr
		uid = self.env.uid
		app_id = self.company_id.app_id
		app_id.planes_disponibles_ids
		plan_evaluacion_ids = [g.id for g in self.plan_ids]
		seguros_obj = self.pool.get('financiera.prestamo.seguro')
		seguros_ids = seguros_obj.search(cr, uid, [
			('state', '=', 'confirmado'),
			('company_id', '=', self.company_id.id)])
		plan_online_ids = [g.id for g in app_id.planes_disponibles_ids]
		# Comprobamos si hay al menos un plan cargado sino consideramos que
		# todos los planes deben estar disponible
		for _id in plan_evaluacion_ids:
			plan_evaluacion_id = self.env['financiera.prestamo.evaluacion.plan'].browse(_id)
			if len(plan_online_ids) == 0 or plan_evaluacion_id.plan_id.id in plan_online_ids:
				if plan_evaluacion_id.plan_id.seguro_calcular:
					for i in seguros_ids:
						seguro_id = self.env['financiera.prestamo.seguro'].browse(i)
						# Compute indice
						indice = self.partner_id.simular_indice_plan(plan_evaluacion_id.plan_id, seguro_id)
						ret.append({
							'plan_id': plan_evaluacion_id.id,
							'nombre': plan_evaluacion_id.nombre,
							'cuotas': plan_evaluacion_id.cuotas,
							'indice': indice,
							'seguro_id': seguro_id.id,
						})
				else:
						indice = self.partner_id.simular_indice_plan(plan_evaluacion_id.plan_id, False)
						ret.append({
							'plan_id': plan_evaluacion_id.id,
							'nombre': plan_evaluacion_id.nombre,
							'cuotas': plan_evaluacion_id.cuotas,
							'indice': indice,
							'seguro_id': False,
						})
		return ret

	@api.model
	def _cron_prestamos_cbu_to_banco(self):
		prestamo_obj = self.pool.get('financiera.prestamo')
		prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
			('state', 'in', ['autorizado','acreditacion_pendiente','acreditado']),
			('app_banco_haberes_numero_entidad','=', False),
			('app_cbu', '!=', False)
			])
		for _id in prestamo_ids:
			prestamo_id = prestamo_obj.browse(self.env.cr, self.env.uid, _id)
			if prestamo_id.app_cbu and len(prestamo_id.app_cbu) == 22:
				prestamo_id.app_banco_haberes_numero_entidad = prestamo_id.app_cbu[0:3]

	@api.one
	def _compute_app_banco_haberes(self):
		if self.app_banco_haberes_numero_entidad:
			bank_obj = self.pool.get('res.bank')
			bank_ids = bank_obj.search(self.env.cr, self.env.uid, [
				('code', '=', self.app_banco_haberes_numero_entidad)])
			if len(bank_ids) > 0:
				self.app_banco_haberes = bank_obj.browse(self.env.cr, self.env.uid, bank_ids[0]).name

	@api.one
	def _compute_app_servicio_completo(self):
		self.app_servicio_completo = False
		if self.app_servicio:
			self.app_servicio_completo = True

	@api.one
	def _compute_app_recibo_sueldo_completo(self):
		self.app_recibo_sueldo_completo = False
		if self.app_recibo_sueldo:
			self.app_recibo_sueldo_completo = True

	@api.one
	def _compute_app_firma_completo(self):
		self.app_firma_completo = False
		if self.app_firma:
			self.app_firma_completo = True

	@api.one
	def _compute_app_tyc(self):
		report_name = self.company_id.configuracion_id.email_tc_report_name
		if report_name:
			pdf = self.pool['report'].get_pdf(self._cr, self._uid, [self.id], report_name, context=None)
			self.app_tyc = base64.encodestring(pdf)

	# Alertas
	@api.one
	def button_alerta_show(self):
		self.alerta_show = True

	@api.one
	def button_alerta_hide(self):
		self.alerta_show = False

	@api.one
	def alerta_actualizar(self):
		self.partner_id.alerta_actualizar()

	@api.one
	def button_app_ip_registro_no_confiable(self):
		self.partner_id.button_app_ip_registro_no_confiable()

	@api.one
	def button_app_ip_registro_confiable(self):
		self.partner_id.button_app_ip_registro_confiable()

	@api.one
	def button_app_estado_bloqueado(self):
		self.partner_id.button_app_estado_bloqueado()

	@api.one
	def button_app_estado_no_bloqueado(self):
		self.partner_id.button_app_estado_no_bloqueado()

	@api.model
	def _cron_actualizar_requerimientos_prestamos(self):
		company_obj = self.pool.get('res.company')
		comapny_ids = company_obj.search(self.env.cr, self.env.uid, [])
		for _id in comapny_ids:
			company_id = company_obj.browse(self.env.cr, self.env.uid, _id)
			if len(company_id.app_id) > 0:
				prestamo_obj = self.pool.get('financiera.prestamo')
				prestamo_ids = prestamo_obj.search(self.env.cr, self.env.uid, [
					('company_id','=', company_id.id),
				])
				for _id in prestamo_ids:
					prestamo_id = prestamo_obj.browse(self.env.cr, self.env.uid, _id)
					prestamo_id.change_app_requerimientos_porcentaje()

	@api.one
	@api.depends('app_calle','app_cbu','partner_id.empresa_nombre','partner_id.empresa_telefono',
	'partner_id.contacto_ids','mobbex_suscripcion_suscriptor_confirm','partner_id.app_dni_frontal',
	'partner_id.app_dni_posterior','partner_id.app_selfie','app_recibo_sueldo','app_servicio','app_firma')
	def change_app_requerimientos_porcentaje(self):
		app_id = self.company_id.app_id
		total_requeridos = 0
		total_completados = 0
		app_requerimientos_cumplidos = []
		app_requerimientos_pendientes = []
		if app_id.app_requiere_direccion:
			total_requeridos += 1.0
			if self.app_calle:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Direccion')
			else:
				app_requerimientos_pendientes.append('Direccion')
		if app_id.app_requiere_cbu:
			total_requeridos += 1.0
			if self.app_cbu:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('CBU')
			else:
				app_requerimientos_pendientes.append('CBU')
		if app_id.app_requiere_trabajo_actual:
			total_requeridos += 1.0
			if self.partner_id.empresa_nombre and self.partner_id.empresa_telefono:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Trabajo actual')
			else:
				app_requerimientos_pendientes.append('Trabajo actual')
		if app_id.app_requiere_contactos:
			total_requeridos += 1.0
			if self.partner_id.contacto_ids and len(self.partner_id.contacto_ids) >= app_id.app_requiere_contactos:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Contactos')
			else:
				app_requerimientos_pendientes.append('Contactos')
		if app_id.app_requeire_tarjeta_debito:
			total_requeridos += 1.0
			if self.mobbex_suscripcion_suscriptor_confirm:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Tarjeta debito')
			else:
				app_requerimientos_pendientes.append('Tarjeta debito')
		if app_id.app_requiere_dni_frontal:
			total_requeridos += 1.0
			if self.partner_id.app_dni_frontal:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('DNI frontal')
			else:
				app_requerimientos_pendientes.append('DNI frontal')
		if app_id.app_requiere_dni_dorso:
			total_requeridos += 1.0
			if self.partner_id.app_dni_posterior:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('DNI dorso')
			else:
				app_requerimientos_pendientes.append('DNI dorso')
		if app_id.app_requiere_selfie:
			total_requeridos += 1.0
			if self.partner_id.app_selfie:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Selfie')
			else:
				app_requerimientos_pendientes.append('Selfie')
		if app_id.app_requiere_recibo_sueldo:
			total_requeridos += 1
			if self.app_recibo_sueldo:
				total_completados += 1
				app_requerimientos_cumplidos.append('Recibo de sueldo')
			else:
				app_requerimientos_pendientes.append('Recibo de sueldo')
		if app_id.app_requiere_servicio:
			total_requeridos += 1.0
			if self.app_servicio:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Servicio')
			else:
				app_requerimientos_pendientes.append('Servicio')
		if app_id.app_requiere_firma:
			total_requeridos += 1.0
			if self.app_firma:
				total_completados += 1.0
				app_requerimientos_cumplidos.append('Firma TyC')
			else:
				app_requerimientos_pendientes.append('Firma TyC')
		if total_requeridos > 0:
			self.app_requerimientos_completos_porcentaje = (total_completados / total_requeridos) * 100
		else:
			self.app_requerimientos_completos_porcentaje = 0
		# Lista de cumplidos
		font_open_cumplidos = '<font style="border-radius:20px;background: #59C446;padding: 5px;color: white;float:left;">'
		if app_requerimientos_cumplidos:
			app_requerimientos_cumplidos = ('</font>'+font_open_cumplidos).join(app_requerimientos_cumplidos)
			app_requerimientos_cumplidos = font_open_cumplidos + app_requerimientos_cumplidos + '</font>'
			self.app_requerimientos_cumplidos = app_requerimientos_cumplidos
		else:
			self.app_requerimientos_cumplidos = font_open_cumplidos + '</font>'
		# Lista de pendientes
		if app_requerimientos_pendientes:
			font_open_pendientes = '<font style="border-radius:20px;background: #BA2E2E;padding: 5px;color: white;float:left;">'
			app_requerimientos_pendientes = ('</font>'+font_open_pendientes).join(app_requerimientos_pendientes)
			app_requerimientos_pendientes = font_open_pendientes + app_requerimientos_pendientes + '</font>'
			self.app_requerimientos_pendientes = app_requerimientos_pendientes
		else:
			self.app_requerimientos_pendientes = False

	@api.multi
	def ver_prestamo(self):
		view_id = self.env.ref('financiera_prestamos.financiera_prestamo_form').id
		context = self._context.copy()
		return {
					'name': 'Prestamos',
					'view_type': 'form',
					'view_mode': 'form',
					'views' : [(view_id,'form')],
					'res_model': 'financiera.prestamo',
					'view_id': view_id,
					'type': 'ir.actions.act_window',
					'res_id': self.id,
					'target': 'current',
					'context': context,
			}

# class ExtendsFinancieraCuotaPrestamo(models.Model):
# 	_name = 'financiera.prestamo.cuota'
# 	_inherit = 'financiera.prestamo.cuota'

# 	@api.one
# 	def button_pagos_360_pagar_online(self):
# 		return {
# 			"type": "ir.actions.act_window", 
# 			"url": self.pagos_360_checkout_url, 
# 			"target": "new"
# 		}

# class ExtendsFinancieraPrestamoEvaluacionPlan(models.Model):
# 	_name = 'financiera.prestamo.evaluacion.plan'
# 	_inherit = 'financiera.prestamo.evaluacion.plan'

# 	@api.multi
# 	def button_simular_plan(self):
# 		self.sudo().seleccionar_plan()
# 		self.sudo().prestamo_id.state_portal = 'simulacion'
# 		if len(self.sudo().prestamo_id.plan_ids) > 0:
# 			monto_maximo_aproximado = self.sudo().prestamo_id.plan_ids[0].monto_maximo_aproximado
# 			monto_maximo = '{:0,.2f}'.format(monto_maximo_aproximado).replace('.', '#').replace(',', '.').replace('#', ',')
# 			self.sudo().prestamo_id.preaprobado_portal = "TENES $"+monto_maximo+ " PRE APROBADO"
# 		else:
# 			self.sudo().prestamo_id.preaprobado_portal = ""
