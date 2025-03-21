{
    'name': "Quản Lý Khách Hàng",
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Module quản lý khách hàng, sản phẩm, đơn hàng và chăm sóc khách hàng',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/customer_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/feedback_view.xml',
        'views/potential_customer_views.xml',
        'views/product_category_views.xml',
        'views/care_views.xml',
    ],
    'installable': True,
    'application': True,
}