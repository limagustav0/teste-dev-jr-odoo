from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    
    
    #------------------- functions -------------------#
    
    def _default_date_availability(self):
        return fields.Date.context_today(self) + timedelta(90)
 
    _name = "estate.property"
    _description = "real estate property"
    
    
    #------------------- fields -------------------#
    
    name = fields.Char(string = "Name", required=True)
    description = fields.Text(string = "Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Date Availability", copy=False, default = lambda self : self._default_date_availability())
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection([('N','North'),('S','South'),('E','East'),('W','West')])
    active = fields.Boolean("Active", default =True)
    state = fields.Selection(selection=[("new", "New"),("offer_received", "Offer Received"),("offer_accepted", "Offer Accepted"),("sold", "Sold"),("canceled", "Canceled")], string="Status", required=True, copy=False,  default="new" )
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id")


    #------------------- computed functions -------------------#

    #calculate garden + living área
    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area
            
    total_area = fields.Integer(compute="_compute_area")
    
    #show the best offer
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0
    
    best_price = fields.Integer(compute = _compute_best_price)

    #default fields if garder = true
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    
    #------------------- action functions -------------------#
    
    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold")
        return self.write({"state" : "sold"})
    
    def action_cancel(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled")
        return self.write({"state" : "canceled"})
    

    
    