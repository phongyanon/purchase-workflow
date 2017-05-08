# -*- coding: utf-8 -*-
#
#
#    Copyright (C) 2012 Ecosoft (<http://www.ecosoft.co.th>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
from openerp.tests.common import TransactionCase


class TestPurchaseIsolatedQuotation(TransactionCase):

    def test_purchase_isolated_quotation(self):
        """
        - New purchase.order will have order_type = 'quotation'
        - When quotation is converted to order
          - Status chagned to 'done'
          - New purchase.order of order_type = 'purchase_order' created
        - Quotation can refer to Order and Order can refer to Quotation
        """
        self.quotation.action_button_convert_to_order()
        self.assertEqual(self.quotation.state, 'done')
        self.purchase_order = self.quotation.order_id
        self.assertEqual(self.purchase_order.order_type, 'purchase_order')
        self.assertEqual(self.purchase_order.state, 'draft')
        self.assertEqual(self.purchase_order.partner_id, self.partner)
        self.assertEqual(self.purchase_order.quote_id, self.quotation)

    def setUp(self):
        super(TestPurchaseIsolatedQuotation, self).setUp()
        self.partner = self.env.ref('base.res_partner_2')
        vals = {'partner_id': self.partner.id,
                'order_type': 'quotation',
                }
        self.quotation = self.env['purchase.order'].create(vals)