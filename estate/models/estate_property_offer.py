from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    
    price = fields.Float("Price")
    status = fields.Selection([('a','Accepted'),('r','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)
    