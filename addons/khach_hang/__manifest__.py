{
    'name': 'quan ly khach hang v2',
    'version': '1.0',
    'summary': 'Manage Customers, Products, Orders, Feedback, Potential Customers, and Customer Care',
    'description': 'A comprehensive module to manage customer-related operations.',
    'author': 'hung',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',  
        'views/customer_views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/feedback_view.xml',
        'views/potential_customer_views.xml',
        'views/care_views.xml',
        'views/inquiry_views.xml',
        'views/templates.xml'
    ],
    'installable': True,
    'application': True,
}