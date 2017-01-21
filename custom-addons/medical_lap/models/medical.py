# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from openerp import api, fields, models
from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class insurance_plan(osv.osv):
    _name = "medical.insurance.plan"
    
    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'name'
        res = [(r['id'], r[rec_name][1]) for r in self.read(cr, uid, ids, [rec_name], context)]
        return res
    
    _columns = {
    'name' : fields.many2one('product.product', 'Plan', required=True,
        domain=[('type', '=', 'service'), ('is_insurance_plan', '=', True)],help='Insurance company plan'),
    'company' : fields.many2one('res.partner','Insurance Company',domain=[('is_insurance_company', '=', "1")],required=True, ),
    'is_default' : fields.boolean('Default plan',help='Check if this is the default plan when assigning this insurance company to a patient'),
    'notes' : fields.text('Extra info'),
    }


class insurance (osv.osv):

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        reads = self.read(cr, uid, ids, ['number','company'], context)
        res = []
        for record in reads:
            name = record['number']
            if record['company']:
                name = record['company'][1] + ': ' +name
            res.append((record['id'], name))
        return res

    _name = "medical.insurance"
    _columns = {
        'name' : fields.many2one ('res.partner','Owner'), 
        'number' : fields.char ('Number', size=64,required=True),
        'company' : fields.many2one ('res.partner','Insurance Company',domain=[('is_insurance_company', '=', "1")],required=True,),
        'member_since' : fields.date ('Member since'),
        'member_exp' : fields.date ('Expiration date'),
        'category' : fields.char ('Category', size=64, help="Insurance company plan / category"),
        'type' : fields.selection([('state','State'),('labour_union','Labour Union / Syndical'),('private','Private'),], 'Insurance Type'),
        'notes' : fields.text ('Extra Info'),
        'plan_id' : fields.many2one('medical.insurance.plan', 'Plan',help='Insurance company plan'),
        }
    


class partner_patient (osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
        'date' : fields.date('Partner since',help="Date of activation of the partner or patient"),
        'ref': fields.char('ID Number', size=64),
        'is_person' : fields.boolean('Person', help="Check if the partner is a person."),
        'is_patient' : fields.boolean('Patient', help="Check if the partner is a patient"),
        'is_doctor' : fields.boolean('Physician', help="Check if the partner is a Physician"),
        'is_institution' : fields.boolean ('Institution', help="Check if the partner is a Medical Center"),
        'is_insurance_company' : fields.boolean('Insurance Company', help="Check if the partner is a Insurance Company"),
        'lastname' : fields.char('Last Name', size=128, help="Last Name"),
        'insurance' : fields.one2many ('medical.insurance','company',"Insurance"),
    }
    _sql_constraints = [
                ('ref_uniq', 'unique (ref)', 'The partner or patient code must be unique')
         ]

    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.lastname:
                name += ' ' + record.lastname
            res.append((record.id, name))
        return res


class product_medical (osv.osv):
    _name = "product.product"
    _inherit = "product.product"
    _columns = {
                'is_insurance_plan' : fields.boolean('Insurance Plan',help='Check if the product is an insurance plan'),
    }

class speciality (osv.osv):
    _name = "medical.speciality"
    _columns = {
        'name' :fields.char ('Description', size=128, required=True,help="ie, Addiction Psychiatry"),
        'code' : fields.char ('Code', size=128, help="ie, ADP"),
    }
    _sql_constraints = [
                ('code_uniq', 'unique (name)', 'The Medical Specialty code must be unique')]


class physician (osv.osv):
    _name = "medical.physician"
    _description = "Information about the doctor"
    _columns = {
        'name' : fields.many2one ('res.partner','Dentist',required=True, domain=[('is_doctor', '=', "1"),('is_person', '=', "1")], help="Physician's Name, from the partner list"),
        'institution' : fields.many2one ('res.partner','Institution',domain=[('is_institution', '=', "1")],help="Institution where she/he works"),
        'code' : fields.char ('Registration No', size=128, help="MD License ID"),
        'speciality' : fields.many2one ('medical.speciality','Specialty',required=True, help="Specialty Code"),
        'info' : fields.text ('Extra info'),
        'ssn': fields.char('SSN', size=128, required=True,), 
        'user_id':fields.related('name','user_id',type='many2one',relation='res.users',string='Dentist User',store=True),

        }

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'name'
        res = [(r['id'], r[rec_name][1]) for r in self.read(cr, uid, ids, [rec_name], context)]
        return res


