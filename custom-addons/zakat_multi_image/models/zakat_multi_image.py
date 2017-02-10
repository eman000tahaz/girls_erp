# -*- coding: utf-8 -*-

from openerp import api, models, fields, exceptions

class LoanImages(models.Model):
    _name = "family.loan"
    _inherit = [_name, "base_multi_image.owner"]

class CaseStudyMultiImage(models.Model):
    _name = "case.study.request"
    _inherit = [_name, "base_multi_image.owner"]
