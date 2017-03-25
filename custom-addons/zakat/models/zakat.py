# -*- coding: utf-8 -*-
from openerp import api, models, fields, exceptions, _, osv
from datetime import datetime
from umalqurra.hijri_date import HijriDate


class RelativeRlation(models.Model):
    _name = 'relative.relation'

    name = fields.Char('صلة القرابة بالأسرة')
    #check_user = fields.Integer(default="0")

class FamilyHeadStatus(models.Model):
    _name = 'family.head'
    name = fields.Char('حالة رب الاسرة')

class WorkPlace(models.Model):
    _name = 'work.place'

    name = fields.Char('جهة العمل')
    #check_user = fields.Integer(default="0")

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'sex'

    sex = fields.Selection([('male', 'ذكر'), ('female', 'أنثى')], 'Sex')
    #check_user = fields.Integer(default="0")

class FamilyState(models.Model):
    _name = 'family.state'

    name = fields.Char('حالة الأسرة')
    #check_user = fields.Integer(default="0")
    
class FamilyHousing(models.Model):
    _name = 'housing'
    _rec_name = 'type'

    # state = fields.Selection([(),
    #                          ()])
    type = fields.Char('Type')
    rooms = fields.Integer('Number of Rooms')
    #check_user = fields.Integer(default="0")

class HousingType(models.Model):
    _name = 'housing.type'

    name = fields.Char('نوع السكن')
    #check_user = fields.Integer(default="0")

class HousingState(models.Model):
    _name = 'housing.state'

    name = fields.Char('حالة المسكن')
    #check_user = fields.Integer(default="0")

class FamilyAddress(models.Model):
    _name = 'family.address'

    name = fields.Char('المدينة')
    #check_user = fields.Integer(default="0")

class LoanName(models.Model):
    _name = "lately.paid.type"

    name = fields.Char('نوع المبلغ المتأخر')   

class MoneyLate(models.Model):
    _name = 'lately.paid'
    _rec_name = "lately_paid_type_id"

    case_study_id = fields.Many2one('case.study.request', 'رقم الحالة')
    lately_paid_type_id = fields.Many2one('lately.paid.type', string="الأسم")
    pocket_of_money = fields.Integer('المبلغ')
    #check_user = fields.Integer(default="0")

class FamilyLoans(models.Model):
    _name = 'family.loan'
    _rec_name = 'community_name'

    loan_money = fields.Integer('مبلغ القرض')
    case_study_id = fields.Many2one('case.study.request', 'رقم الحالة')
    community_name = fields.Char('اسم الجهة')
    monthly_installment = fields.Integer('القسط الشهري')
    image = fields.Binary('المستند')
    #check_user = fields.Integer(default="0")

class NeedsType(models.Model):
    _name = 'needs.type'

    name = fields.Char('الاسم')
    unit_of_help = fields.Char('الوحدة')
    #check_user = fields.Integer(default="0")

class EductionLearn(models.Model):
    _name = 'eduction.learn'
    name = fields.Char('الحالة التعليمية')


class FamilyData(models.Model):
    _name = 'family.member'

    name = fields.Char('الاسم الثلاثى مع القبيلة')
    relative_relation = fields.Many2one('relative.relation', string="صلة القرابة")
    birthday_date = fields.Date('تاريخ الميلاد')
    educ_state = fields.Many2one('eduction.learn', string="الحالة التعليمية")
    description = fields.Text('ملاحظة')
    case_study_id = fields.Many2one('case.study.request', 'Case Study')
    image = fields.Binary('المستند')


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
    
    case_study_id = fields.Many2one('case.study.request', 'دراسة الحالة')
    need_type_id = fields.Many2one('needs.type', string="المساعدات المطلوبة")
    frequency_help = fields.Selection([('m', 'شهريا'), ('y', 'سنويا')])
    selecting_date_from = fields.Date('وقت الاختيار من')
    selecting_date_to = fields.Date('وقت الاختيار الى')
    dispatch_date_from = fields.Date('موعد التسلم من')
    dispatch_date_to = fields.Date('موعد التسليم الى')
    value = fields.Integer('القيمة')
    summery = fields.Text("ملاحظات")
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

    case_study_id = fields.Many2one('case.study.request', 'الحالة')
    total_income = fields.Integer(string='إجمالي الدخل')
    net_income = fields.Integer(string='صافي الدخل')
    each_person_share = fields.Integer(string='نصيب كل فرد')
    case_classify =  fields.Text('تصنيف الحالة')
    expense = fields.Integer(string='إجمالي المصاريف')
    commissary_name = fields.Many2one('res.partner', string='اسم المندوب')
    commissary_phone = fields.Char('رقم الهاتف')
    branch = fields.Many2one('branch.place',string="الفرع")
    f_researcher_name = fields.Many2one('res.partner', string="اسم الباحث الأول")
    s_researcher_name = fields.Many2one('res.partner', string="اسم الباحث الثاني")

