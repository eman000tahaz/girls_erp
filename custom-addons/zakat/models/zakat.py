# -*- coding: utf-8 -*-
from openerp import api, models, fields, exceptions, _
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
    unit_of_help = fields.Char('Unit')


class FamilyNeeds(models.Model):
    _name = "family.need" 
    _rec_name = 'need_type_id'
    # Is Admin
    def _is_admin(self):
        if self.env['res.users'].has_group('zakat.group_admin'):
            self.is_admin = True
        else:
            self.is_admin = False
        return self.is_admin
    
    case_study_id = fields.Many2one('case.study.request', 'Case Study')
    need_type_id = fields.Many2one('needs.type', string="Name")
    agrees = fields.Selection([('y', 'Yes'), ('N', 'No')], string="Yes/No", default='y')
    frequency_help = fields.Selection([('m', 'Monthly'), ('y', 'Yearly')])
    selecting_date_from = fields.Date('Selecting date from')
    selecting_date_to = fields.Date('Selecting date to')
    dispatch_date_from = fields.Date('Dispatch Date from')
    dispatch_date_to = fields.Date('Dispatch Date to')
    value = fields.Float('Value')
    summery = fields.Text("Summery of Family Needs")
    is_admin = fields.Boolean(compute='_is_admin', string="Is Admin?")
    approve = fields.Boolean(string="Approve")
    is_recieve = fields.Boolean(string="Is Recieved?")
    colorize = fields.Boolean(string="Color")

    @api.one
    def confirm(self):
        if self.dispatch_date_from == str(datetime.now().date()):
            self.is_recieve = True
            self.colorize = False
        else:
            raise exceptions.Warning(_("You don't determine the date to recieve or it is not the date"))
    # Automation action
    @api.v7
    def update_family_need(self, cr, uid, context=None):
        family_need_obj = self.pool.get('family.need')
        get_f_n_obj = self.pool.get('family.need').search(cr, uid, [])
        get_f_n_browse = self.pool.get('family.need').browse(cr, uid, get_f_n_obj)
        for get_each_data in get_f_n_browse:
            if get_each_data.dispatch_date_from and get_each_data.is_recieve == False and get_each_data.approve == True:
                if get_each_data.dispatch_date_from == str(datetime.now().date()):
                    get_each_data.write({'colorize': True})



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
    pocket_of_money = fields.Float('Money Less than')

class WomenOpinion(models.Model):
    _name = "women.commission.opinion"
    _rec_name = "needs_type_id"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    opinion = fields.Text('Opinion',required=True)
    needs_type_id = fields.Many2one('case.category', string="Type")
    pocket_of_money = fields.Float('Money')
    partner_ids = fields.Many2many('res.partner', string="Members")

class BranchManagementOpinion(models.Model):
    _name = "branch.management.opinion"
    _rec_name = 'case_study_id'
    
    case_study_id = fields.Many2one('case.study.request', 'Case No')
    opinion = fields.Text('Opinion',)
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

    # Is Admin
    @api.one
    def _is_admin(self):
        if self.env['res.users'].has_group('zakat.group_admin'):
            self.is_admin = True
        else:
            self.is_admin = False
        return self.is_admin

    # Is Registration user
    def _is_registration_user(self):
        if self.env['res.users'].has_group('zakat.group_registration_user'):
            self.is_registration_user = True
        else:
            self.is_registration_user = False
        return self.is_registration_user


    date = fields.Datetime('Date', default=datetime.now(), translate=True)
    hijri_date = fields.Char('Hijri date', default="dd/mm/yyyy")
    family_head = fields.Char(string='Family Head', translate=True)
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
    wife_name = fields.Char()
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
    admin_comment = fields.Text('Admin Comment')
    is_admin = fields.Boolean(compute='_is_admin', string="Is Admin?", default="_is_admin")
    is_registration_user = fields.Boolean(compute='_is_registration_user', string="Is Registration")
    ###################################### Logic #######################################
    @api.v7
    def approve(self, cr, uid, ids, context=None):
        case_obj = self.pool.get('case.study.request')
        users_obj = self.pool.get('res.users').search(cr, uid, [])
        users_bro = self.pool.get('res.users').browse(cr, uid, users_obj)
        partner_ids = []
        
        # Group registration user
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_registration_user'):
            case_obj.write(cr, uid, ids,{
                'state': 'approve1'
            })
            for each_user in users_bro:
                print each_user, users_bro
                if self.pool.get('res.users').has_group(cr, each_user.id, 'zakat.group_departmental_user'):
                    partner_ids.append(each_user.partner_id.id)

            # Send Notidication to Departmental that has new rewuest 
        
        # Group Departmental Group
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_departmental_user'):
            get_record_data = self.pool.get('case.study.request').browse(cr, uid, ids[0])
            if get_record_data.women_commission_opinion_ids:
                case_obj.write(cr, uid, ids[0], {
                    'state': 'approve3'
                })
            else:
                case_obj.write(cr, uid, ids[0], {
                    'state': 'approve2'
                })


        # Group Social Survey
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_social_survey'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve1'
            })

        # Group Central Team
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_central_team'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve4'
            })
        if partner_ids:
            post_vars = {'subject': "New Case Need to approve",
                 'body':("You have new case study which needs to approve"),
                 'partner_ids': partner_ids,}  
            thread_pool = self.pool.get('mail.thread')
            thread_pool.message_post(cr, uid,
                            False,
                            type="notification",
                            subtype="mt_comment",
                            context=context,
                            **post_vars)

        
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

    # Admin Approve all needs
    @api.one
    def approve_all_needs(self):
        print self.family_needs_ids
        for each_need in self.family_needs_ids:
            each_need.write({
                'approve': True
            })



        
