# customer_management/controllers/main.py
from odoo import http
from odoo.http import request

class CustomerManagementController(http.Controller):

    @http.route('/customer_management/customers', type='json', auth='user')
    def get_customers(self):
        customers = request.env['cm.customer'].search([])
        return customers.read(['name', 'email', 'phone'])

    @http.route('/customer_management/orders', type='json', auth='user')
    def get_orders(self):
        orders = request.env['cm.order'].search([])
        return orders.read(['customer_id', 'order_date', 'total_amount'])