class CaseCategory(models.Model):
    _name = "case.category"

    case_study_id = fields.Many2one('case.study.request', 'Case No')
    name = fields.Char('اسم الفئة')
    pocket_of_money = fields.Integer('المبلغ أقل من')

class WomenOpinion(models.Model):
    _name = "women.commission.opinion"
    _rec_name = "needs_type_id"

    case_study_id = fields.Many2one('case.study.request', 'الحالة')
    opinion = fields.Text('التعليق',required=True)
    needs_type_id = fields.Many2one('case.category', string="النوع")
    pocket_of_money = fields.Integer('نفقات أخرى')
    check_user = fields.Integer(default="0")
    #partner_ids = fields.Many2many('res.partner', string="الأعضاء")

class BranchManagementOpinion(models.Model):
    _name = "branch.management.opinion"
    _rec_name = 'case_study_id'
    
    case_study_id = fields.Many2one('case.study.request', 'الحالة')
    opinion = fields.Text('رأى مدير الفرع')
    check_user = fields.Integer(default="0")
    #partner_ids = fields.Many2many('res.partner', string="التوقيع")

class FinalOpinion(models.Model):
    _name = "final.opinion"
    _rec_name = "char_deputy_id"

    case_study_id = fields.Many2one('case.study.request', 'الحالة')
    opinion = fields.Text('رأى اللجنة النهائية')
    char_deputy_id = fields.Many2one('res.partner', 'رئيس اللجنة أو نائبه')
    first_signature_id = fields.Many2one('res.partner', 'توقيع')
    char_deputy1_id = fields.Many2one('res.partner', 'رئيس اللجنة أو نائبه')

    #Second_signature_id = fields.Many2one('res.partner', 'توقيع')

