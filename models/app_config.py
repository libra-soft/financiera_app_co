# -*- coding: utf-8 -*-

from openerp import models, fields, api

class AppConfig(models.Model):
    _name = 'app.config'

    name = fields.Char('Nombre')
    # Parametros de la solicitud
    monto_minimo_solicitud = fields.Float('Monto minimo de solicitud')
    monto_maximo_solicitud = fields.Float('Monto maximo de solicitud')
    monto_incremento = fields.Float('Monto incremento')
    cuotas_minimas_solicitud = fields.Float('Cantidad minima de cuotas en solicitud')
    cuotas_maximas_solicitud = fields.Float('Cantidad maxima de cuotas en solicitud')
    cuotas_incremento = fields.Float('Cantidad de incremento')

    sucursal_id = fields.Many2one('financiera.entidad', 'Sucursal')
    comercio_id = fields.Many2one('financiera.entidad', 'Comercio')
    responsable_user_id = fields.Many2one('res.users', 'Responsable')
    # unique_documentation_report = fields.Char('Nombre del reporte unico a firmar por el cliente')
    company_id = fields.Many2one('res.company', 'Empresa', required=False,
       default=lambda self: self.env['res.company']._company_default_get('app.config'))





