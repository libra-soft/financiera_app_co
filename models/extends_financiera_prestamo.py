# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError

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
	leyenda_tc = fields.Char(" ", default=" ")
	app_cbu = fields.Char('CBU para depositar el capital')


	@api.model
	def default_get(self, fields):
		rec = super(ExtendsFinancieraPrestamo, self).default_get(fields)
		# configuracion_id = self.env.user.company_id.configuracion_id
		context = dict(self._context or {})
		current_uid = context.get('uid')
		current_user = self.env['res.users'].browse(current_uid)
		app_config_id = current_user.company_id.app_id
		# sucursal_id = current_user.entidad_login_id
		# partner_id = None
		if current_user.user_has_groups('financiera_prestamos.user_portal'):
			partner_id = current_user.partner_id.id
			app_cbu = current_user.app_cbu
			rec.update({
				'partner_id': partner_id,
				'origen_id': app_config_id.portal_origen_id.id,
				'sucursal_id': app_config_id.portal_sucursal_id.id,
				'responsable_id': app_config_id.portal_responsable_id.id,
				'app_cbu': app_cbu,
				'monto_solicitado': app_config_id.monto_minimo_solicitud,
			})
		return rec

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

	@api.one
	def button_simular(self):
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
			elif self.company_id.app_id.metodo_confirmacion_tc in ('sms'):
				self.leyenda_tc = "Le enviamos un sms con los terminos y condiciones, siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
				self.sudo().metodo_aceptacion_sms_enviar_tc()
			elif self.company_id.app_id.metodo_confirmacion_tc in ('sms_email'):
				self.leyenda_tc = "Le enviamos un email con los terminos y condiciones, y un codigo por sms. Siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
			elif self.company_id.app_id.metodo_confirmacion_tc == 'email':
				self.leyenda_tc = "Le enviamos un email con los terminos y condiciones, siga las instrucciones que contiene el mismo mensaje para finalizar la acreditacion."
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