# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
import xlwt
import base64
import StringIO


class FinancieraPrestamoCuotaToExcelWizard(models.TransientModel):
	_name = 'financiera.prestamo.cuota.to.excel.wizard'
	
	fecha_inicio_debitos = fields.Date('Fecha de Inicio Débitos')
	fecha_fin_debitos = fields.Date('Fecha de Fin Débitos')
	reintentos = fields.Integer('Reintentos')
	file = fields.Binary('Archivo')
	file_name = fields.Char('Nombre', default='cuotas.xls')

	@api.multi
	def generate_excel(self):
		context = dict(self._context or {})
		active_ids = context.get('active_ids')
		stream = StringIO.StringIO()
		book = xlwt.Workbook(encoding='utf-8')
		sheet = book.add_sheet(u'Sheet1')
		sheet.write(0, 0, 'Tipo Registro')
		sheet.write(0, 1, 'Tipo Id adherente')
		sheet.write(0, 2, 'Id adherente')
		sheet.write(0, 3, 'Número Referencia')
		sheet.write(0, 4, 'Tipo de documento de Identidad')
		sheet.write(0, 5, 'Documento de Identidad')
		sheet.write(0, 6, 'Apellido y Nombre')
		sheet.write(0, 7, 'DÍAS DE ATRASO')
		sheet.write(0, 8, 'Provincia')
		sheet.write(0, 9, 'Empleador')
		sheet.write(0, 10, 'Código Servicio del cliente')
		sheet.write(0, 11, 'Código Medio de Pago')
		sheet.write(0, 12, 'Nro. Cuenta del medio de pago')
		sheet.write(0, 13, 'Nro. Cuenta del medio de pago')
		sheet.write(0, 14, 'Nro. Cuenta del medio de pago')
		sheet.write(0, 15, 'Código Moneda')
		sheet.write(0, 16, 'Tipo de operación de fecha')
		sheet.write(0, 17, 'Monto Cuota')
		sheet.write(0, 18, 'Fecha de Inicio Débitos')
		sheet.write(0, 19, 'Fecha de Fin Débitos')
		sheet.write(0, 20, 'Reintentos')
		sheet.write(0, 21, 'Monto a Debitar')
		sheet.write(0, 22, 'Detalle débito')
		sheet.write(0, 23, 'Información Medio de Pago')
		row = 1
		for _id in active_ids:
			cuota_id = self.env['financiera.prestamo.cuota'].browse(_id)
			col = 0
			while col <= 23:
				if col == 0:
					sheet.write(row, col, 'D')
				elif col == 1:
					sheet.write(row, col, 'C')
				elif col == 2:
					sheet.write(row, col, int(cuota_id.partner_id.main_id_number))
				elif col == 3:
					sheet.write(row, col, cuota_id.id)
				elif col == 4:
					sheet.write(row, col, 'D')
				elif col == 5:
					sheet.write(row, col, cuota_id.partner_id.dni)
				elif col == 6:
					sheet.write(row, col, cuota_id.partner_id.name)
				elif col == 7:
					sheet.write(row, col, cuota_id.partner_id.alerta_dias_ultimo_pago)
				elif col == 8:
					sheet.write(row, col, cuota_id.partner_id.state_id.name)
				elif col == 9:
					sheet.write(row, col, cuota_id.partner_id.function)
				elif col == 10:
					sheet.write(row, col, '')
				elif col == 11:
					sheet.write(row, col, 'D')
				elif col == 12:
					sheet.write(row, col, cuota_id.prestamo_id.app_cbu)
				elif col == 13:
					sheet.write(row, col, cuota_id.partner_id.app_cbu)
				elif col == 14:
					if len(cuota_id.partner_id.bank_ids) > 0:
						sheet.write(row, col, cuota_id.partner_id.bank_ids[0].cbu)
				elif col == 15:
					sheet.write(row, col, '032')
				elif col == 16:
					sheet.write(row, col, 'B')
				elif col == 17:
					sheet.write(row, col, int(str(cuota_id.saldo).replace(',','').replace('.', '')))
				elif col == 18:
					if self.fecha_inicio_debitos:
						sheet.write(row, col, str(self.fecha_inicio_debitos).replace('-', '').replace('/', ''))
				elif col == 19:
					if self.fecha_fin_debitos:
						sheet.write(row, col, str(self.fecha_fin_debitos).replace('-', '').replace('/', ''))
				elif col == 20:
					sheet.write(row, col, self.reintentos)
				elif col == 21:
					sheet.write(row, col, int(str(cuota_id.saldo).replace(',','').replace('.', '')))
				elif col == 22:
					sheet.write(row, col, 'PRESTAMO')
				elif col == 23:
					sheet.write(row, col, cuota_id.prestamo_id.name)
				col += 1
			row +=1
		book.save(stream)
		self.file = base64.encodestring(stream.getvalue())
		return {'type': 'ir.actions.do_nothing'}