from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real Estate Property Type"
    _order = 'name desc'

    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]
