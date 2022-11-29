from odoo import api,fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"
    
    
    #------------------- fields -------------------#
    
    price = fields.Float("Price")
    status = fields.Selection([('a','Accepted'),('r','Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", string="Property Type", store=True
    )
    state = fields.Selection(selection=[("accepted", "Accepted"),("refused", "Refused"),],string="Status",copy=False,default=False,)
    validity = fields.Integer("Validity", default = 7)
    date_deadline = fields.Date("Date deadline")
    
    #------------------- computed functions -------------------#
    #calculate date deadline
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    
        




    
    
    
    
    
    
    