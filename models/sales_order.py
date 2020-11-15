# -*- coding: utf-8 -*-
import requests
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SolanaSalesOrder(models.Model):
    _inherit = 'sale.order'

    def _get_transaction_id(self):
        for record in self:
            payment = self.env['payment.transaction'].search([('sale_order_id', '=', record.id)], limit=1)
            if payment:
                record.transaction = payment.id
            else:
                record.transaction = False

    # < ------Fields for Model--------------------------------------------------------------------------------------- >

    is_payment_recorded = fields.Boolean('Is the Payment Recorded in this ERP', help='Cryptocurrency transactions need to be recorded and associated with this server for order handling.', default=False)
    transaction=fields.Many2one('payment.transaction',string="Transaction", compute=_get_transaction_id)

    # An order that is submitted, will have a sale order, an associated invoice, a payment, and a payment token
    # check if the payment has been completed, if so mark the payment as done
    def salesorder_payment_sync(self):
        # retrieve all the cryptocurrency payment acquirers
        # TODO search 'is_enabled' '=' True?
        cryptocurrency_payment_acquirers = self.env['payment.acquirer'].search([('is_cryptocurrency', '=', True)])

        for acquirer in cryptocurrency_payment_acquirers:
            # get the transactions recorded on the blockchain
            transactions_snapshot = acquirer.recent_transactions
            _logger.info(f'Transactions found: {transactions_snapshot}')
            self._cr.execute("SELECT payment_transaction.id, sale_order.id, payment_token.id FROM "
                             "payment_transaction, sale_order, sale_order_transaction_rel, "
                             "payment_token WHERE sale_order.is_payment_recorded IS NOT True AND sale_order.state = "
                             "'sent' AND payment_token.id = "
                             "payment_transaction.payment_token_id AND sale_order.id = "
                             "sale_order_transaction_rel.sale_order_id AND payment_transaction.id = "
                             "sale_order_transaction_rel.transaction_id AND payment_transaction.acquirer_id = "
                             f"{acquirer.id}")

            # TODO BUG!!!!! if you're not logged in, this above sql query doesn't return any results!

            for payment_transaction_id, sale_order_id, payment_token_id in self.env.cr.fetchall():
                # expected TO address: acquirer.address
                # expected FROM address: payment_token.name.split('-')[0].strip()
                # expected AMOUNT: sales_order.amount_total
                payment_token = self.env['payment.token'].sudo().browse(payment_token_id)
                sales_order = self.env['sale.order'].sudo().browse(sale_order_id)

                i = 0
                for transaction in transactions_snapshot:
                    # match the decimal place rounding that is done within odoo
                    transaction_amount_rounded = round(transaction['amount'], sales_order.currency_id.decimal_places)

                    _logger.info(f'comparing from address:{transaction["from_address"]}, {payment_token.name.split("-")[0].strip()}')
                    _logger.info(f'comparing to address:{transaction["to_address"]}, {acquirer.address}')
                    _logger.info(f'comparing amount: {transaction_amount_rounded}, {sales_order.amount_total}')

                    matches = 0
                    if transaction['from_address'] == payment_token.name.split('-')[0].strip():
                        matches = matches + 1

                    if transaction['to_address'] == acquirer.address:
                        matches = matches + 2

                    if transaction_amount_rounded == sales_order.amount_total:
                        matches = matches + 4

                    # TODO query to see if any other payment transaction records exist with this transactions tx hash
                    # dependency tx hash must be added as a field to payment.transaction
                    if matches == 7:
                        payment_transaction = self.env['payment.transaction'].sudo().browse(payment_transaction_id)

                        sales_order.write({'is_payment_recorded': True,
                                           'state': 'sale'})
                        payment_transaction.write({'state': 'done'})
                        # TODO write tx id / hash to payment_transaction

                        _logger.info(f'Match found setting sales order to recorded: {sales_order.id}')
                        _logger.info(f'Match found setting sales order to recorded: {payment_transaction.id}')

                        # match found, delete it from the transaction snapshot,
                        # so it doesn't get attribute to another order from the same customer
                        del transactions_snapshot[i]
                        break
                    else:
                        i = i + 1
                        if matches == 1:
                            _logger.info('Only the from address matched')
                        if matches == 2:
                            _logger.info('Only the to address matched')
                        if matches == 3:
                            # TODO add message to sales order with a link to the block explorer
                            #  stating that this tx could be associated with the transactions,
                            #  but the buyer didn't have the right amount
                            #   manual payment will have to be registered or manual refund if too much
                            _logger.info('Only the to and from address matched')
                        if matches == 4:
                            _logger.info('Only the amount matched')
                        if matches == 5:
                            _logger.info('Only the from address and the amount matched')
                        if matches == 6:
                            _logger.info('Only the to address and amount matched')

                # TODO cancel the order if it hasn't been recorded on the blockchain yet
