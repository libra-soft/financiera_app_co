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
	app_calle = fields.Char("Calle")
	app_altura = fields.Char("Altura")
	app_piso = fields.Char("Piso")
	app_departamento = fields.Char("Departamento")
	app_cp = fields.Char("CP")
	app_ciudad = fields.Char("Ciudad")
	app_provincia = fields.Char("Provincia")
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
	# Requeimiento de la tarjeta de debito
	requiere_tarjeta_debito = fields.Boolean('Requiere tarjeta de debito', readonly=True, related='company_id.app_id.requiere_tarjeta_debito')
	requiere_tarjeta_debito_pass = fields.Boolean('Supera el requerimiento de tarjeta de debito')
	app_tarjeta_debito_digitos_fin = fields.Char("Ultimos 4 digitos", related='partner_id.app_tarjeta_debito_digitos_fin')
	app_tarjeta_debito_vencimiento_month = fields.Selection(related='partner_id.app_tarjeta_debito_vencimiento_month')
	app_tarjeta_debito_vencimiento_year = fields.Selection(related='partner_id.app_tarjeta_debito_vencimiento_year')
	app_monto_solicitado_readonly = fields.Boolean('Monto solo lectura', default=False)
	app_estado_bloqueado = fields.Boolean(related='partner_id.app_estado_bloqueado')
	app_ip_registro_no_confiable = fields.Boolean(related='partner_id.app_ip_registro_no_confiable')
	# alertas
	alerta_show = fields.Boolean('Ver alertas', default=True)
	alerta_ultima_actualizacion = fields.Datetime(related='partner_id.alerta_ultima_actualizacion')
	alerta_ip_multiple_registros = fields.Integer(related='partner_id.alerta_ip_multiple_registros')
	alerta_celular_multiple_partner = fields.Integer(related='partner_id.alerta_celular_multiple_partner')
	alerta_celular_como_contacto = fields.Integer(related='partner_id.alerta_celular_como_contacto')
	alerta_domicilio_similar = fields.Integer(related='partner_id.alerta_domicilio_similar')

	alerta_prestamos_activos = fields.Integer(related='partner_id.alerta_prestamos_activos')
	alerta_prestamos_cobrados = fields.Integer(related='partner_id.alerta_prestamos_cobrados')
	
	alerta_cuotas_activas = fields.Integer(related='partner_id.alerta_cuotas_activas')
	alerta_cuotas_cobradas = fields.Integer(related='partner_id.alerta_cuotas_cobradas')
	alerta_cuotas_normal = fields.Integer(related='partner_id.alerta_cuotas_normal')
	alerta_cuotas_preventivas = fields.Integer(related='partner_id.alerta_cuotas_preventivas')
	alerta_cuotas_temprana = fields.Integer(related='partner_id.alerta_cuotas_temprana')
	alerta_cuotas_media = fields.Integer(related='partner_id.alerta_cuotas_media')
	alerta_cuotas_tardia = fields.Integer(related='partner_id.alerta_cuotas_tardia')
	alerta_cuotas_incobrable = fields.Integer(related='partner_id.alerta_cuotas_incobrable')
	# Datos compartidos entre financieras
	alerta_ver_y_compartir = fields.Boolean('Ver y compartir', related='company_id.app_id.app_ver_y_compartir_riesgo_cliente')
	alerta_registrado_financieras = fields.Integer(related='partner_id.alerta_registrado_financieras')
	alerta_prestamos_activos_financieras = fields.Integer(related='partner_id.alerta_prestamos_activos_financieras')
	alerta_cuotas_vencidas_financieras = fields.Integer(related='partner_id.alerta_cuotas_vencidas_financieras')
	alerta_compromiso_mensual_financieras = fields.Float(related='partner_id.alerta_compromiso_mensual_financieras')
	alerta_ip_no_confiable_financieras = fields.Integer(related='partner_id.alerta_ip_no_confiable_financieras')
	# Requerimientos automaticos
	app_requerimientos_completos_porcentaje = fields.Float("Cumplimiento de requerimientos", store=True, compute='change_app_requerimientos_porcentaje')
	app_requerimientos_cumplidos = fields.Char("Requerimientos cumplidos", store=True, compute='change_app_requerimientos_porcentaje')
	app_requerimientos_pendientes = fields.Char("Requerimientos pendientes", store=True, compute='change_app_requerimientos_porcentaje')

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
		if app_id.requiere_tarjeta_debito and (not partner_id.app_tarjeta_debito_digitos_fin or not partner_id.app_tarjeta_debito_vencimiento_month or not partner_id.app_tarjeta_debito_vencimiento_year):
			datos_incompletos += "* Completar los datos de la tarjeta de debito en CBU y medios de pago.\n"
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
		# self.button_actualizar_tarjeta_debito_prestamo_portal()
		# if not self.requiere_tarjeta_debito_pass:
		# 	raise UserError("Debe completar los datos de la tarjeta de debito para continuar.")
		self.sudo().enviar_a_revision()
		flag_aprobado = False
		for plan_id in self.plan_ids:
			if plan_id.state == 'aprobado':
				flag_aprobado = True
		if not flag_aprobado:
			self.preaprobado_portal = "No tenemos nada en este momento para usted. Vuelve a consultar dentro de 30 dias. Estamos calificando tu cuenta."
			self.state_portal = 'simulacion'
		else:
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
			raise UserError("Debe seleccionar Monto y Plan.")
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
	def button_confirmar_monto_solicitado_portal(self):
		self.sudo().set_monto_solicitado(self.monto_solicitado)
		self.sudo().plan_id = None
		self.app_monto_solicitado_readonly = True
	
	@api.multi
	def button_editar_monto_solicitado_portal(self):
		self.app_monto_solicitado_readonly = False
		
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
				msg_response_normalizado = self.cleanhtml(msg.get('body'))
				# Comprobar si respondio con el codigo correcto
				# if app_id.comprobar_codigo_prestamo:
				if self.email_tc_code in msg_response_normalizado[:len(str(self.email_tc_code))]:
					# Comprobar que el siguente caracter no se un numero
					if not msg_response_normalizado[len(str(self.email_tc_code))].isdigit():
						self.respuesta_email_codigo_prestamo = True

				# Comprobar que no se modifico el mensaje original en la respuesta
				# if app_id.comprobar_mensaje_original:
				message_original_id = self.pool.get('mail.message').browse(self.env.cr, self.env.uid, msg.get('parent_id'))
				message_original_normalizado = self.cleanhtml(message_original_id.body)
				message_original_normalizado = message_original_normalizado.replace(u'\xa0', u'&nbsp;')
				if message_original_normalizado in msg_response_normalizado:
					self.respuesta_email_mensaje_original = True
				
				confirmar_prestamo = True
				if app_id.comprobar_codigo_prestamo:
					confirmar_prestamo = self.respuesta_email_codigo_prestamo
				if app_id.comprobar_mensaje_original:
					confirmar_prestamo = confirmar_prestamo and self.respuesta_email_mensaje_original
				if app_id.metodo_confirmacion_tc_agregar_mobbex_suscripcion:
					confirmar_prestamo = confirmar_prestamo and self.mobbex_suscripcion_suscriptor_confirm
				if confirmar_prestamo:
					self.sudo().enviar_a_acreditacion_pendiente()
					self.state_portal = 'confirmado'
		return True

	@api.one
	def mobbex_suscripcion_exitosa(self):
		super(ExtendsFinancieraPrestamo, self).mobbex_suscripcion_exitosa()
		if len(self.company_id.app_id) > 0:
			app_id = self.company_id.app_id
			confirmar_prestamo = True
			if app_id.metodo_confirmacion_tc_agregar_mobbex_suscripcion:
				confirmar_prestamo = self.mobbex_suscripcion_suscriptor_confirm
			if app_id.comprobar_codigo_prestamo:
				confirmar_prestamo = confirmar_prestamo and self.respuesta_email_codigo_prestamo
			if app_id.comprobar_mensaje_original:
				confirmar_prestamo = confirmar_prestamo and self.respuesta_email_mensaje_original
			if confirmar_prestamo:
				self.sudo().enviar_a_acreditacion_pendiente()
				self.state_portal = 'confirmado'

	@api.multi
	def ver_solicitar_prestamo_portal(self):
		view_id = self.env.ref('financiera_app.financiera_prestamo_portal_form', False)
		return {
			'name': 'Solicitar prestamo',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'financiera.prestamo',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'inline',
		}


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

	@api.one
	def enviar_a_acreditacion_pendiente(self):
		super(ExtendsFinancieraPrestamo, self).enviar_a_acreditacion_pendiente()
		self.state_portal = 'confirmado'

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
		# Lista de cumplidos
		font_open_cumplidos = '<font style="border-radius:20px;background: #59C446;padding: 5px;color: white;float:left;">'
		app_requerimientos_cumplidos = ('</font>'+font_open_cumplidos).join(app_requerimientos_cumplidos)
		if app_requerimientos_cumplidos:
			app_requerimientos_cumplidos = font_open_cumplidos + app_requerimientos_cumplidos + '</font>'
		self.app_requerimientos_cumplidos = app_requerimientos_cumplidos
		# Lista de pendientes
		font_open_pendientes = '<font style="border-radius:20px;background: #BA2E2E;padding: 5px;color: white;float:left;">'
		app_requerimientos_pendientes = ('</font>'+font_open_pendientes).join(app_requerimientos_pendientes)
		if app_requerimientos_pendientes:
			app_requerimientos_pendientes = font_open_pendientes + app_requerimientos_pendientes + '</font>'
		self.app_requerimientos_pendientes = app_requerimientos_pendientes

class ExtendsFinancieraCuotaPrestamo(models.Model):
	_name = 'financiera.prestamo.cuota'
	_inherit = 'financiera.prestamo.cuota'

	@api.one
	def button_pagos_360_pagar_online(self):
		return {
			"type": "ir.actions.act_window", 
			"url": self.pagos_360_checkout_url, 
			"target": "new"
		}

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
