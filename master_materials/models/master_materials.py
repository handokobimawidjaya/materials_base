# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning

class MasterMaterials(models.Model):
    _name = "master.materials"
    _description = "Master Materials"

    name = fields.Char("Material Name")
    code = fields.Char("Material Code")
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton'),
    ], string="Material Type")
    price = fields.Float("Material Price")
    supplier_id = fields.Many2one('res.partner', string='Supplier')

    @api.onchange('price')
    def onchange_price(self):
        if self.price:
            if int(self.price) < 100:
                raise Warning('Harga Material tidak boleh kurang dari 100.')