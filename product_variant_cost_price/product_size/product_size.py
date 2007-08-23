##############################################################################
#
# Copyright (c) 2005-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################

import datetime
from osv import fields,osv
import pooler

class stock_production_lot(osv.osv):
	_inherit = 'stock.production.lot'
	def _get_size(dtype):
		def calc_date(self, cr, uid, context={}):
			if context.get('product_id', False):
				product = pooler.get_pool(cr.dbname).get('product.product').browse(cr, uid, [context['product_id']])[0]
				duree = getattr(product, dtype) or 0
				return duree
			else:
				return False
		return calc_date

	_columns = {
		'width': fields.float('Width'),
		'length': fields.float('Length'),
		'thickness': fields.float('Thickness'),
	}
	_defaults = {
		'width': _get_size('width'),
		'length': _get_size('length'),
		'thickness': _get_size('thickness'),
	}
	def name_get(self,cr, uid, ids, context):
		if not len(ids):
			return []
		res = [(r['id'], (r['name'] or '') + ' ('+str(int(r['width']))+','+str(int(r['length']))+','+str(int(r['thickness']))+')') for r in self.read(cr, uid, ids, ['name','width','length','thickness'], context)]
		return res
stock_production_lot()

class product_product(osv.osv):
	_inherit = 'product.product'
	_columns = {
		'width': fields.float('Width'),
		'length': fields.float('Length'),
		'thickness': fields.float('Thickness'),
	}
product_product()

class sale_order(osv.osv):
	_inherit = 'sale.order.line'
	_columns = {
		'prodlot_id' : fields.many2one('stock.production.lot', 'Production lot', help="Production lot is used to put a serial number on the production"),
	}
sale_order()
