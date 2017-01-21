# coding=utf-8

#    Copyright (C) 2008-2010  Luis Falcon

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


import time
import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _

# Add Lab test information to the Patient object

class patient_data (osv.osv):
    _name = "medical.patient"
    _inherit = "medical.patient"

    def name_get(self, cr, uid, ids, context={}):
        if not len(ids):
            return []
        rec_name = 'name'
        res = [(r['id'], r[rec_name][1]) for r in self.read(cr, uid, ids, [rec_name], context)]
        return res
        
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

    _columns = {
        'lab_test_ids': fields.one2many('medical.lab.appointment','patient','Lab Tests Required',readonly = True),
        }

patient_data ()    
    
class test_type (osv.osv):
    _name = "medical.test_type"
    _description = "Type of Lab test"
    _columns = {
        'name' : fields.char ('Test',size=128,help="Test type, eg X-Ray, hemogram,biopsy...", required=True,
        select=True),
        'code' : fields.char ('Code',size=128,help="Short name - code for the test", required=True,
        select=True),
        'info' : fields.text ('Description'),
        'product_id' : fields.many2one('product.product', 'Service', required=True),
        'critearea': fields.one2many('medical_test.critearea','test_type_id','Test Cases'),


    }
    _sql_constraints = [
            ('code_uniq', 'unique (name)', 'The Lab Test code must be unique')]

test_type ()

class lab (osv.osv):
    _name = "medical.lab"
    _description = "Lab Test"
    _columns = {
        'appointment_id':fields.many2one('medical.lab.appointment'),
        'name' : fields.char ('ID', size=128, help="Lab result ID",readonly=True),
        'test' : fields.many2one ('medical.test_type', 'Test type', help="Lab test type", required=True, select=True),
        'patient' : fields.many2one ('medical.patient', 'Patient', help="Patient ID", required=True, select=True), 
        'pathologist' : fields.many2one ('medical.physician','Pathologist',help="Pathologist",select=True),
        'requestor' : fields.many2one ('medical.physician', 'Physician', help="Doctor who requested the test",select=True),
        'results' : fields.text ('Results'),
        'diagnosis' : fields.text ('Diagnosis'),
        'critearea': fields.one2many('medical_test.critearea','medical_lab_id','Test Cases'),
        'date_requested' : fields.datetime ('Date requested', required=True,
        select=True),
        'date_analysis' : fields.datetime ('Date of the Analysis',select=True),        
        }

    _defaults = {
        'date_requested': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'date_analysis': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'name' : lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'medical.lab'),         
         }
    _order= "name desc" 


    _sql_constraints = [
                ('id_uniq', 'unique (name)', 'The test ID code must be unique')]
lab ()



class medical_lab_test_units(osv.osv):
    _name = "medical.lab.test.units"
    _columns = {
        'name' : fields.char('Unit', size=25,select=True),
        'code' : fields.char('Code', size=25,select=True),
        }
    _sql_constraints = [
            ('name_uniq', 'unique(name)', 'The Unit name must be unique')]
medical_lab_test_units()

class medical_test_critearea(osv.osv):
    _name = "medical_test.critearea"
    _description = "Lab Test Critearea"    
    _columns ={
       'name' : fields.char('Test', size=64, required=True, select=True),
       'result' : fields.float('Result'),
       'normal_range' : fields.text('Normal Range'),
       'warning':fields.boolean('Warning'),
       'excluded':fields.boolean('Excluded'),
       'lower_limit' : fields.float ('Lower Limit'),
       'upper_limit' : fields.float ('Upper Limit'),
       'remark' : fields.text('Remark'),
       'result_text' : fields.char('Result - Text', help='Non-numeric results. For example qualitative values, morphological, colors ...'), 
       
       'units' : fields.many2one('medical.lab.test.units', 'Units'),
       'test_type_id' : fields.many2one('medical.test_type','Test type'),
       'medical_lab_id' : fields.many2one('medical.lab','Test Cases'),
       'sequence' : fields.integer('Sequence'),       
       }
    _defaults = {
         'sequence' : lambda *a : 1, 
         'excluded': False, 
         'warning': False, 
         }
    _order="sequence"
    def onchange_result (self, cr, uid, ids,lower_limit, upper_limit,result,context=False):
        v={}
        if (float(result) < lower_limit or float(result) > upper_limit):
            v['warning']=True
        else:
            v['warning']=False
        return {'value': v} 
     
