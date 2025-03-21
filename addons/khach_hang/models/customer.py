from odoo import models, fields, api
from datetime import datetime

class Customer(models.Model):
    _name = 'customer.management.customer'
    _description = 'Customer'
    
    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    
    # Potential customer fields
    is_potential = fields.Boolean(string='Is Potential Customer')
    interested_product_type = fields.Many2one('product.category', string='Interested Product Type')
    source = fields.Selection([
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('advertisement', 'Advertisement'),
        ('other', 'Other')
    ], string='Lead Source')
    
    # Customer care fields
    needs_care = fields.Boolean(string='Needs Care')
    last_care_date = fields.Date(string='Last Care Date')
    next_care_date = fields.Date(string='Next Care Date')
    
    # Relations
    order_ids = fields.One2many('customer.management.order', 'customer_id', string='Orders')
    care_ids = fields.One2many('customer.management.care', 'customer_id', string='Care History')
    feedback_ids = fields.One2many('customer.management.feedback', 'customer_id', string='Feedback')
    inquiry_ids = fields.One2many('customer.management.inquiry', 'customer_id', string='Inquiries')
    
    order_count = fields.Integer(compute='_compute_order_count', string='Order Count')
    care_count = fields.Integer(compute='_compute_care_count', string='Care Count')
    
    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)
    
    @api.depends('care_ids')
    def _compute_care_count(self):
        for record in self:
            record.care_count = len(record.care_ids)