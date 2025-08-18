from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"
    _order = 'sequence, name desc'

    name = fields.Char(required=True)
    property_ids = fields.One2many(
        'estate.property', 'property_type_id', string="Properties"
    )
    sequence = fields.Integer("Sequence", default=10)

    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The name must be unique.'),
    ]

    offer_count = fields.Integer(
        compute='_compute_offer_count',
        string="Number of Offers"
    )

    @api.depends('property_ids.offer_ids')
    def _compute_offer_count(self):
        """Count total offers for this property type"""
        for record in self:
            offers = record.property_ids.mapped('offer_ids')
            record.offer_count = len(offers)