medical_test_critearea()

    

class medical_patient_lab_test(osv.osv):
    _name = 'medical.patient.lab.test'
    def _get_default_dr(self, cr, uid, context={}):
        partner_id = self.pool.get('res.partner').search(cr,uid,[('user_id','=',uid)])
        if partner_id:
            dr_id = self.pool.get('medical.physician').search(cr,uid,[('name','=',partner_id[0])])
            if dr_id:
                return dr_id[0]
            #else:
            #    raise osv.except_osv(_('Error !'),
            #            _('There is no physician defined ' \
            #                    'for current user.'))
        else:
            return False
        
    _columns = {
        'name' : fields.many2one('medical.test_type','Test Type',required=True, select=True),
        'date' : fields.datetime('Date'),
        'state' : fields.selection([('draft','Draft'),('tested','Tested'),('cancel','Cancel')],'State',readonly=True),
        'patient_id' : fields.many2one('medical.patient','Patient',required=True),
        'doctor_id' : fields.many2one('medical.physician','Doctor', help="Doctor who Request the lab test."), 
        'request' : fields.char('Request', readonly=True),
        'urgent' : fields.boolean('Urgent'),
        'medical_patient_id' : fields.many2one('medical.lab.appointment','Apt Id'),
        }
    
    _defaults={
       'date' : lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
       'state' : lambda *a : 'draft',
       'doctor_id' : _get_default_dr,        
       }
    
    def create(self, cr, uid, vals, context=None):
        vals['request'] = self.pool.get('ir.sequence').get(cr, uid, 'medical.patient.lab.test') or '0'
        id =super(medical_patient_lab_test, self).create(cr, uid, vals, context=context)
        return id
     
    def create_lab_test(self, cr, uid, ids, context={}):
        
        data=ids

        test_request_obj = self.pool.get('medical.patient.lab.test')
        lab_obj = self.pool.get('medical.lab')

        test_report_data={}
        test_cases = []
        test_obj = self.browse(cr, uid, ids, context=context)
        for test in test_obj:
            if test.state == 'tested':
                raise  osv.except_osv(_('UserError'),_('At least one of the selected record Test Record is already created.'))
        lab_id_list = []
        for test in [test_obj]:
            test_report_data['test'] = test.name.id
            test_report_data['patient'] = test.patient_id.id
            test_report_data['requestor'] = test.doctor_id.id
            test_report_data['date_requested'] = test.date
            
            for critearea in test.name.critearea:
                test_cases.append((0,0,{'name':critearea.name,
                            'sequence':critearea.sequence,
                            'normal_range':critearea.normal_range,
                            'lower_limit':critearea.lower_limit,
                            'upper_limit':critearea.upper_limit,
                            'units':critearea.units.id,
                            }))
            test_report_data['critearea'] = test_cases
            lab_id = lab_obj.create(cr,uid,test_report_data,context=context)
            lab_id_list.append(lab_id)
            self.write(cr, uid, [test.id], {'state':'tested'})
        return {
        'domain': "[('id','=', "+str(lab_id_list)+")]",
        'name': 'Lab Test Report',
        'view_type': 'tree',
        'view_mode': 'tree',
        'res_model': 'medical.lab',
        'type': 'ir.actions.act_window'
        }
   
medical_patient_lab_test()

