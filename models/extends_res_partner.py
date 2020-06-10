# -*- coding: utf-8 -*-

from openerp import models, fields, api
from cStringIO import StringIO
import base64

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_datos_personales = fields.Boolean('Datos personales completos')
	app_nombre = fields.Char('Nombre')
	app_apellido = fields.Char('Apellido')
	app_documento = fields.Char('Documento')
	app_nacimiento = fields.Date('Nacimiento')
	# Datos Domicilio
	app_datos_domicilio = fields.Boolean('Datos domicilio completos')
	app_direccion = fields.Char('Direccion')
	app_numero = fields.Char('Numero')
	app_cp = fields.Char('CP')
	app_telefono = fields.Char('Telefono fijo')
	app_localidad = fields.Char('Localidad')
	app_provincia = fields.Char('Provincia')
	# Datos Ingreso
	app_datos_ingreso = fields.Boolean('Datos de ingreso completos')
	app_ingreso = fields.Char("Ingreso")
	app_cuotas = fields.Char("Cuotas")
	app_ingreso_pareja = fields.Char("Ingreso de la pareja")
	app_otros_ingresos = fields.Char("Otros ingresos")
	app_asignaciones = fields.Char("Asignaciones")
	app_ocupacion = fields.Char("ocupacion")
	app_puesto = fields.Char("Puesto")
	# Datos vivienda y transporte
	app_datos_vivienda_transporte = fields.Boolean("Datos de vivienda y transporte completos")
	app_vivienda = fields.Char("Vivienda")
	app_alquiler = fields.Char("Monto alquiler")
	app_hipoteca = fields.Char("Credito hipotecario")
	app_vivienda_tiempo = fields.Char("Anos que vive ahi")
	app_vivienda_conviven = fields.Char("Personas que conviven")
	app_vivienda_hijos = fields.Char("Hijos que conviven")
	app_transporte = fields.Char("Transporte")
	app_prendario = fields.Char("Credito prendario")
	# DNI y selfie
	app_dni_frontal = fields.Binary("DNI frontal", store=True, attachment=False)
	app_dni_frontal_download = fields.Binary("", related="app_dni_frontal")
	app_dni_frontal_download_name = fields.Char("", default="dni-frontal.jpeg")
	app_dni_posterior = fields.Binary("DNI posterior")
	app_dni_posterior_download = fields.Binary("", related="app_dni_posterior")
	app_dni_posterior_download_name = fields.Char("", default="dni-posterior.jpeg")
	app_selfie = fields.Binary("Selfie")
	app_selfie_download = fields.Binary("", related="app_selfie")
	app_selfie_download_name = fields.Char("", default="selfie.jpeg")
	# CBU
	app_cbu = fields.Char("CBU")
	app_alias = fields.Char("Alias")
	app_numero_celular = fields.Char("Numero de celular")
	app_numero_celular_validado = fields.Boolean("Validado")
	app_codigo = fields.Char("Codigo")
