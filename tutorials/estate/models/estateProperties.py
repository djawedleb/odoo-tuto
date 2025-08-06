from odoo import models,fields

class TestModel(models.Model):
    _name = "test_model"
    _description = "Test Model"

    name = fields.Char()
    description = fields.Text()