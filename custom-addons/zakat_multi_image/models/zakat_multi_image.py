# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class CaseStudyMultiImage(models.Model):
    _name = "case.study.request"
    _inherit = [_name, "base_multi_image.owner"]
