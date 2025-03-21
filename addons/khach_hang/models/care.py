from odoo import models, fields, api
from datetime import datetime

class CustomerCare(models.Model):
    _name = 'customer.management.care'
    _description = 'Customer Care'
    
    customer_id = fields.Many2one('customer.management.customer', string='Customer', required=True)
    care_date = fields.Date(string='Care Date', default=fields.Date.today)
    staff_id = fields.Many2one('res.users', string='Staff', default=lambda self: self.env.user)
    contact_method = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('other', 'Other')
    ], string='Contact Method')
    notes = fields.Text(string='Notes')
    follow_up_needed = fields.Boolean(string='Follow-up Needed')
    follow_up_date = fields.Date(string='Follow-up Date')
    
    @api.model
    def create(self, vals):
        record = super(CustomerCare, self).create(vals)
        # Update the last care date on the customer
        if record.customer_id:
            record.customer_id.write({'last_care_date': record.care_date})
        return record