class Documentation(models.Model):
    _name = "documentation"

    name = fields.Char('اسم المستند')
    image = fields.Binary('المستند')
    case_study_id = fields.Many2one('case.study.request')


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
            self.lately_paid_total += each_lately_paid.pocket_of_money
        return 1

    def _compute_total_paid(self):
        self.display_lately_paid_total = 0
        for each_lately_paid in self.lately_paid_money_ids:
            self.display_lately_paid_total += each_lately_paid.pocket_of_money
        return 1

    def _total_number_family(self):
        self.total_number_family = 0
        for each_member in self.family_member_ids:
            if each_member:
                self.total_number_family += 1
        return 1

    def  _total_income(self):
        self.total_income = self.other + self.salary + self.pension + self.rents
        self.salary_total = self.total_income
        return 1
    def _get_hijra(self):
        um = HijriDate(datetime.now().year,datetime.now().month,datetime.now().day,gr=True)
        self.hijri_date = str(int(um.day)) + "/" + str(int(um.month))+"/"+ str(int(um.year))

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


    date = fields.Datetime('التاريخ الميلادى', default=datetime.now())
    hijri_date = fields.Char(string="التأريخ")
    family_head = fields.Char(string='اسم رب الأسرة')
    relative_relation = fields.Many2one('relative.relation', 'صلة القرابة بالأسرة')
    national_id = fields.Char('الرقم المدنى')
    work_place = fields.Char('جهة العمل')
    job = fields.Char('الوظيفة')
    mobile = fields.Char('الهاتف')
    fh_state = fields.Many2one('family.head',string='حالة رب الأسرة')
    fh_state_desc = fields.Text(string='حالة رب الأسرة')
    salary = fields.Integer('الراتب')
    pension = fields.Integer('راتب تقاعد ')
    rents = fields.Integer('إيجارات')
    other = fields.Integer('أخرى')
    salary_total = fields.Integer(compute='_total_income',string="المجموع")
    account_no = fields.Char('Bank Account Number')
    bank_name = fields.Char('Bank Name')
    wife_name = fields.Char('اسم الزوجة')
    wife_mobile = fields.Char('رقم هاتف الزوجة')
    address = fields.Many2one('family.address', 'العنوان الدائم')
    family_state = fields.Many2one('family.state', string='حالة الأسرة')
    persons_lived_in = fields.Integer('عدد أفراد الأسرة الساكنين بالمنزل')
    persons_lived_out = fields.Integer('عدد أفراد الأسرة الذين لا يسكنون مع الأسرة')
    housing_state = fields.Many2one('housing.state', string="حالة المسكن")
    other_state = fields.Char('اخرى')
    state_type = fields.Many2one('housing.type', 'نوع السكن')
    rooms = fields.Integer('عدد الغرف')
    loan_ids = fields.One2many('family.loan', 'case_study_id', 'القروض')
    lately_paid_money_ids = fields.One2many('lately.paid', 'case_study_id', 'المبالغ المتأخرة')
    family_needs_ids = fields.One2many('family.need', 'case_study_id', 'متطلبات الأسرة')
    case_classification_ids = fields.One2many('case.classification', 'case_classify', ' تصنيف الحالة')
    ##family_req_ids = fields.One2many('family.requirement', 'request_id', 'Family requirements', translate=True)
    women_commission_opinion_ids = fields.One2many('women.commission.opinion', 'case_study_id', 'راى الباحث الاجتماعى')
    branch_management_opinion_ids = fields.One2many('branch.management.opinion', 'case_study_id', ' رأي إدارة الفرع')
    final_opinion_ids = fields.One2many('final.opinion', 'case_study_id', 'التقرير النهائي للجنة')
    family_member_ids = fields.One2many('family.member', 'case_study_id', 'أفراد العائلة')
    documentation_ids = fields.One2many('documentation', 'case_study_id', 'المستند')
    reject = fields.Char('Reject', default='n')
    state = fields.Selection([
            ('new', 'New'),
            ('approve1', 'First Approve'),
            ('approve2', 'Second Approve'),
            ('approve3', 'Third Approve'),
            ('approve4', 'Forth Approve'),
            ('approve5', 'Approved')
            ],default='new')
    loans_number = fields.Integer(compute='_opportunity_meeting_phonecall_count', string="Total")
    display_number = fields.Integer(compute='_display_meeting_phonecall_count', string="Total")
    lately_paid_total = fields.Integer(compute='_display_lately_paid', string="Total")
    display_lately_paid_total = fields.Integer(compute='_compute_total_paid', string="Total")
    total_number_family = fields.Integer(compute='_total_number_family', string="عدد أفراد الأسرة")
    total_income = fields.Integer(compute='_total_income', string="الدخل‬ ‫اجمالي‬")
    admin_comment = fields.Text('تعليق الادمن')
    is_admin = fields.Boolean(compute='_is_admin', string="Is Admin?", default="_is_admin")
    is_registration_user = fields.Boolean(compute='_is_registration_user', string="Is Registration")
    case_state = fields.Char('حالة الطلب', default="طلب جديد")
    check_user = fields.Integer(default="0")
    branch_management = fields.Integer(default="0")
    social_department = fields.Integer(default="0")
    central_department = fields.Integer(default="0")
    delay_requests = fields.Integer(default="0")
    ###################################### Logic # ######################################

    @api.v7
    def approve(self, cr, uid, ids, context=None):
        case_obj = self.pool.get('case.study.request')
        users_obj = self.pool.get('res.users').search(cr, uid, [])
        users_bro = self.pool.get('res.users').browse(cr, uid, users_obj)
        partner_ids = []
        
        # Group registration user
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_registration_user'):

            case_obj.write(cr, uid, ids,{
                'state': 'approve1',
                'case_state': 'لاعتماد الحالة',
                'check_user' : 1 ,
                'branch_management': 1 ,
            })
            for each_user in users_bro:
                print each_user, users_bro
                if self.pool.get('res.users').has_group(cr, each_user.id, 'zakat.group_departmental_user'):
                    partner_ids.append(each_user.partner_id.id)
            domain = [('state','=','new'), ('reject', '=', 'n')]
            # Send Notidication to Departmental that has new rewuest 
        
        # Group Departmental Group
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_departmental_user'):
            get_record_data = self.pool.get('case.study.request').browse(cr, uid, ids[0])
            if get_record_data.women_commission_opinion_ids:
                case_obj.write(cr, uid, ids[0], {
                    'state': 'approve3',
                    'case_state': 'للمراجعة النهائية',
                    'central_department': 1
                })
            else:
                case_obj.write(cr, uid, ids[0], {
                    'state': 'approve2',
                    'case_state': 'للبحث الاجتماعي',
                    'social_department': 1 
                })
            domain = [('state','=','approve1'), ('reject', '=', 'n')]

        # Group Social Survey
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_social_survey'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve1',
                'case_state': 'لاعتماد البحث الاجتماعي',
                'branch_management': 1
            })
            domain = [('state','=','approve2'), ('reject', '=', 'n')]

        # Group Central Team
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_central_team'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve4',
                'case_state': 'للموافقة النهائية'
            })
            domain = [('state','=','approve3'), ('reject', '=', 'n')]

        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_finial_decision_team'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve5',
                'case_state': 'تمت الموافقة'
            })
            domain = [('state','=','approve4'), ('reject', '=', 'n')]

        # Group Admin Team
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_admin'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve4',
                'case_state': 'تمت الموافقة النهائية عليه'
            })
            domain = [('state','=','approve4'), ('reject', '=', 'n')]

        if partner_ids:
            post_vars = {'subject': "طلبات جديدة",
                 'body':("هناك طلبات تحتاج الى موافقة"),
                 'partner_ids': partner_ids,}  
            thread_pool = self.pool.get('mail.thread')
            thread_pool.message_post(cr, uid,
                            False,
                            type="notification",
                            subtype="mt_comment",
                            context=context,
                            **post_vars)
        
        model_obj = self.pool.get('ir.model.data')
        data_id = model_obj._get_id(cr, uid, 'zakat', 'view_zakat_tree')
        view_id = model_obj.browse(cr, uid, data_id).res_id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'case.study.request',
            'view_mode' : 'tree',
            'domain': domain,
            'nodestroy' : True,
        }
        
    @api.v7
    def refuse(self, cr, uid, ids,context=None):
        
        # Group registration user
        case_obj = self.pool.get('case.study.request')
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_registration_user'):
            case_obj.write(cr, uid, ids[0], {
                'reject': 'y'
            })
            domain = [('state','=','new'), ('reject', '=', 'n')]
            

        # Group Departmental Group
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_departmental_user'):
            case_obj.write(cr, uid, ids[0],{
                'state': 'new',
                'case_state': 'لمراجعة الحالة',
                'check_user' : 0,
                'branch_management': 0
            })
            domain = [('state','=','approve1'), ('reject', '=', 'n')]
            
        # Group Social Survey
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_social_survey'):
            case_obj.write(cr, uid, ids[0], {
                'reject': 'y',
                'case_state': 'طلب مرفوض من الباحث الاجتماعي',
                'branch_management': 0,
                'social_department': 0
            })
            domain = [('state','=','approve2'), ('reject', '=', 'n')]

        # Group Central Team
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_central_team'):
            case_obj.write(cr, uid, ids[0], {
                'state': 'approve1',
                'case_state': 'لاستكمال النواقص',
                'central_department': 0,
                'branch_management': 0,
                'social_department': 0
            })
            domain = [('state','=','approve3'), ('reject', '=', 'n')]
        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_finial_decision_team'):
            case_obj.write(cr, uid, ids[0], {
                'reject': 'y',
                'case_state': 'تم رفض الاسرة',
                'central_department': 1,
                'branch_management': 1,
                'social_department': 1
            })
            domain = [('state','=','approve4'), ('reject', '=', 'n')]

        if self.pool.get('res.users').has_group(cr, uid, 'zakat.group_admin'):
            case_obj.write(cr, uid, ids[0], {
                'reject': 'y',
                'case_state': 'طلب تم رفضه من الادمن',
                'branch_management': 1,
                'social_department': 1,
                'central_department': 1

            })
            domain = [('state','=','approve4'), ('reject', '=', 'n')]
        model_obj = self.pool.get('ir.model.data')
        data_id = model_obj._get_id(cr, uid, 'zakat', 'view_zakat_tree')
        view_id = model_obj.browse(cr, uid, data_id).res_id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'case.study.request',
            'view_mode' : 'tree',
            'domain': domain,
            'nodestroy' : True,
            
        }

    @api.v7
    def delay_request(self, cr, uid, ids, context=None):
        req_obj = self.pool.get('case.study.request')
        req_obj.write(cr, uid, ids[0], {
                'delay_requests': 1

            })
        model_obj = self.pool.get('ir.model.data')
        data_id = model_obj._get_id(cr, uid, 'zakat', 'view_zakat_tree')
        view_id = model_obj.browse(cr, uid, data_id).res_id

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'case.study.request',
            'view_mode' : 'tree',
            'domain': [('state','=','approve4'), ('reject', '=', 'n')],
            'nodestroy' : True,
            
        }


    @api.one
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


    @api.onchange('salary')
    def _onchange_salary(self):
        self.salary_total = self.salary
    
    @api.onchange('pension')
    def _onchange_pension(self):
        self.salary_total = self.salary + self.pension

    @api.onchange('rents')
    def _onchange_rents(self):
        self.salary_total = self.salary + self.pension + self.rents

    @api.onchange('other')
    def _onchange_other(self):
        self.salary_total = self.salary + self.pension + self.rents + self.other

    @api.onchange('date')
    def _onchange_date(self):
        date_time = datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S').date()
        um = HijriDate(date_time.year,date_time.month,date_time.day,gr=True)
        self.hijri_date = str(int(um.day)) + "/" + str(int(um.month))+"/"+ str(int(um.year))
    @api.model
    def create(self, values):
        created_id = super(CaseStudyRequest,self).create(values)
        self.env.user.notify_info('تم الحفظ')
        return created_id	 


    
    





        