class medical_lab_appointment(osv.osv):
    _name = "medical.lab.appointment"
    _columns = {
        'doctor' : fields.many2one ('medical.physician','Physician',  help="Physician's Name",required=True,),
        'name' : fields.char ('Appointment ID',size=64, readonly=True,),
        'patient' : fields.many2one ('medical.patient','Patient', help="Patient Name",required=True,),
        'appointment_sdate' : fields.datetime ('Appointment Start',required=True,),
        'appointment_edate' : fields.datetime ('Appointment End',required=True,),
        'request_date' : fields.datetime ('Request Date',required=True,),
        'institution' : fields.many2one ('res.partner','Health Center', domain=[('is_institution', '=', "1")],help="Medical Center",required=True),
        'urgency' : fields.selection([('a','Normal'),('b','Urgent'),('c','Medical Emergency'),], 'Urgency Level'),
        'comments' : fields.text('Comments'),
        'user_id' : fields.many2one ('res.users','User', help="Login User"),
        'state': fields.selection([('draft','Draft'),('requested','Requested'),('outcome','Outcome'),('cancel','Cancel')], 'State',readonly="1"),
        'test_ids' : fields.many2many('medical.test_type','apt_test_rel','apt_id','test_id','Tests',required=True, select=True),
        'lab_request': fields.one2many('medical.patient.lab.test','medical_patient_id','Test Cases'),
        'pricelist_id':fields.many2one('product.pricelist','Pricelist',required=True),
        'inv_id':fields.many2one ('account.invoice', 'Invoice',readonly =True),
        'no_invoice':fields.boolean('Invoice exempt'),
        'lab_result': fields.one2many('medical.lab','appointment_id','Lab Result'),
   }
    _sql_constraints = [
       ('date_check', "CHECK (appointment_sdate <= appointment_edate)", "Appointment Start Date must be before Appointment End Date !"),
   ]
    _order = "appointment_sdate desc"
    _defaults = {
        'state':'draft',
        'urgency': lambda *a: 'a',
        'appointment_sdate': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
        'request_date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
#     def get_date(self, cr, uid, ids, date1,lang):  
#         new_date=''
#         if date1: 
#             search_id = self.pool.get('res.lang').search(cr,uid,[('code','=',lang)])
#             record=self.pool.get('res.lang').browse(cr,uid,search_id)  
#             new_date=datetime.strftime(datetime.strptime(date1,'%Y-%m-%d %H:%M:%S').date(),record.date_format)
#         return new_date
    
    def cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'cancel'}, context=context)    
        return True
    
    def create_invoices(self, cr, uid, ids, context=None):
        """create invoices for appointment """
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        for obj in self.browse(cr, uid, ids, context=context):
            journal_ids = self.pool.get('account.journal').search(cr, uid,[('type', '=', 'sale'), ('company_id', '=', obj.institution.company_id.id)],limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error!'),
                    _('Please define sales journal for this company: "%s" (id:%d).') % (obj.institution.company_id.name, obj.institution.company_id.id))
            invoice_vals = {
                'origin':obj.name,
                'type': 'out_invoice',
                'date_invoice' :obj.appointment_sdate[0:10],
                'reference': obj.name,
                'account_id': obj.patient.name.property_account_receivable_id.id,
                'partner_id': obj.patient.name.id,
                'journal_id': journal_ids[0],
                'currency_id': obj.pricelist_id.currency_id.id,
                'company_id': obj.institution.company_id.id,
                'user_id': obj.user_id and obj.user_id.id or False,
                'fiscal_position_id':obj.patient.name.property_account_position_id and obj.patient.name.property_account_position_id.id or False,
                }
            invoice_id = invoice_obj.create(cr, uid, invoice_vals)
