# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import math

class ResPartnerSetPasswordWizards(models.TransientModel):
	_name = 'res.partner.set.password.wizard'

	partner_id = fields.Many2one('res.partner', 'Cliente')
	nuevo_password = fields.Char('Nueva contraseña')
	password_match_message = fields.Char('Requerimientos', compute='_compute_password_match_message')

	@api.one
	def _compute_password_match_message(self):
		self.password_match_message = self.partner_id.password_match_message()

	@api.multi
	def generar_nuevo_password(self):
		nuevo_password = self.partner_id.password_generate()
		return self.partner_id.wizard_set_password(nuevo_password)
		
	@api.one
	def set_password(self):
		if self.partner_id.check_password(self.nuevo_password):
			self.partner_id.set_password(self.partner_id.id, self.nuevo_password)

	@api.one
	def set_password_and_send_by_email(self):
		self.set_password()
		self.partner_id.send_mail_password_generate(self.nuevo_password)
	
	@api.multi
	def set_password_and_send_by_whatsapp(self):
		self.set_password()
		if self.partner_id.mobile:
			url = 'https://wa.me/+549' + self.partner_id.mobile + '?text=Hola ' + self.partner_id.name + '%0A'
			url += 'Su usuario es: ' + self.partner_id.email + '%0A'
			url += 'Su nueva contraseña es: ' + self.nuevo_password + '%0A'
			url += 'Ingrese en: ' + self.partner_id.company_id.portal_url
			return {
				'name'     : 'Whatsapp',
				'res_model': 'ir.actions.act_url',
				'type'     : 'ir.actions.act_url',
				'target'   : 'new',
				'url'      : url,
			}
		else:
			raise UserError("El celular no esta cargado.")