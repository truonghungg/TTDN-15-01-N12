from odoo import models, fields, api
from datetime import datetime, timedelta

class Order(models.Model):
    _name = 'customer.management.order'
    _description = 'Customer Order'
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, 
                       default=lambda self: self.env['ir.sequence'].next_by_code('customer.order'))
    customer_id = fields.Many2one('customer.management.customer', string='Customer', required=True)
    date_order = fields.Date(string='Order Date', default=fields.Date.today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    
    order_line_ids = fields.One2many('customer.management.order.line', 'order_id', string='Order Lines')
    total_amount = fields.Float(compute='_compute_total_amount', string='Total Amount', store=True)
    
    feedback_ids = fields.One2many('customer.management.feedback', 'order_id', string='Feedback')
    feedback_requested = fields.Boolean(string='Feedback Requested')
    
    care_needed = fields.Boolean(string='Care Needed', compute='_compute_care_needed', store=True)
    care_date = fields.Date(string='Care Date', compute='_compute_care_date', store=True)
    
    @api.depends('order_line_ids.subtotal')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_line_ids)
    
    @api.depends('order_line_ids.product_id', 'order_line_ids.product_id.requires_follow_up', 'state')
    def _compute_care_needed(self):
        for order in self:
            if order.state == 'done':
                for line in order.order_line_ids:
                    if line.product_id.requires_follow_up:
                        order.care_needed = True
                        break
                    else:
                        order.care_needed = False
            else:
                order.care_needed = False
    
    @api.depends('date_order', 'order_line_ids.product_id.follow_up_days', 'care_needed')
    def _compute_care_date(self):
        for order in self:
            if order.care_needed and order.date_order:
                max_days = 0
                for line in order.order_line_ids:
                    if line.product_id.requires_follow_up and line.product_id.follow_up_days > max_days:
                        max_days = line.product_id.follow_up_days
                
                if max_days > 0:
                    order.care_date = order.date_order + timedelta(days=max_days)
                else:
                    order.care_date = order.date_order + timedelta(days=7)  # Default 7 days
            else:
                order.care_date = False
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_done(self):
        self.write({'state': 'done'})
        # Schedule customer care if needed
        for order in self:
            if order.care_needed and order.customer_id:
                order.customer_id.write({
                    'needs_care': True,
                    'next_care_date': order.care_date
                })
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})
    
    def action_request_feedback(self):
        self.ensure_one()
        self.write({'feedback_requested': True})
        # Here you could also send an email to the customer requesting feedback
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Feedback',
            'res_model': 'customer.management.feedback',
            'view_mode': 'form',
            'context': {
                'default_customer_id': self.customer_id.id,
                'default_order_id': self.id,
                'default_feedback_type': 'product_review'
            },
            'target': 'new'
        }

class OrderLine(models.Model):
    _name = 'customer.management.order.line'
    _description = 'Order Line'
    
    order_id = fields.Many2one('customer.management.order', string='Order')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(compute='_compute_subtotal', string='Subtotal', store=True)
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
    
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit