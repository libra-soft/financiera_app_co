# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtendsResBank(models.Model):
	_name = 'res.bank'
	_inherit = 'res.bank'

	code = fields.Char('Codigo', help='Clave de 3 digitos.')

