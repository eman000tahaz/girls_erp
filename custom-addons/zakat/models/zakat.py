from openerp import api, models, fields, exceptions
import Datetime

class CaseStudyRequest(models.Model):
    _name = "case.study.request"

    date = fields.Datetime('Date', default=Datetime.now(), translate=True)
    family_head = fields.Many2one('res.partner', 'Family Head', translate=True)
    relative_relation = fields.Many2one('relative.relation', 'Relative Relation', translate=True)
    work_place = fields.Many2one('work.place', 'Work Place', translate=True)
    job = fields.Char('Job', translate=True)
    mobile = fields.Char('Mobile', translate=True)
    fh_state = fields.Selection([('employee', '=', 'Employee'),
                                 ('retired', '=', 'Retired'),
                                 ('helpless', '=', 'Helpless'),
                                 ('jailed', '=', 'Jailed'),
                                 ('dead', '=', 'Dead'),
                                 ('unemployed', '=', 'Unemployed'),
                                 ('other', '=', 'Other')], 'Family Head State', translate=True)
    fh_state_desc = fields.Char()
    salary = fields.Float('Salary', translate=True)
    pension = fields.Float('Pension', translate=True)
    rents = fields.Float('Rents', translate=True)
    other = fields.Float('Salary', translate=True)
    account_no = fields.Char('Bank Account Number', translate=True)
    bank_name = fields.Char('Bank Name', translate=True)
    wife_name = fields.Many2one('res.partner', domain=[('sex', '=', 'female')], translate=True)
    wife_mobile = fields.Char('Wife Mobile', translate=True)
    address = fields.Char('Address', translate=True)
    family_state = fields.Many2one('family.state', translate=True)
    housing = fields.Many2one('housing', 'Housing State', translate=True)
    ##loan_ids = fields.One2many('loan', 'request_id', 'Loans', translate=True)
    ##family_req_ids = fields.One2many('family.requirement', 'request_id', 'Family requirements', translate=True)

class RelativeRlation(models.Model):
    _name = 'relative.relation'

    name = fields.Char('Name', translate=True)

class WorkPlace(models.Model):
    _name = 'work.place'

    name = fields.Char('Name', translate=True)

class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    sex = fields.Selection([('male', '=', 'Male'), ('female', '=', 'Female')], 'Sex', translate=True)

class FamilyState(models.Model):
    _name = 'family.state'

    name = fields.Char('State Name', translate=True)
    persons_lived_in = fields.Integer('Individuals Who lived in House', translate=True)
    persons_lived_out = fields.Integer('Individuals Who Not lived in House', translate=True)

class FamilyState(models.Model):
    _name = 'housing'

    state = fields.Selection([(),
                              ()])
    type = fields.Char('Type')
    rooms = fields.Integer('Number of Rooms', translate=True)
    