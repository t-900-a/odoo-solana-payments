# -*- coding: utf-8 -*-
{
    'name': "odoo-solana-payments",

    'summary': """
        Allows you to accept a variety of currencies (USDT, USDC, BTC, SOL) via the solana blockchain""",

    'description': """
        Payment Acquierer built for Odoo 14; utilizes the public Solana blockchain to enable the acceptance of a variety of currencies.
        USDT / USDC are native on Solana, while BTC, ETH and other BIP44 coin types can be wrapped onto Solana. 
        Transactions are instant and less than a penny.
        Current list of supported tokens / currencies:
            USDC
    """,

    'author': "T-900",
    'website': "http://github.com/t-900-a/odoo-solana-payments",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['website_sale',
                'website_payment',
                'website',
                'payment_transfer',
                'payment',
                'base_setup',
                'web',
                ],

    # always loaded
    'data': [
        'views/scheduler.xml',
        'views/solana_acquirer_form.xml',
        'views/solana_payment_confirmation.xml',
        'data/currency.xml',
        'data/solana_sol_payment_acquirer.xml',
    ],
    # only loaded in demonstration mode
    # TODO add demo data
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'GPL-3',
}