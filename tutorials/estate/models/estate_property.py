from datetime import date, timedelta
from odoo import models, fields

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property Model"
    
    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold')
    ], default='new', required=True, copy=False, string="Status")

    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
