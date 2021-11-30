# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
from odoo.exceptions import UserError
import qrcode
import base64
import io
import logging

_logger = logging.getLogger(__name__)

class Invoice(models.Model):
    _inherit = 'account.move'

    qr_code_image = fields.Binary("QRCode Image", compute='_generate_qr_code')
    company_vat = fields.Char(string='Company / Vendor Vat',related="company_id.vat",store=True)


    def _generate_qr_code(self):
        qr_info = ''
        required_fields = ['company_id', 'company_vat', 'write_date', 'amount_total', 'amount_tax']
        required_fields_attributes = self.env['ir.model.fields'].search([('model_id.model','=','account.move'), ('name','in',required_fields)])
        data = {}
        for field_info in required_fields_attributes:
            if field_info.name == "company_id":
                tag = 1
                value = self[field_info.name].display_name
                if value:
                    qr_info += format(tag,'02X') + format(len(value.encode('utf-8')),'02X') + value.encode('utf-8').hex()
                else:
                    _logger.warning(field_info.name+" has no value")
                break
        for field_info in required_fields_attributes:
            if field_info.name == "company_vat":
                tag = 2
                value = self[field_info.name]
                if value:
                    qr_info += format(tag,'02X') + format(len(value.encode('utf-8')),'02X') + value.encode('utf-8').hex()
                else:
                    _logger.warning(field_info.name+" has no value")
                break
        for field_info in required_fields_attributes:
            if field_info.name == "write_date":
                tag = 3
                value = self[field_info.name].strftime("%Y-%M-%dT%H:%m:%SZ")
                if value:
                    qr_info += format(tag,'02X') + format(len(value.encode('utf-8')),'02X') + value.encode('utf-8').hex()
                else:
                    _logger.warning(field_info.name+" has no value")
                break
        for field_info in required_fields_attributes:
            if field_info.name == "amount_total":
                tag = 4
                value = self[field_info.name]
                if value:
                    qr_info += format(tag,'02X') + format(len(str(value).encode('utf-8')),'02X') + format(value,'0.2f').encode('utf-8').hex()
                else:
                    _logger.warning(field_info.name+" has no value")
                break
        for field_info in required_fields_attributes:
            if field_info.name == "amount_tax":
                tag = 5
                value = self[field_info.name]
                if value:
                    qr_info += format(tag,'02X') + format(len(str(value).encode('utf-8')),'02X') + format(value,'0.2f').encode('utf-8').hex()
                else:
                    _logger.warning(field_info.name+" has no value")
                break
        qr_info = base64.b64encode(bytearray.fromhex(qr_info))
        _logger.debug(qr_info)
        data = io.BytesIO()
        qrcode.make(qr_info, box_size=4).save(data, optimise=True, format='PNG')
        self.qr_code_image = base64.b64encode(data.getvalue()).decode()

    def unlink(self):
        if self.state != "draft":
            raise UserError(_("This Record Can't Be deleted"))
        return super(Invoice, self).unlink()

    def write(self,vals):
        if vals == {}:
            return
        if self.state == "posted":
            if ('access_token' not in str(vals) and 'invoice_payment_ref' not in str(vals) and "name" not in str(vals) and "message_main_attachment_id" not in str(vals) and "tax_country_id" not in str(vals)):
                _logger.info("data : ")
                _logger.info(vals)
                raise UserError(_("This Record Can't Be Modified"))
        return super(Invoice, self).write(vals)
