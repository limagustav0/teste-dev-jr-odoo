from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"
    
    
    #------------------- fields -------------------#
    
    name = fields.Char("Name", required = True)
    color = fields.Integer("Color Index")