from odoo import models, fields, api
from datetime import datetime

class CustomerFeedback(models.Model):
    _name = 'customer.management.feedback'
    _description = 'Customer Feedback'
    
    customer_id = fields.Many2one('customer.management.customer', string='Customer', required=True)
    product_id = fields.Many2one('product.template', string='Product')
    order_id = fields.Many2one('customer.management.order', string='Related Order')
    
    date_feedback = fields.Date(string='Feedback Date', default=fields.Date.today)
    feedback_type = fields.Selection([
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
        ('compliment', 'Compliment'),
        ('product_review', 'Product Review'),
        ('other', 'Other')
    ], string='Feedback Type')
    
    content = fields.Text(string='Feedback Content', required=True)
    rating = fields.Selection([
        ('1', '1 - Very Dissatisfied'),
        ('2', '2 - Dissatisfied'),
        ('3', '3 - Neutral'),
        ('4', '4 - Satisfied'),
        ('5', '5 - Very Satisfied')
    ], string='Rating')
    
    staff_id = fields.Many2one('res.users', string='Assigned Staff')
    response = fields.Text(string='Response')
    date_response = fields.Date(string='Response Date')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('responded', 'Responded'),
        ('closed', 'Closed')
    ], string='Status', default='new')
    
    def action_in_progress(self):
        self.write({
            'state': 'in_progress',
            'staff_id': self.env.user.id
        })
    
    def action_respond(self):
        self.write({
            'state': 'responded',
            'date_response': fields.Date.today()
        })
    
    def action_close(self):
        self.write({'state': 'closed'})
        
    @api.model
    def create(self, vals):
        record = super(CustomerFeedback, self).create(vals)
        # Update product rating if this is a product review
        if record.product_id and record.rating:
            self._update_product_rating(record.product_id.id)
        return record
    
    def write(self, vals):
        result = super(CustomerFeedback, self).write(vals)
        # If rating or product changed, update product rating
        if 'rating' in vals or 'product_id' in vals:
            product_ids = []
            if 'product_id' in vals and self.product_id:
                product_ids.append(self.product_id.id)
            for record in self:
                if record.product_id and record.product_id.id not in product_ids:
                    product_ids.append(record.product_id.id)
            
            for product_id in product_ids:
                self._update_product_rating(product_id)
        return result
    
    def _update_product_rating(self, product_id):
        """Update the average rating for a product"""
        feedback_ratings = self.search([
            ('product_id', '=', product_id),
            ('rating', '!=', False)
        ])
        
        if feedback_ratings:
            total_rating = 0
            count = 0
            for feedback in feedback_ratings:
                try:
                    rating_value = int(feedback.rating)
                    total_rating += rating_value
                    count += 1
                except (ValueError, TypeError):
                    continue
            
            if count > 0:
                avg_rating = total_rating / count
                self.env['product.template'].browse(product_id).write({
                    'customer_rating': avg_rating
                })