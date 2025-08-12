from datetime import timedelta

from odoo import api,models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection([
        ('draft', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], required=True, default='draft', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property',   required=True)

    validity = fields.Integer(default=7,)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_compute_inverse_date_deadline',
        store=True,
        string="Deadline"
    )

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
            if  'accepted' in accepted_buyer:
                raise UserError("This offer has already been accepted.")
            else:
                record.status = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
