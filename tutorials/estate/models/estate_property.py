from datetime import date, timedelta
from odoo import api,models, fields
from odoo.tools.populate import compute


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property Model"

    name = fields.Char(required=True, default="Unknown")
    user_id = fields.Many2one('res.users', string='Salesperson',
                              default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False
    )

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
    # This means: Many properties can share the same property type.
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")

    # A property can have many tags and a tag can be assigned to many properties. This is supported by the many2many concept.
    tag_ids = fields.Many2many(
        'estate.property.tag', )

    offer_ids= fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Float(
        compute='_compute_total_area',
        store=True,
    )
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    best_price = fields.Float(
        compute="_compute_best_price",
        store=True,
        string="Best Price"
    )
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0


    @api.onchange('garden_area','garden_orientation','garden')
    def _onchange_garden_area(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False
