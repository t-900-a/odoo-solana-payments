<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <data>

        <template id="solana_payment_confirmation" inherit_id="website_sale.payment_confirmation_status">
            <xpath expr="//*[@class='card-header']" position="inside">
                <t t-if="payment_tx_id.acquirer_id.is_cryptocurrency == True and payment_tx_id.acquirer_id.address and payment_tx_id.state == 'pending'">
                    <p>Payment should be made to
                        <ul>
                            <b>
                                <li style="clear: both;">
                                    Address: <t t-raw="payment_tx_id.acquirer_id.address"/>
                                </li>
                            </b>
                            <t t-if="payment_tx_id.acquirer_id.address_alias != ''">
                                <li style="clear: both;">
                                    <b>
                                        Address Alias: <t t-raw="payment_tx_id.acquirer_id.address_alias"/>
                                    </b>
                                </li>
                            </t>
                        </ul>
                    </p>
                </t>
                <!--   TODO pay with web wallet: https://www.sollet.io/          -->
                <!--    TODO enable the user to accept the payment in their web wallet         -->
                <!--    TODO add barcode: accept the payment via their mobile wallet         -->
                <!--    payment_tx_id.acquirer_id.qr_code?      -->
            </xpath>
        </template>

    </data>
</odoo>
