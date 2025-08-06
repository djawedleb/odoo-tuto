from odoo import models,fields

class estate_property(models.Model):
    _name = "estate_property"
    _description = "Test Model"

    name = fields.Char()
    description = fields.Text()