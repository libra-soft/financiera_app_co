# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtendsResBank(models.Model):
	_name = 'res.bank'
	_inherit = 'res.bank'

	code = fields.Char('Codigo', help='Clave de 3 digitos.')

	def lista_de_bancos(self):
		lista_de_bancos = []
		banco_obj = self.pool.get('res.bank')
		banco_ids = banco_obj.search(self.env.cr, self.env.uid, [])
		for _id in banco_ids:
			banco_id = self.env['res.bank'].browse(_id)
			lista_de_bancos.append((banco_id.code, banco_id.name))
		return lista_de_bancos
