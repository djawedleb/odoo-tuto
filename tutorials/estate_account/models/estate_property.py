from odoo import models,  Command
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        res = super().sold_property()
        for prop in self:
            if not prop.buyer_id:
                raise UserError("Set a buyer before selling the property.")
            # Find a Sales journal for the property's company
            journal = self.env["account.journal"].search([
                ("type", "=", "sale"),
                ("company_id", "=", self.env.company.id),
            ], limit=1)
            if not journal:
                raise UserError("No Sales journal found for the company.")

            # self.env["account.move"].create({
            #     "partner_id": prop.buyer_id.id,   # customer
            #     "move_type": "out_invoice",       # customer invoice
            #     "journal_id": journal.id,
            # })
            commission = prop.selling_price * 0.06
            admin_fee = 100.0

            self.env["account.move"].create({
                "partner_id": prop.buyer_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Agency commission (6%) - {prop.name}",
                        "quantity": 1.0,
                        "price_unit": commission,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": admin_fee,
                    }),
                ],
            })
        return res
