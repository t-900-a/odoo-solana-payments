# -*- coding: utf-8 -*-
import base64
from odoo import models, fields
from odoo.exceptions import MissingError
from solana._layouts.system_instructions import SYSTEM_INSTRUCTIONS_LAYOUT, InstructionType as SOLInstructionType
from solana.rpc.api import Client
from solana.system_program import TransferParams as SOLTransferParams
from solana.system_program import decode_transfer as sol_decode_transfer
from solana.transaction import Transaction, TransactionInstruction
from spl.token._layouts import INSTRUCTIONS_LAYOUT, InstructionType as SPLInstructionType
from spl.token.instructions import TransferParams as SPLTransferParams
from spl.token.instructions import decode_transfer as spl_decode_transfer
import logging

_logger = logging.getLogger(__name__)

class SolanaPaymentAcquirer(models.Model):
    """
    Inherits from payment.acquirer
    Custom fields added: is_cryptocurrency, environment, address, types, address alias
    """
    _inherit = 'payment.acquirer'
    _recent_transactions = []

    provider = fields.Selection(selection_add=[('solana', 'Solana')], ondelete={'solana': 'set default'})

    def _get_providers(self, context=None):
        providers = super(SolanaPaymentAcquirer, self)._get_providers(cr, uid, context=context)
        providers.append(['solana', 'Solana'])
        return providers

    is_cryptocurrency = fields.Boolean('Cryptocurrency?', default=False)
    environment = fields.Selection([('dev', 'Devnet'), ('test', 'Testnet'), ('main', 'Mainnet')], default='dev')
    address = fields.Char(string="Wallet Address", help='The receiving address that you expect to receive payments')
    address_alias = fields.Char(string="Wallet Alias", help='The alias that you have registered for the receiving address')
    # not used right now, could be used to update price data?
    type = fields.Selection([
        ('sol', 'SOL'),
        # TODO        ('btc', 'BTC'),
        # TODO        ('usdt', 'USDT'),
        # TODO        ('usdc', 'USDC'),
        # TODO        ('eth', 'ETH'),
        ('none', 'none')], "none",
        default='none', required=True,
        help='Currently implemented Solana Cryptocurrencies')

    @property
    def recent_transactions(self) -> []:
        solana_transactions = []
        if self.environment == 'dev':
            server = 'https://devnet.solana.com'
        if self.environment == 'test':
            server = 'https://testnet.solana.com'
        if self.environment == 'prod':
            server = 'https://api.mainnet-beta.solana.com'

        solana_client = Client(server)
        if self.address == '':
            raise MissingError(f'Payment provider is not configured: {self._get_providers}')
        _logger.info(f'Checking transactions for Solana address: {self.address}')
        _logger.info(f'result:{solana_client.get_confirmed_signature_for_address2(self.address)}')
        # TODO improve error handing of this section i.e. if an error occurs there is no result
        transactions = solana_client.get_confirmed_signature_for_address2(self.address)["result"]
        for tx in transactions:
            tx_result = solana_client.get_confirmed_transaction(tx_sig=tx["signature"], encoding="base64")

            raw_tx_str = tx_result['result']['transaction'][0]

            raw_tx_base64_bytes = raw_tx_str.encode('ascii')
            raw_tx_bytes = base64.b64decode(raw_tx_base64_bytes)

            des_tx: Transaction = Transaction.deserialize(raw_tx_bytes)
            tx_instruction: TransactionInstruction = des_tx.instructions.pop()
            # program id will be a bunch of ones if it's a transaction involving SOL
            if tx_instruction.program_id.__str__() == "11111111111111111111111111111111":
                if SYSTEM_INSTRUCTIONS_LAYOUT.parse(
                        tx_instruction.data).instruction_type == SOLInstructionType.Transfer:
                    transfer_params: SOLTransferParams = sol_decode_transfer(tx_instruction)
                    solana_transactions.append({'from_address': transfer_params.from_pubkey.__str__(),
                                                'to_address': transfer_params.to_pubkey.__str__(),
                                                'amount': transfer_params.lamports * .000000001})
            # program id will be Token... if it's a transaction involving tokens
            if tx_instruction.program_id.__str__() == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA":
                if INSTRUCTIONS_LAYOUT.parse(tx_instruction.data).instruction_type == SPLInstructionType.Transfer:
                    transfer_params: SPLTransferParams = spl_decode_transfer(tx_instruction)
                    solana_transactions.append({'from_address': transfer_params.source.__str__(),
                                                'to_address': transfer_params.dest.__str__(),
                                                'amount': transfer_params.amount * .000000001})
                    # TODO each token can have it's own decimal place configuration, so ^^^ this multiplication won't work for all tokens

        # TODO add field to keep track of the blockheight that we've already scanned
        # dependency https://github.com/michaelhly/solana-py/issues/44
        # update that field everytime this function is ran
        return solana_transactions

    # < -------------------------------------------------------------------------------------------------------------- >
