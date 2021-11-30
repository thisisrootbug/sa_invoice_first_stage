# -*- coding: utf-8 -*-
from odoo import models, fields, api ,_
from odoo.exceptions import UserError
import qrcode
import base64
import io
import logging

_logger = logging.getLogger(__name__)

class Invoice(models.Model):
    _inherit = 'account.invoice'

    qr_code_image = fields.Binary("QRCode Image", compute='_generate_qr_code')
    company_vat = fields.Char(string='Company / Vendor Vat',related="company_id.vat",store=True)


    def _generate_qr_code(self):
        qr_info = ''
        required_fields = {'Company':'company_id', 'Company Vat':'company_vat', 'Last Updated on':'write_date', 'Total':'amount_total', 'Tax':'amount_tax'}
        required_fields_attributes = self.env['ir.model.fields'].search([('model_id.model','=','account.invoice'), ('name','in',list(required_fields.values()))])
        data = {}
        for field_info in required_fields_attributes:
            if field_info.ttype == 'many2one':
                if field_info.name == "company_id":
                    qr_info += _('Company / Vendor Name') + " : " + self[field_info.name].display_name + "\n"
                    continue
                else:
                    qr_info += field_info.field_description +" : " + self[field_info.name].display_name + "\n"
            else:
                if field_info.name == "write_date":
                    qr_info += _('Timestamp') +" : " + self[field_info.name].strftime('%Y-%M-%d %H:%m:%S') + "\n"
                elif field_info.name == "amount_total":
                    qr_info += _('Total With Tax') + " : " + str(self[field_info.name]) + "\n"
                elif field_info.name == "amount_tax":
                    qr_info += _('Total VAT') + " : " + str(self[field_info.name]) + "\n"
        _logger.info(qr_info)
        qr_info = base64.b64encode(qr_info)
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
        if self.state == "paid":
            if ('ref' not in str(vals) and 'access_token' not in str(vals) and 'invoice_payment_ref' not in str(vals) and "name" not in str(vals) and "message_main_attachment_id" not in str(vals) and "tax_country_id" not in str(vals) and "l10n_sa_confirmation_datetime" not in str(vals)):
                _logger.info("data : ")
                _logger.info(vals)
                raise UserError(_("This Record Can't Be Modified"))
        return super(Invoice, self).write(vals)
