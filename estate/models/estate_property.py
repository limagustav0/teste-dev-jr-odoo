from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class EstateProperty(models.Model):
    
    
    _sql_constraints = [
        ('estate_property_expected_price_positive', 'CHECK(expected_price > 0)','The expected price must be strictly positive.'),
        ('estate_property_selling_price_positive', 'CHECK(selling_price >= 0)','The selling price must be strictly positive.'),
        ('estate_property_offer', 'CHECK(offer_ids.price >= 0)','The offer price must be strictly positive.'),
        ('estate_property_name', 'UNIQUE(name)','The property tag name and property type name must be unique.'),
    ]
    
    #------------------- functions -------------------#
    
    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)
 
    _name = "estate.property"
    _description = "real estate property"
    _order = "name desc"
    
    
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

    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Only new and canceled properties can be deleted.")
        return super().unlink()
    
        
    

    
    #------------------- action functions -------------------#
    
    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Canceled properties cannot be sold")
        return self.write({"state" : "sold"})
    
    def action_cancel(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled")
        return self.write({"state" : "canceled"})
    
    
    #------------------- constraint functions -------------------#
    
    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )
    
    def action_cancel(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled")
        return self.write({"state" : "canceled"})

    
    @api.onchange('offer_ids')
    def chance_status(self):
        for prop in self:
            if len(prop.offer_ids):
                prop.state = "offer_received"
    
    

    
            
    

    
    