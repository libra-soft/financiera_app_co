# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AppConfig(models.Model):
	_name = 'app.config'

	name = fields.Char('Nombre')
	# Parametros de la solicitud
	monto_minimo_solicitud = fields.Float('Monto minimo de solicitud')
	monto_maximo_solicitud = fields.Float('Monto maximo de solicitud')
	monto_incremento = fields.Integer('Monto incremento')
	monto_inicial = fields.Float('Monto inicial')
	cuotas_minimas_solicitud = fields.Float('Cantidad minima de cuotas en solicitud')
	cuotas_maximas_solicitud = fields.Float('Cantidad maxima de cuotas en solicitud')
	cuotas_incremento = fields.Integer('Cantidad de incremento')
	cuotas_inicial = fields.Float('Cantidad de cuotas inicial')
	# Opciones movil
	app_sucursal_id = fields.Many2one('financiera.entidad', 'Sucursal')
	app_comercio_id = fields.Many2one('financiera.entidad', 'Comercio')
	app_responsable_id = fields.Many2one('res.users', 'Responsable')
	app_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en movil')
	# Opciones portal
	portal_sucursal_id = fields.Many2one('financiera.entidad', 'Sucursal')
	portal_comercio_id = fields.Many2one('financiera.entidad', 'Comercio')
	portal_responsable_id = fields.Many2one('res.users', 'Responsable')
	portal_origen_id = fields.Many2one('financiera.prestamo.origen', 'Origen del prestamo en portal')
	# unique_documentation_report = fields.Char('Nombre del reporte unico a firmar por el cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False)
	# Requerimientos para solicitud
	app_cbu = fields.Boolean('Requiere CBU para deposito del capital')