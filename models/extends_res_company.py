# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	app_id = fields.Many2one('app.config', 'Configuracion Plataforma web y App Movil')
	app_is_contracted = fields.Boolean('Esta contratado?')
	# app_ver_y_compartir_riesgo_cliente = fields.Booelan("Ver y compartir riesgo cliente")