class patient_data (osv.osv):

    def name_get(self, cr, user, ids, context={}):
        if not len(ids):
            return []
        def _name_get(d):
            name = d.get('name','')
            id = d.get('patient_id',False)
            if id:
                name = '[%s] %s' % (id,name[1])
            return (d['id'], name)
        result = map(_name_get, self.read(cr, user, ids, ['name','patient_id'], context))
        return result

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=80):
        if not args:
            args=[]
        if not context:
            context={}
        if name:
            ids = self.search(cr, user, [('patient_id','=',name)]+ args, limit=limit, context=context)
            if not len(ids):
                ids += self.search(cr, user, [('name',operator,name)]+ args, limit=limit, context=context)
        else:
            ids = self.search(cr, user, args, limit=limit, context=context)
        result = self.name_get(cr, user, ids, context)
        return result    

    def onchange_dob(self, cr, uid, ids,birth_date,context = None ):
         v={}
         c_date=datetime.today().strftime('%Y-%m-%d')
         if (birth_date<=c_date):
            v['dob'] = birth_date
         else:
            raise  osv.except_osv(_('UserError'), _(' Birthdate cannot be After Current Date'))
         return {'value': v} 
    
# Get the patient age in the following format : "YEARS MONTHS DAYS"
# It will calculate the age of the patient while the patient is alive. When the patient dies, it will show the age at time of death.
        
    def _patient_age(self, cr, uid, ids, name, arg, context={}):
        def compute_age_from_dates (patient_dob,patient_deceased,patient_dod):
            now=datetime.now()
            if (patient_dob):
                dob=datetime.strptime(patient_dob,'%Y-%m-%d')
                if patient_deceased :
                    dod=datetime.strptime(patient_dod,'%Y-%m-%d %H:%M:%S')
                    delta=relativedelta (dod, dob)
                    deceased=" (deceased)"
                else:
                    delta=relativedelta (now, dob)
                    deceased=''
                years_months_days = str(delta.years) +"y "+ str(delta.months) +"m "+ str(delta.days)+"d" + deceased
            else:
                years_months_days = "No DoB !"
             
            return years_months_days
        result={}
        for patient_data in self.browse(cr, uid, ids, context=context):
            result[patient_data.id] = compute_age_from_dates (patient_data.dob,patient_data.deceased,patient_data.dod)
        return result

    _name = "medical.patient"
    _description = "Patient related information"
    _columns = {
        'name' : fields.many2one('res.partner','Patient', required="1", domain=[('is_patient', '=', True), ('is_person', '=', True)], help="Patient Name"),
        'patient_id': fields.char('Patient ID', size=64, readonly=True,  help="Patient Identifier provided by the Health Center. Is not the patient id from the partner form"),    
        'ssn': fields.char('SSN', size=128,help="Patient Unique Identification Number"),    
        'dob' : fields.date ('Date of Birth'),
        'age' : fields.function(_patient_age, method=True, type='char', size=32, string='Patient Age',help="It shows the age of the patient in years(y), months(m) and days(d).\nIf the patient has died, the age shown is the age at time of death, the age corresponding to the date on the death certificate. It will show also \"deceased\" on the field"),
        'sex' : fields.selection([('m','Male'),('f','Female'),], 'Sex', ),
        'marital_status' : fields.selection([('s','Single'),('m','Married'),('w','Widowed'),('d','Divorced'),('x','Separated'),], 'Marital Status'),
        'blood_type' : fields.selection([('A','A'),('B','B'),('AB','AB'),('O','O'),], 'Blood Type'),
        'rh' : fields.selection([('+','+'),('-','-'),], 'Rh'),
        'user_id':fields.related('name','user_id',type='many2one',relation='res.users',string='Doctor',help="Physician that logs in the local Medical system (HIS), on the health center. It doesn't necesarily has do be the same as the Primary Care doctor",store=True),
        'critical_info' : fields.text ('Important disease, allergy or procedures information',help="Write any important information on the patient's disease, surgeries, allergies, ..."),
        'general_info' : fields.text ('General Information',help="General information about the patient"),
        'deceased' : fields.boolean ('Deceased',help="Mark if the patient has died"),
        'dod' : fields.datetime ('Date of Death'),
        'photo':fields.related('name','image',type='binary',string='Picture'),
    }
#     _defaults={
#         'patient_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'medical.patient'),
#         }

    _sql_constraints = [
                ('name_uniq', 'unique (name)', 'The Patient already exists'),
                ('patient_id_uniq', 'unique (patient_id)', 'The Patient ID already exists'),
#                 ('ssn_uniq', 'unique (ssn)', 'The Patient SSN already exists')
                ]
    
    def create(self, cr, uid, vals, context=None):
        c_date=datetime.today().strftime('%Y-%m-%d')
        if (vals['dob']<=c_date):
            vals['patient_id'] = self.pool.get('ir.sequence').get(cr,uid,'medical.patient')
            id = super(patient_data, self).create(cr, uid, vals, context=context)
        else:
            raise  osv.except_osv(_('UserError'), _(' Birthdate cannot be After Current Date'))
        return id
    
            
