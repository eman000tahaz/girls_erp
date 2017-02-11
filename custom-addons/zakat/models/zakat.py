# -*- coding: utf-8 -*-
from openerp import api, models, fields, exceptions
from datetime import datetime

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

class LoanName(models.Model):
    _name = "lately.paid.type"

    name = fields.Char('Lately Paid Type')   

class MoneyLate(models.Model):
    _name = 'lately.paid'
    _rec_name = "lately_paid_type_id"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    lately_paid_type_id = fields.Many2one('lately.paid.type', string="Lately Paid")
    pocket_of_money = fields.Float('Money')

class FamilyLoans(models.Model):
    _name = 'family.loan'
    _rec_name = 'community_name'
    
    loan_money = fields.Float('Loan Money')
    case_study_id = fields.Many2one('case.study.request', 'Case No')
    community_name = fields.Char('Community Name')
    monthly_installment = fields.Float('Monthly Installment')


class NeedsType(models.Model):
    _name = 'needs.type'

    name = fields.Char('Name')

class FamilyNeeds(models.Model):
    _name = "family.need" 
    _rec_name = 'need_type_id'
    
    case_study_id = fields.Many2one('case.study.request', 'Case No')
    need_type_id = fields.Many2one('needs.type', string="Name")
    agrees = fields.Selection([('y', 'Yes'), ('N', 'No')], string="Yes/No")
    summery = fields.Text("Summery of Family Needs")

class BranchPlace(models.Model):
    _name = 'branch.place'
    name = fields.Char('Branch')

class CaseClassification(models.Model):
    _name = 'case.classification'
    _rec_name = 'commissary_name'

    case_study_id = fields.Many2one('case.study.request', 'Case No')
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

class CaseCategory(models.Model):
    _name = "case.category"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    name = fields.Char('Name')
    pocket_of_money = fields.Float('Money')

class WomenOpinion(models.Model):
    _name = "women.commission.opinion"
    _rec_name = "needs_type_id"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    opinion = fields.Text('Opinion')
    needs_type_id = fields.Many2one('case.category', string="Type")
    pocket_of_money = fields.Float('Money')
    partner_ids = fields.Many2many('res.partner', string="Members")

class BranchManagementOpinion(models.Model):
    _name = "branch.management.opinion"
    _rec_name = 'case_study_id'
    
    case_study_id = fields.Many2one('case.study.request', 'Case No')
    opinion = fields.Text('Opinion')
    partner_ids = fields.Many2many('res.partner', string="Signature")

class FinalOpinion(models.Model):
    _name = "final.opinion"
    _rec_name = "char_deputy_id"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    opinion = fields.Text('Opinion')
    char_deputy_id = fields.Many2one('res.partner', 'Chairman of the Committee or his deputy')
    first_signature_id = fields.Many2one('res.partner', 'Signature')
    char_deputy1_id = fields.Many2one('res.partner', 'Chairman of the Committee or his deputy')
    Second_signature_id = fields.Many2one('res.partner', 'Signature')


class CaseStudyRequest(models.Model):
    _name = "case.study.request"
    _rec_name = 'date'

    def _opportunity_meeting_phonecall_count(self):
        self.loans_number = 0 
        for each_loan in self.loan_ids:
            self.loans_number += each_loan.loan_money
        return 1
    def _display_meeting_phonecall_count(self):
        self.display_number = 0 
        for each_loan in self.loan_ids:
            self.display_number += each_loan.loan_money
        return 1

    def _display_lately_paid(self):
        self.lately_paid_total = 0
        for each_lately_paid in self.lately_paid_money_ids:
            self.lately_paid_total = each_lately_paid.pocket_of_money
        return 1

    def _compute_total_paid(self):
        self.display_lately_paid_total = 0
        for each_lately_paid in self.lately_paid_money_ids:
            self.display_lately_paid_total = each_lately_paid.pocket_of_money
        return 1


    date = fields.Datetime('Date', default=datetime.now(), translate=True)
    hijri_date = fields.Char('Hijri date')
    family_head = fields.Many2one('res.partner', 'Family Head', translate=True)
    relative_relation = fields.Many2one('relative.relation', 'Relative Relation', translate=True)
    national_id = fields.Char('National ID')
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
    loan_ids = fields.One2many('family.loan', 'case_study_id', 'Loans', translate=True)
    lately_paid_money_ids = fields.One2many('lately.paid', 'case_study_id', 'Lately Paid')
    family_needs_ids = fields.One2many('family.need', 'case_study_id', 'Family Needs')
    case_classification_ids = fields.One2many('case.classification', 'case_classify', 'Case Classification')
    ##family_req_ids = fields.One2many('family.requirement', 'request_id', 'Family requirements', translate=True)
    women_commission_opinion_ids = fields.One2many('women.commission.opinion', 'case_study_id', 'Women Commission Opinion')
    branch_management_opinion_ids = fields.One2many('branch.management.opinion', 'case_study_id', 'Branch Management Opinion')
    final_opinion_ids = fields.One2many('final.opinion', 'case_study_id', 'Final Opinion')
    reject = fields.Char('Reject', default='n')
    state = fields.Selection([
            ('new', 'New'),
            ('approve1', 'First Approve'),
            ('approve2', 'Second Approve'),
            ('approve3', 'Third Approve'),
            ('approve4', 'Approved')
            ],default='new')
    loans_number = fields.Float(compute='_opportunity_meeting_phonecall_count', string="Total")
    display_number = fields.Float(compute='_display_meeting_phonecall_count', string="Total")
    lately_paid_total = fields.Float(compute='_display_lately_paid', string="Total")
    display_lately_paid_total = fields.Float(compute='_compute_total_paid', string="Total")
    ###################################### Logic #######################################
    @api.one
    def approve(self):

        # Group registration user
        if self.env['res.users'].has_group('zakat.group_registration_user'):
            self.write({
                'state': 'approve1'
            })

        # Group Departmental Group
        if self.env['res.users'].has_group('zakat.group_departmental_user'):
            if self.loan_ids:
                self.write({
                    'state': 'approve3'
                })
            else:
                self.write({
                    'state': 'approve2'
                })


        # Group Social Survey
        if self.env['res.users'].has_group('zakat.group_social_survey'):
            self.write({
                'state': 'approve1'
            })

        # Group Central Team
        if self.env['res.users'].has_group('zakat.group_central_team'):
            self.write({
                'state': 'approve4'
            })

    @api.one
    def refuse(self):
        
        # Group registration user
        if self.env['res.users'].has_group('zakat.group_registration_user'):
            self.write({
                'reject': 'y'
            })

        # Group Departmental Group
        if self.env['res.users'].has_group('zakat.group_departmental_user'):
            self.write({
                'state': 'new'
            })

        # Group Social Survey
        if self.env['res.users'].has_group('zakat.group_social_survey'):
            self.write({
                'reject': 'approve1'
            })

        # Group Central Team
        if self.env['res.users'].has_group('zakat.group_central_team'):
            self.write({
                'reject': 'approve1'
            })

    def loans(self):
        print "found"



        