#             print"create invoices+++++++++++++",invoice_id
            for each_request in obj.lab_request:
                tax_ids = []
                for tax_line in each_request.name.product_id.taxes_id:
                    tax_ids.append(tax_line.id)
                if each_request.name.product_id.categ_id: 
                    account = each_request.name.product_id.categ_id.property_account_income_categ_id.id  
                    if not account:
                        raise osv.except_osv(_('Error !'), _('There is no expense account defined for this product: "%s" (id:%d)') % (obj.service_id.name, obj.service_id.id,))
                else:
                    account = self.pool.get('ir.property').get(cr, uid, 'property_account_income_categ', 'product.category').id
                price_unit = self.pool.get('product.pricelist').price_get(cr, uid, [obj.pricelist_id.id],
                    each_request.name.product_id.id, 1.0, obj.patient.name.id, {
                        'uom': each_request.name.product_id.uom_id.id ,
                        'date': obj.appointment_sdate[0:10],
                        })[obj.pricelist_id.id]
                print price_unit,"price_unit----------------------"
                in_line_vals ={
                'product_id':each_request.name.product_id.id,  
                'name' : each_request.name.product_id.name,
                'account_id': account,
                'quantity': 1,
                'price_unit' : price_unit,
                'invoice_id' : invoice_id,
                'uos_id':each_request.name.product_id.uom_id.id,
                'invoice_line_tax_ids':  [(6,0,tax_ids)],
                }
                invoice_line_obj.create(cr, uid, in_line_vals)
            self.write(cr, uid, [obj.id], {'inv_id':invoice_id,'invoice_done':True})
        return True
    
    def requested(self, cr, uid, ids, context=None):
        print'innnnnn *********** confirm*********',ids
        browse_record=self.pool.get('medical.lab.appointment').browse(cr,uid,ids)
        test_report_data={}
        lab_request=[]
        for test_obj1 in browse_record.test_ids:
            test_report_data={}
            test_report_data['name'] = test_obj1.id
            test_report_data['patient_id'] = browse_record.patient.id
            test_report_data['doctor_id'] = browse_record.doctor.id
            test_report_data['date'] = browse_record.request_date 
            test_report_data['state'] ='draft'
            lab_request.append((0,0,test_report_data))
        self.write(cr,uid,ids,{'lab_request':lab_request,'state': 'requested'},context=context)
        return True
    
    def outcome(self, cr, uid, ids, context=None):
        browse_record=self.pool.get('medical.lab.appointment').browse(cr,uid,ids)
        lab_result=[]
        for test_obj1 in browse_record.test_ids:
            test_report_data={}
            test_report_data['test'] = test_obj1.id
            test_report_data['patient'] = browse_record.patient.id
            test_report_data['requestor'] = browse_record.doctor.id
            test_report_data['date_requested'] = browse_record.request_date   
            test_cases =[]
            for critearea in test_obj1.critearea:
                test_cases.append((0,0,{'name':critearea.name,
                    'sequence':critearea.sequence,
                    'normal_range':critearea.normal_range,
                    'lower_limit':critearea.lower_limit,
                    'upper_limit':critearea.upper_limit,
                    'units':critearea.units.id,
                    }))
            test_report_data['critearea'] = test_cases
            lab_result.append((0,0,test_report_data))
        for test_obj1 in browse_record.lab_request:
            self.pool.get('medical.patient.lab.test').write(cr,uid,[test_obj1.id],{'state': 'tested'})
        self.write(cr,uid,ids,{'lab_result':lab_result,'state': 'outcome'},context=context)
        return True 
       
    def create(self, cr, uid, vals, context=None):
#         history_id = self.pool.get('medical.lab.appointment').search(cr, uid, [])   
#         for each_id in history_id:
#             appoint_record=self.browse(cr,uid,each_id,context=None)
#             if appoint_record.doctor.id==vals['doctor']:
#                 if appoint_record.appointment_sdate<=vals['appointment_sdate'] and vals['appointment_edate'] <=appoint_record.appointment_edate:
#                     raise  osv.except_osv(_('UserError'), _('Appointment Overlapping'))
#          
#                 if appoint_record.appointment_sdate<=vals['appointment_sdate'] and appoint_record.appointment_edate>=vals['appointment_sdate'] :
#                     raise  osv.except_osv(_('UserError'), _('Appointment Overlapping'))
#          
#                 if appoint_record.appointment_sdate<=vals['appointment_edate'] and appoint_record.appointment_edate>=vals['appointment_edate'] :
#                     raise  osv.except_osv(_('UserError'), _('Appointment Overlapping'))
#          
#                 if appoint_record.appointment_sdate>=vals['appointment_sdate'] and appoint_record.appointment_edate<=vals['appointment_edate'] :
#                     raise  osv.except_osv(_('UserError'), _('Appointment Overlapping'))
#          
#                 if vals['appointment_sdate']>=vals['appointment_edate']:
#                     raise  osv.except_osv(_('UserError'), _('Start of Appointment Date is greater than End of Appointment Date'))             
        if vals.get('name','0')=='0':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'medical.lab.appointment') or '0'
        return super(medical_lab_appointment, self).create(cr, uid, vals, context=context)
    
medical_lab_appointment()
