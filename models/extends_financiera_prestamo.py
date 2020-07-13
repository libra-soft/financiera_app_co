# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	state_portal = fields.Selection([
		('requisitos', 'Requisitos'),
		('simulacion', 'Simulacion'),
		('condiciones', 'Condiciones'),
		# ('solicitado', 'Solicitado'),
	], 'Estado en portal', default='requisitos')
	cuotas_portal = fields.Integer("Cuotas", related='plan_id.cuotas')
	primer_cuota_portal = fields.Float('Primera cuota', digits=(16,2), compute='_compute_primera_cuota_portal')
	ultima_cuota_portal = fields.Float('Ultima cuota', digits=(16,2), compute='_compute_ultima_cuota_portal')
	preaprobado_portal = fields.Char(" ", default="")
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
				'monto_solicitado': app_config_id.monto_inicial,
			})
		return rec

	@api.one
	def button_regresar(self):
		if self.state_portal == 'simulacion':
			self.state_portal = 'requisitos'
			self.preaprobado_portal = ""
			self.sudo().enviar_a_solicitado()

	@api.one
	def button_simular(self):
		self.sudo().enviar_a_revision()
		self.sudo().enviar_a_autorizado()
		if len(self.plan_ids) > 0:
			# Preseleccion de plan: El primero con el mayor monto!
			self.monto_solicitado = self.sudo().plan_ids[0].monto_maximo_aproximado
			monto_maximo = '{:0,.2f}'.format(self.monto_solicitado).replace('.', '#').replace(',', '.').replace('#', ',')
			self.preaprobado_portal = "TENES $"+monto_maximo+ " PRE APROBADO"
			self.sudo().plan_ids[0].seleccionar_plan()
			self.state_portal = 'simulacion'
		else:
			self.preaprobado_portal = ""
	
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