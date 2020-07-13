# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import math

class FinancieraPrestamoCambiarMontoPortalWizards(models.TransientModel):
	_name = 'financiera.prestamo.cambiar.monto.portal.wizard'

	prestamo_id = fields.Many2one('financiera.prestamo', 'Cliente')
	monto_solicitado = fields.Float('Monto solicitado')
	
	@api.one
	def editar_monto_solicitado_portal(self):
		self.sudo().prestamo_id.set_monto_solicitado(self.monto_solicitado)
		self.sudo().prestamo_id.plan_id = None
