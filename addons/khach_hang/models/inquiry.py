from odoo import models, fields, api
from datetime import datetime

class CustomerInquiry(models.Model):
    _name = 'customer.management.inquiry'
    _description = 'Customer Inquiry'
    
    name = fields.Char(string='Subject', required=True)
    customer_id = fields.Many2one('customer.management.customer', string='Customer', required=True)
    question = fields.Text(string='Question', required=True)
    date_asked = fields.Date(string='Date Asked', default=fields.Date.today)
    
    support_staff_id = fields.Many2one('res.users', string='Support Staff')
    answer = fields.Text(string='Answer')
    date_answered = fields.Date(string='Date Answered')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('answered', 'Answered'),
        ('closed', 'Closed')
    ], string='Status', default='new')
    
    def action_in_progress(self):
        self.write({
            'state': 'in_progress',
            'support_staff_id': self.env.user.id
        })
    
    def action_answer(self):
        self.write({
            'state': 'answered',
            'date_answered': fields.Date.today()
        })
    
    def action_close(self):
        self.write({'state': 'closed'})