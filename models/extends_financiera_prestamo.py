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
	cuotas_portal = fields.Integer("Cuotas", related='plan_id.cuotas')
	primer_cuota_portal = fields.Float('Primera cuota', digits=(16,2), compute='_compute_primera_cuota_portal')
	ultima_cuota_portal = fields.Float('Ultima cuota', digits=(16,2), compute='_compute_ultima_cuota_portal')
	preaprobado_portal = fields.Char(" ", default="")
	aceptacion_detalle_cuotas_portal = fields.Boolean("Declaro haber leido y aceptado el presente detalle de cuotas.")
	aceptacion_tc_portal = fields.Boolean("Declaro haber leido y aceptado los presentes terminos y condiciones.")
	respuesta_email_codigo_prestamo = fields.Boolean("Codigo correcto en la respuesta por mail")
	respuesta_email_mensaje_original = fields.Boolean("Mensaje original en la respuesta por mail")
	leyenda_tc = fields.Char(" ", default=" ")
	app_cbu = fields.Char('CBU para depositar el capital')
	# Requeimiento de la tarjeta de debito
	requiere_tarjeta_debito = fields.Boolean('Requiere tarjeta de debito', readonly=True, related='company_id.app_id.requiere_tarjeta_debito')
	requiere_tarjeta_debito_pass = fields.Boolean('Supera el requerimiento de tarjeta de debito')
	app_tarjeta_debito_digitos_fin = fields.Char("Ultimos 4 digitos", related='partner_id.app_tarjeta_debito_digitos_fin')
	app_tarjeta_debito_vencimiento_month = fields.Selection(related='partner_id.app_tarjeta_debito_vencimiento_month')
	app_tarjeta_debito_vencimiento_year = fields.Selection(related='partner_id.app_tarjeta_debito_vencimiento_year')
	
	@api.model
	def default_get(self, fields):
		rec = super(ExtendsFinancieraPrestamo, self).default_get(fields)
		# configuracion_id = self.env.user.company_id.configuracion_id
		context = dict(self._context or {})
		current_uid = context.get('uid')
		current_user = self.env['res.users'].browse(current_uid)
		app_id = current_user.company_id.app_id
		# sucursal_id = current_user.entidad_login_id
		# partner_id = None
		if current_user.user_has_groups('financiera_prestamos.user_portal'):
			partner_id = current_user.partner_id
			self.pre_requisitos_solicitud_portal(partner_id)
			requiere_tarjeta_debito_pass = not app_id.requiere_tarjeta_debito or (partner_id.app_tarjeta_debito_vencimiento_month != False and partner_id.app_tarjeta_debito_vencimiento_year != False)
			rec.update({
				'partner_id': partner_id.id,
				'origen_id': app_id.portal_origen_id.id,
				'sucursal_id': app_id.portal_sucursal_id.id,
				'responsable_id': app_id.portal_responsable_id.id,
				'app_cbu': partner_id.app_cbu,
				'monto_solicitado': app_id.monto_minimo_solicitud,
				'requiere_tarjeta_debito_pass': requiere_tarjeta_debito_pass,
			})
		return rec

	@api.one
	def button_actualizar_tarjeta_debito_prestamo_portal(self):
		self.requiere_tarjeta_debito_pass = not self.requiere_tarjeta_debito or (self.app_tarjeta_debito_vencimiento_month != False and self.app_tarjeta_debito_vencimiento_year != False)

	def pre_requisitos_solicitud_portal(self, partner_id):
		# Requisitos establecidos en este mismo modulo
		app_id = partner_id.company_id.app_id
		datos_incompletos = "Desde Mi Perfil debe: \n"
		perfil_incompleto = False
		if app_id.requiere_state_validado and not partner_id.state == 'validated':
			datos_incompletos += "* Validar Identidad.\n"
			perfil_incompleto = True
		# Si no requiere validar identidad, vemos si requiere algunos de los parametros
		# que conformar validar identidad
		if not app_id.requiere_state_validado:
			if app_id.requiere_datos_personales == 'completo' and partner_id.app_datos_personales == 'rechazado':
				datos_incompletos += "* Completar datos personales.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_personales == 'validado' and partner_id.app_datos_personales != 'aprobado':
				datos_incompletos += "* Completar datos personales y esperar la aprobacion.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_dni_frontal == 'completo' and partner_id.app_datos_dni_frontal == 'rechazado':
				datos_incompletos += "* Cargar DNI fronal.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_dni_frontal == 'validado' and partner_id.app_datos_dni_frontal != 'aprobado':
				datos_incompletos += "* Cargar DNI fronal y esperar la aprobacion.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_dni_dorso == 'completo' and partner_id.app_datos_dni_posterior == 'rechazado':
				datos_incompletos += "* Cargar DNI dorso.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_dni_dorso == 'validado' and partner_id.app_datos_dni_posterior != 'aprobado':
				datos_incompletos += "* Cargar DNI dorso y esperar la aprobacion.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_selfie == 'completo' and partner_id.app_datos_selfie == 'rechazado':
				datos_incompletos += "* Cargar selfie.\n"
				perfil_incompleto = True
			if app_id.requiere_datos_selfie == 'validado' and partner_id.app_datos_selfie != 'aprobado':
				datos_incompletos += "* Cargar selfie y esperar la aprobacion.\n"
				perfil_incompleto = True

		if app_id.requiere_datos_domicilio == 'completo' and partner_id.app_datos_domicilio == 'rechazado':
			datos_incompletos += "* Completar datos del domicilio.\n"
			perfil_incompleto = True
		if app_id.requiere_datos_domicilio == 'validado' and partner_id.app_datos_domicilio != 'aprobado':
			datos_incompletos += "* Completar datos del domicilio y esperar la aprobacion.\n"
			perfil_incompleto = True
		if app_id.requiere_datos_ingreso and not partner_id.app_datos_ingreso:
			datos_incompletos += "* Completar datos de ingreso.\n"
			perfil_incompleto = True
		if app_id.requiere_datos_vivienda_transporte and not partner_id.app_datos_vivienda_transporte:
			datos_incompletos += "* Completar datos de vivienda y transporte.\n"
			perfil_incompleto = True
		if app_id.requiere_cbu == 'completo' and partner_id.app_datos_cbu == 'rechazado':
			datos_incompletos += "* Completar datos del CBU.\n"
			perfil_incompleto = True
		if app_id.requiere_cbu == 'validado' and partner_id.app_datos_cbu != 'aprobado':
			datos_incompletos += "* Completar datos del CBU y esperar la aprobacion.\n"
			perfil_incompleto = True
		if app_id.requiere_celular_validado and not partner_id.app_numero_celular_validado:
			datos_incompletos += "* Completar numero de celular.\n"
			perfil_incompleto = True
		if perfil_incompleto:
			raise UserError(datos_incompletos)

	@api.one
	def button_regresar(self):
		if self.state_portal == 'simulacion':
			self.state_portal = 'requisitos'
			self.preaprobado_portal = ""
			self.sudo().enviar_a_solicitado()
		if self.state_portal == 'condiciones':
			self.state_portal = 'simulacion'
			self.aceptacion_detalle_cuotas_portal = False
			self.aceptacion_tc_portal = False
		# Solo para debug!!
		if self.state_portal == 'aceptacion':
			self.state_portal = 'condiciones'
			self.aceptacion_detalle_cuotas_portal = False
			self.aceptacion_tc_portal = False

	@api.one
	def button_simular(self):
		# Controlar si requiere tarjeta
		self.button_actualizar_tarjeta_debito_prestamo_portal()
		if not self.requiere_tarjeta_debito_pass:
			raise UserError("Debe completar los datos de la tarjeta de debito para continuar.")
		self.sudo().enviar_a_revision()
		flag_aprobado = False
		for plan_id in self.plan_ids:
			if plan_id.state == 'aprobado':
				flag_aprobado = True
		if not flag_aprobado:
			raise ValidationError("No tenemos nada en este momento para usted. Vuelve a consultar dentro de 30 dias. Estamos calificando tu cuenta.")
		self.sudo().enviar_a_autorizado()
		if len(self.plan_ids) > 0:
			# Preseleccion de plan: El primero con el mayor monto!
			self.sudo().set_monto_solicitado(self.sudo().plan_ids[0].monto_maximo_aproximado)
			monto_maximo = '{:0,.2f}'.format(self.monto_solicitado).replace('.', '#').replace(',', '.').replace('#', ',')
			self.preaprobado_portal = "TENES $"+monto_maximo+ " PRE APROBADO"
			self.sudo().plan_ids[0].seleccionar_plan()
			self.state_portal = 'simulacion'
		else:
			self.preaprobado_portal = ""
	
	@api.one
	def button_condiciones(self):
		if len(self.cuota_ids) == 0:
			raise UserError("Debe seleccionar Monto y Cuotas")
		else:
			self.state_portal = 'condiciones'

	@api.one
	def button_aceptar_condiciones(self):
		if self.aceptacion_detalle_cuotas_portal and self.aceptacion_tc_portal:
			self.state_portal = 'aceptacion'
			if self.company_id.app_id.metodo_confirmacion_tc == 'manual':
				self.leyenda_tc = "Lo contactaremos para finalizar la acreditacion."
			elif self.company_id.app_id.metodo_confirmacion_tc == 'sms':
				self.leyenda_tc = "Le enviamos un sms con los terminos y condiciones, siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
				self.sudo().metodo_aceptacion_sms_enviar_tc()
			elif self.company_id.app_id.metodo_confirmacion_tc == 'email':
				self.leyenda_tc = "Le enviamos un email con los terminos y condiciones, siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
				self.sudo().send_mail_tc('sin_sms')
			elif self.company_id.app_id.metodo_confirmacion_tc == 'email_sms':
				self.leyenda_tc = "Le enviamos un email con los terminos y condiciones, y un codigo por sms. Siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
				self.sudo().send_mail_tc('con_sms')
		else:
			raise ValidationError("Debe aceptar los terminos y condiciones.")

	@api.multi
	def button_wizard_editar_monto_solicitado_portal(self):
		params = {
			'prestamo_id': self.id,
		}
		view_id = self.env['financiera.prestamo.cambiar.monto.portal.wizard']
		new = view_id.create(params)
		return {
			'type': 'ir.actions.act_window',
			'name': 'Editar monto solicitado portal',
			'res_model': 'financiera.prestamo.cambiar.monto.portal.wizard',
			'view_type': 'form',
			'view_mode': 'form',
			'res_id': new.id,
			'view_id': self.env.ref('financiera_app.editar_monto_solicitado_portal_wizard', False).id,
			'target': 'new',
		}
	
	@api.one
	def _compute_primera_cuota_portal(self):
		if len(self.cuota_ids) > 0:
			self.primer_cuota_portal = self.cuota_ids[0].total
	
	@api.one
	def _compute_ultima_cuota_portal(self):
		if len(self.cuota_ids) > 0:
			self.ultima_cuota_portal = self.cuota_ids[len(self.cuota_ids)-1].total

	@api.multi
	def button_dummy(self):
		return True

	@api.one
	def button_aceptar_detalle_cuotas(self):
		self.aceptacion_detalle_cuotas_portal = True

	@api.one
	def button_aceptacion_tc_portal(self):
		self.aceptacion_tc_portal = True

	@api.one
	def sms_response_confirma_tc(self):
		self.sudo().enviar_a_acreditacion_pendiente()
		self.state_portal = 'confirmado'

	@api.multi
	def button_ver_detalle_cuotas(self):
		self.ensure_one()
		action = self.env.ref('financiera_app.detalle_cuotas_portal_action')
		result = action.read()[0]
		form_view = self.env.ref('financiera_app.detalle_cuotas_portal')
		result['views'] = [(form_view.id, 'form')]
		result['res_id'] = self.id
		result['target'] = 'new'
		return result

	@api.multi
	def button_ver_tc_portal(self):
		report_name = self.company_id.configuracion_id.email_tc_report_name
		ret = self.env['report'].get_action(self, report_name)
		ret['report_type'] = 'qweb-html'
		return ret

	def send_mail_tc(self, condicion_sms):
		if len(self.company_id.configuracion_id) > 0:
			configuracion_id = self.company_id.configuracion_id
			if len(configuracion_id.email_tc_template_id) > 0:
				email_template = configuracion_id.email_tc_template_id
				if configuracion_id.email_tc_report_name:
					pdf = self.pool['report'].get_pdf(self._cr, self._uid, [self.id], configuracion_id.email_tc_report_name, context=None)
					if pdf != None:
						new_attachment_id = self.env['ir.attachment'].create({
							'name': "Terminos y condiciones - "+self.name+'.pdf',
							'datas_fname': "Terminos y condiciones - "+self.name+'.pdf',
							'type': 'binary',
							'datas': base64.encodestring(pdf),
							'res_model': 'financiera.prestamo',
							'res_id': self.id,
							'mimetype': 'application/x-pdf',
							'company_id': self.company_id.id,
						})
						email_template.attachment_ids = [(6, 0, [new_attachment_id.id])]
				context = self.env.context.copy()
				context.update({
					'active_model': 'financiera.prestamo',
					'active_id': self.id,
				})
				if condicion_sms == 'con_sms':
					print("con_sms")
					context.update({
						'sub_action': 'tc_sent',
					})
				elif condicion_sms == 'sin_sms':
					print("sin_sms")
					context.update({
						'sub_action': 'tc_sent_without_sms',
					})
				email_template.with_context(context).send_mail(self.id, raise_exception=False, force_send=True)

	def cleanhtml(self, raw_html):
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext

	@api.model
	def message_update(self, msg, update_vals=None):
		""" Overrides mail_thread message_update that is called by the mailgateway
			through message_process.
			This override updates the document according to the email.
		"""
		print("Leyendo email entrante!!!")
		if len(self.company_id.app_id) > 0:
			app_id = self.company_id.app_id
			if app_id.metodo_confirmacion_tc in ('email', 'email_sms'):
				confirmar_prestamo = True
				msg_response_normalizado = self.cleanhtml(msg.get('body'))
				print("msg.body normalizado: ", msg_response_normalizado)
				# Comprobar si respondio con el codigo correcto
				if app_id.comprobar_codigo_prestamo:
					if self.email_tc_code in msg_response_normalizado[:len(str(self.email_tc_code))]:
						# Comprobar que el siguente caracter no se un numero
						if msg_response_normalizado[len(str(self.email_tc_code))].isdigit():
							confirmar_prestamo = False
						else:
							self.respuesta_email_codigo_prestamo = True

				# Comprobar que no se modifico el mensaje original en la respuesta
				if app_id.comprobar_mensaje_original:
					message_original_id = self.pool.get('mail.message').browse(self.env.cr, self.env.uid, msg.get('parent_id'))
					message_original_normalizado = self.cleanhtml(message_original_id.body)
					message_original_normalizado = message_original_normalizado.replace(u'\xa0', u'&nbsp;')
					if not message_original_normalizado in msg_response_normalizado:
						confirmar_prestamo = False
					else:
						self.respuesta_email_mensaje_original = True
				
				if confirmar_prestamo:
					self.sudo().enviar_a_acreditacion_pendiente()
					self.state_portal = 'confirmado'
		return True

class ExtendsFinancieraPrestamoEvaluacionPlan(models.Model):
	_name = 'financiera.prestamo.evaluacion.plan'
	_inherit = 'financiera.prestamo.evaluacion.plan'

	@api.multi
	def button_simular_plan(self):
		self.sudo().seleccionar_plan()
		self.sudo().prestamo_id.state_portal = 'simulacion'
		if len(self.sudo().prestamo_id.plan_ids) > 0:
			monto_maximo_aproximado = self.sudo().prestamo_id.plan_ids[0].monto_maximo_aproximado
			monto_maximo = '{:0,.2f}'.format(monto_maximo_aproximado).replace('.', '#').replace(',', '.').replace('#', ',')
			self.sudo().prestamo_id.preaprobado_portal = "TENES $"+monto_maximo+ " PRE APROBADO"
		else:
			self.sudo().prestamo_id.preaprobado_portal = ""