# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError,ValidationError
from odoo.tools.safe_eval import safe_eval
from datetime import datetime

from urllib.request import urlopen
import simplejson

class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def _compute_suggested_price(self):
        for rec in self:
            if rec.origin:
                order = self.env['sale.order'].search([('name','=',rec.origin)],limit=1)
                for order_line in order.order_line:
                    rec.suggested_price = order_line.suggested_price

    suggested_price = fields.Float('Precio sugerido',compute=_compute_suggested_price)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self,vals):
        res = super(SaleOrderLine, self).create(vals)
        if res.product_id:
            suggested_price = res.product_id.list_price
            res.write({'suggested_price': suggested_price})
        return res


    @api.multi
    def write(self,vals):
        res = super(SaleOrderLine, self).write(vals)
        if 'product_id' in vals.keys():
            rec = self[0]
            suggested_price = rec.product_id.list_price
            rec.write({'suggested_price': suggested_price})
        return res

    suggested_price = fields.Float('Precio sugerido')




