from odoo import models, fields, api

class Product(models.Model):
    _inherit = 'product.template'
    
    # Additional fields for customer management
    customer_rating = fields.Float(string='Customer Rating', default=0.0, help="Average customer rating from 0 to 5")
    feedback_count = fields.Integer(string='Feedback Count', compute='_compute_feedback_count')
    popular_with_customers = fields.Boolean(string='Popular with Customers', compute='_compute_popular', store=True)
    customer_notes = fields.Text(string='Customer Notes', help="Special notes about this product for customer management")
    
    # For potential customers
    recommended_for_new = fields.Boolean(string='Recommended for New Customers', 
                                         help="This product is recommended for new or potential customers")
    
    # For customer care
    requires_follow_up = fields.Boolean(string='Requires Follow-up', 
                                        help="Products that may require customer follow-up after purchase")
    follow_up_days = fields.Integer(string='Follow-up Days', 
                                   help="Number of days after purchase to follow up with customer")
    
    # Related fields
    customer_feedback_ids = fields.One2many('customer.management.feedback', 'product_id', string='Customer Feedback')
    
    @api.depends('customer_feedback_ids')
    def _compute_feedback_count(self):
        for product in self:
            product.feedback_count = len(product.customer_feedback_ids)
    
    @api.depends('customer_rating', 'feedback_count')
    def _compute_popular(self):
        for product in self:
            # A product is considered popular if it has a good rating and enough feedback
            product.popular_with_customers = product.customer_rating >= 4.0 and product.feedback_count >= 5
    
    def action_view_feedback(self):
        self.ensure_one()
        return {
            'name': 'Product Feedback',
            'type': 'ir.actions.act_window',
            'res_model': 'customer.management.feedback',
            'view_mode': 'tree,form',
            'domain': [('product_id', '=', self.id)],
            'context': {'default_product_id': self.id}
        }