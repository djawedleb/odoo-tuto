from datetime import timedelta
from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    price = fields.Float(required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], required=True, default='new', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True,
        string="Property Type"
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_compute_inverse_date_deadline',
        store=True,
        string="Deadline"
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'Offer price must be strictly positive')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (fields.Datetime.now() + timedelta(days=record.validity)).date()

    def _compute_inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Datetime.now().date()).days

    def accept_offer(self):
        for record in self:
            accepted_buyer = record.property_id.offer_ids.mapped('status')
            if 'accepted' in accepted_buyer:
                raise UserError("only one offer can be accepted.")
            else:
                record.property_id.state = 'offer_accepted'
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            record.property_id.state = 'offer_received'
            record.status = 'refused'
            record.property_id.selling_price = 0.0
        return True

    @api.model
    def create(self, vals):
        # Ensure required values exist
        property_id = vals.get('property_id')
        price = vals.get('price')
        if property_id and price is not None:
            prop = self.env['estate.property'].browse(property_id)
            # Prevent creating lower-than-existing offer
            existing_max = max(prop.offer_ids.mapped('price')) if prop.offer_ids else 0.0
            if price <= existing_max:
                raise UserError("Your offer price must be higher than existing offers.")

        # Create the offer
        offer = super().create(vals)

        # Set property state to 'offer_received'
        if property_id:
            prop = self.env['estate.property'].browse(property_id)
            prop.write({'state': 'offer_received'})

        return offer