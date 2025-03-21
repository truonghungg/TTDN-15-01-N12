from odoo import models, fields, api

class Customer(models.Model):
    _name = 'khach_hang.customer'
    _description = 'Khách Hàng'

    name = fields.Char(string='Tên', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Điện Thoại')
    address = fields.Text(string='Địa Chỉ')
    order_ids = fields.One2many('khach_hang.order', 'customer_id', string='Đơn Hàng')
    feedback_ids = fields.One2many('khach_hang.feedback', 'customer_id', string='Phản Hồi')
    care_activity_ids = fields.One2many('khach_hang.care_activity', 'customer_id', string='Hoạt Động Chăm Sóc')
    order_count = fields.Integer(
        string='Số Đơn Hàng',
        compute='_compute_order_count',
        store=True  # Thêm store=True để lưu trữ giá trị
    )

    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)