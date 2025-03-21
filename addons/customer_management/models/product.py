from odoo import models, fields, api

class ProductCategory(models.Model):
    _name = 'khach_hang.product.category'
    _description = 'Danh Mục Sản Phẩm'

    name = fields.Char(string='Tên Danh Mục', required=True)
    description = fields.Text(string='Mô Tả')

class Product(models.Model):
    _name = 'khach_hang.product'
    _description = 'Sản Phẩm'

    name = fields.Char(string='Tên', required=True)
    price = fields.Float(string='Giá', required=True)
    description = fields.Text(string='Mô Tả')
    category_id = fields.Many2one('khach_hang.product.category', string='Danh Mục Sản Phẩm')
    stock_quantity = fields.Integer(string='Số Lượng Tồn Kho', default=0)
    stock_alert_threshold = fields.Integer(string='Ngưỡng Cảnh Báo Tồn Kho', default=10)

    @api.constrains('stock_quantity')
    def _check_stock_alert(self):
        for product in self:
            if product.stock_quantity < product.stock_alert_threshold:
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get('khach_hang.product').id,
                    'res_id': product.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_warning').id,
                    'summary': f'Cảnh Báo Tồn Kho Thấp: {product.name}',
                    'note': f'Số lượng tồn kho ({product.stock_quantity}) dưới ngưỡng cảnh báo ({product.stock_alert_threshold}).',
                    'user_id': self.env.user.id,
                })