# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    @api.multi
    def _get_flattened_totals(self, factor=1, totals=None):
        """
        Generate a summary of product quantities as a dict of flattened BOM
        """
        self.ensure_one()
        if totals is None:
            totals = {}
        # TODO: product or product template?
        factor /= self.product_uom._compute_quantity(
            self.product_qty, self.product_tmpl_id.uom_id, round=False)
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product=line.product_id)
            if sub_bom:
                new_factor = factor * line.product_uom._compute_quantity(
                    line.product_qty, line.product_id.uom_id, round=False)
                sub_bom._get_flattened_totals(new_factor, totals)
            else:
                if totals.get(line.product_id):
                    totals[line.product_id] += \
                        line.product_uom._compute_quantity(
                    line.product_qty, line.product_id.uom_id, round=False)
                else:
                    totals[line.product_id] = \
                        line.product_uom._compute_quantity(
                    line.product_qty, line.product_id.uom_id, round=False)
        return totals
