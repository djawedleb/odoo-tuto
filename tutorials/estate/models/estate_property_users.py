from odoo import models, fields


class EstatePropertyUsers(models.Model):

    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'user_id',  # This is the inverse of the user_id field in estate.property
        string="Properties",
        domain="[('state', 'in', ['new', 'offer_received', 'offer_accepted'])]"  # Only available properties
    )