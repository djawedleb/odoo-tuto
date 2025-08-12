from datetime import timedelta

from odoo import api,models, fields



class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ('canceled', 'Canceled')
    ], default='accepted', required=True)
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