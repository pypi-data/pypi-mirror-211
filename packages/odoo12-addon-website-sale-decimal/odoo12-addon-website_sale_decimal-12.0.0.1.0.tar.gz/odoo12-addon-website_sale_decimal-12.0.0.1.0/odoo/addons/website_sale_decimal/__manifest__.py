{
    'name': 'Website Sale Decimal',
    'version': '12.0.0.1.0',
    'author': 'Coopdevs SCCL',
    'category': 'Website',
    'summary': 'Allow decimal quantities in the website sale module',
    'description': """
This addon changes the parseInt function to parseFloat in the website_sale module, allowing decimal quantities in the cart.
    """,
    'depends': ['website_sale'],
    'data': [
        'views/assets.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,

}
