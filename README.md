Solana Payment Acquirer for Odoo Ecommerce
====================

![Solana](https://raw.githubusercontent.com/t-900-a/odoo-solana-payments/master/static/src/img/solanasol_icon.png)
![Odoo Ecommerce](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimages.g2crowd.com%2Fuploads%2Fproduct%2Fimage%2Fsocial_landscape%2Fsocial_landscape_1489710415%2Fodoo-ecommerce.png&f=1&nofb=1)

Allows you to accept a variety of currencies (USDT, USDC, BTC, SOL) via the solana blockchain

A payment module for handling SPL tokens and native SOL transactions in the context of the Odoo Ecommerce platform

Utilizes the public Solana blockchain to enable the acceptance of a variety of currencies.
USDT / USDC are native on Solana, while BTC, ETH and other BIP44 coin types are wrapped onto Solana. 
Transactions are instant and less than a penny.

* release 0.2
* open source: https://github.com/t-900-a/odoo-solana-payments/
* Solana is a Web-Scale Blockchain
* works with Odoo 14.0
* detailed configuration guide yet to come

Copyrights
----------

GNU General Public License v3.0
https://github.com/t-900-a/odoo-solana-payments/blob/master/LICENSE

Demo Website
----------

Site: http://solanashop.mooo.com/

Demo Video: https://siasky.net/AABOhlJI929pKrie_EP5x9IzmeDWax86wSDnpQSzWtjO-w

![SolanaShop](https://siasky.net/PADuTEMjZiigfoHy5sJXDCg-mAS63PPsXFxYNL7S95V2NA)

Installation Notes
----------
Requires these Odoo modules:
                'website_sale',
                'website_payment',
                'website',
                'payment_transfer',
                'payment',
                'base_setup',
                'web',
                
Install this module.

Add your wallet address and / or alias: Website > Configuration > Payment Acquirers > Edit

At this time this module is not recommended for use in production, but if you feel comfortable with the risks; set the state from Test Mode to Enabled and the Environment from Devnet to Mainnet.

Under website settings > Pricing > check both "Pricelists" (Multiple prices per product) and "Multi-Currencies"

SOL is added to your currencies available in Odoo, if you want to add SPL tokens (i.e. USDC) you will need to add them.

The USD/SOL rate is manually set via Settings / Currencies.

After you've added an SPL token as a currency, you need to create a copy of the Solana Payment Acquirer.

This can be done: Website > Configuration > Payment Acquirers > Action > Duplicate

Customize your Wallet Address / Alias under each payment acquirer that you create.


Each currency will require a pricelist, Create a Pricelist and mark it as selectible.

Set the price computation to "Sales Price" and "Formula", you can add discounts to incentivize the use of a certain token.

At this time they need to match their price list to their payment method. I.e. if they're going to pay with SPL BTC, then the drop down for the BTC price list needs to be selected.


Once this is all done, your site visitors can change currencies to their preferred currency and can pay via Solana. 
Requests will be made to an external solana api to confirm payments are made and the sales order and payments will be marked as paid/complete.


Want to help?
-------------

There are a bunch of TODOs that need looked at.

The code should have unit tests, but doesn't due to the time constraints of the hackathon.


Development
-----------

Install odoo: https://github.com/Yenthe666/InstallScript

Pull the repo down to your odoo custom addons folder.

Install the module and test.


Thanks to
-----------------
![CryptoHO.ST](https://cryptoho.st/images/cryptohost_logo_sized.3.png)


Fast and reliable VPS store. Accepting Monero, Bitcoin, Lightning Network, Litecoin and Dash.

https://cryptoho.st/
