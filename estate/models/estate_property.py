from odoo import fields, models
from datetime import date, timedelta


class EstateProperty(models.Model):
    
    def _default_date_availability(self):
        return fields.Date.context_today(self) + timedelta(90)
 
    _name = "estate.property"
    _description = "real estate property"
    
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
    user_id = fields.Many2one("res.users", copy=False, default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    
    