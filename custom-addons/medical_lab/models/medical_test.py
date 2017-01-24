from openerp import api, models, fields, exceptions

class MedicalLabRequest(models.Model):
    _name="lab.medical.request"


    @api.one
    def change_state(self):
        for medical_test in self.medical_test_ids:
            if medical_test.result == False :
                raise exceptions.ValidationError("Please Enter Results first")
        self.write({'state': 'tested'})

    patient_id = fields.Many2one ('medical.patient', 'Patient', help="Patient Name", required=True, select=True)
    ##appointment_id = fields.Many2one('medical.lab.appointment')
    medical_test_ids = fields.One2many('lab.medical.test', 'medical_request_id', 'Medical Tests')
    diagnosis = fields.Text ('Diagnosis')
    request_date = fields.Datetime ('Request Date', required=True,select=True)
    test_date = fields.Datetime ('Test Date',select=True)
    state = fields.Selection([('request', 'Request'), ('tested', 'Tested')], default='request')

class MedicalLabTest(models.Model):
    _name="lab.medical.test"

    medical_request_id = fields.Many2one('lab.medical.request', 'Medical Request')
    test_id = fields.Many2one ('lab.test.type', 'Test type', help="Lab test type", required=True, select=True)
    result = fields.Float ('Result')
    lower_limit = fields.Float ('Lower Limit')
    upper_limit = fields.Float ('Upper Limit')
    normal = fields.Boolean('Normal')
    warning = fields.Boolean('Warning')
    excluded = fields.Boolean('Excluded')
    test_date = fields.Datetime ('Test Date',select=True)
    price = fields.Float('Price')
    diagnosis = fields.Text ('Diagnosis')

    @api.depends('test_id')
    def onchange_test_id(self):
        values={}
        print "amy"
        if self.test_id:
            test = self.env['lab.test.type'].search([('id', '=', self.test_id.id)])
            print test
            values = {
                'lower_limit': test.lower_limit,
                'upper_limit' : test.upper_limit,
            }
        return {'value': values}

    @api.depends('result')
    def onchange_result(self):
        v={}
        if(float(self.result) < self.lower_limit or float(self.result) > self.upper_limit):
            v['excluded']=True
            v['warning']=False
            v['normal']=False
        elif(float(self.result) == self.lower_limit or float(self.result) == self.upper_limit):
            v['warning']=True
            v['excluded']=False
            v['normal']=False
        else :
            v['normal']=True
            v['warning']=False
            v['excluded']=False
        return {'value': v}


class TestType(models.Model):
    _name="lab.test.type"

    name = fields.Char('Test Name')
    code = fields.Char('Test Code')
    lower_limit = fields.Float ('Lower Limit')
    upper_limit = fields.Float ('Upper Limit')
    desc = fields.Text('Description')
    sample_type = fields.Selection([('blood', 'BLOOD'), ('urine', 'URINE'), ('stool', 'STOOL')], 'SAMPLE TYPE')
    product = fields.Many2one('product.product')
    price = fields.Float('Price')
    time =fields.Float('Time')