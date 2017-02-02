# -*- coding: utf-8 -*-

from openerp import api, models, fields, exceptions
from datetime import datetime

class CaseStudyRequest(models.Model):
    _name = "case.study.request"
    _rec_name = 'date'

    date = fields.Datetime('Date', default=datetime.now(), translate=True)
    hijri_date = fields.Char('Hijri date')
    family_head = fields.Many2one('res.partner', 'Family Head', translate=True)
    relative_relation = fields.Many2one('relative.relation', 'Relative Relation', translate=True)
    work_place = fields.Many2one('work.place', 'Work Place', translate=True)
    job = fields.Char('Job', translate=True)
    mobile = fields.Char('Mobile', translate=True)
    fh_state = fields.Selection([('employee', 'Employee'),
                                 ('retired', 'Retired'),
                                 ('helpless', 'Helpless'),
                                 ('jailed', 'Jailed'),
                                 ('dead', 'Dead'),
                                 ('unemployed' , 'Unemployed'),
                                 ('other' , 'Other')], 'Family Head State', translate=True)
    fh_state_desc = fields.Text(string='Description')
    salary = fields.Float('Salary', translate=True)
    pension = fields.Float('Pension', translate=True)
    rents = fields.Float('Rents', translate=True)
    other = fields.Float('Other Salary', translate=True)
    account_no = fields.Char('Bank Account Number', translate=True)
    bank_name = fields.Char('Bank Name', translate=True)
    wife_name = fields.Many2one('res.partner', domain=[('sex', '=', 'female')], translate=True)
    wife_mobile = fields.Char('Wife Mobile', translate=True)
    address = fields.Char('Address', translate=True)
    family_state = fields.Many2one('family.state', translate=True)
    housing = fields.Many2one('housing', 'Housing State', translate=True)
    loan_ids = fields.One2many('family.loan', 'name', 'Loans', translate=True)
    lately_paid_money = fields.One2many('lately.paid', 'name', 'Lately Paid')
    family_needs = fields.One2many('family.need', 'name', 'Family Needs')
    case_classification_ids = fields.One2many('case.classification', 'case_classify', 'Case Classification')
    ##family_req_ids = fields.One2many('family.requirement', 'request_id', 'Family requirements', translate=True)

class RelativeRlation(models.Model):
    _name = 'relative.relation'

    name = fields.Char('Name', translate=True)

class WorkPlace(models.Model):
    _name = 'work.place'

    name = fields.Char('Name', translate=True)

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'sex'

    sex = fields.Selection([('male', 'Male'), ('female', 'Female')], 'Sex', translate=True)

class FamilyState(models.Model):
    _name = 'family.state'

    name = fields.Char('State Name', translate=True)
    persons_lived_in = fields.Integer('Individuals Who lived in House', translate=True)
    persons_lived_out = fields.Integer('Individuals Who Not lived in House', translate=True)

class FamilyHousing(models.Model):
    _name = 'housing'
    _rec_name = 'type'

    # state = fields.Selection([(),
    #                          ()])
    type = fields.Char('Type')
    rooms = fields.Integer('Number of Rooms', translate=True)

class MoneyLate(models.Model):
    _name = 'lately.paid'

    name = fields.Many2one('lately.paid.type')
    pocket_of_money = fields.Float('Money')

class FamilyLoans(models.Model):
    _name = 'family.loan'

    name = fields.Char('Loan Money')
    community_name = fields.Char('Community Name')
    monthly_installment = fields.Float('Monthly Installment')

class LoanName(models.Model):
    _name = "lately.paid.type"

    name = fields.Char('Lately Paid Type')   

class FamilyNeeds(models.Model):
    _name = "family.need" 
    
    name = fields.Many2one('needs.type')
    agrees = fields.Selection([('y', 'Yes'), ('N', 'No')], string="Yes/No")
    summery = fields.Text("Summery of Family Needs")

class NeedsType(models.Model):
    _name = 'needs.type'

    name = fields.Char('Name')

class CaseClassification(models.Model):
    _name = 'case.classification'
    _rec_name = 'commissary_name'

    total_income = fields.Float(string='Total Income')
    net_income = fields.Float(string='Net Income')
    each_person_share = fields.Float(string='Each One Share')
    case_classify =  fields.Text('Case Classification')
    expense = fields.Float(string='Expense')
    commissary_name = fields.Many2one('res.partner')
    commissary_phone = fields.Char()
    branch = fields.Many2one('branch.place')
    f_researcher_name = fields.Many2one('res.partner', string="First Researcher Name")
    s_researcher_name = fields.Many2one('res.partner', string="Second Researcher Name")


class BranchPlace(models.Model):
    _name = 'branch.place'
    name = fields.Char('Branch')
        
