from openerp import api, models, fields, exceptions

class XrayRequest(models.Model):
    _name = "xray.request"

    @api.one
    def change_state(self):
        for medical_test in self.medical_test_ids:
            if medical_test.xray_image == False or medical_test.diagnosis :
                raise exceptions.ValidationError("Please Insure that you Entered X-Ray Images and Diagnosis")
        self.write({'state': 'tested'})

    patient_id = fields.Many2one ('medical.patient', 'Patient', help="Patient Name", required=True, select=True)
    ##appointment_id = fields.Many2one('medical.lab.appointment')
    medical_test_ids = fields.One2many('xray.test', 'medical_request_id', 'Medical Tests')
    final_diagnosis = fields.Text ('Diagnosis')
    request_date = fields.Datetime ('Request Date', required=True,select=True)
    test_date = fields.Datetime ('Test Date',select=True)
    state = fields.Selection([('request', 'Request'), ('tested', 'Tested')], default='request')


class XrayTest(models.Model):
    _name="xray.test"

    medical_request_id = fields.Many2one('lab.medical.request', 'Medical Request')
    test_id = fields.Many2one ('xray.type', 'Test type', help="xray test type", required=True, select=True)
    xray_image = fields.Binary('X-Ray Image')
    normal = fields.Boolean('Normal')
    warning = fields.Boolean('Warning')
    test_date = fields.Datetime ('Test Date',select=True)
    price = fields.Float('Price')
    diagnosis = fields.Text ('Diagnosis')

    @api.onchange('test_id')
    def _onchange_test_id(self):
        if self.test_id:
            test = self.env['xray.type'].search([('id', '=', self.test_id.id)])
            self.price = test.price

class XrayType(models.Model):
    _name="xray.type"

    name = fields.Char('Test Name')
    code = fields.Char('Test Code')
    desc = fields.Text('Description')
    regional_imaging = fields.Selection([('chest', 'Chest'), ('brain', 'Brain'), ('bone', 'Bone'), ('tooth', 'Tooth')], 'SAMPLE TYPE')
    product = fields.Many2one('product.product')
    price = fields.Float('Price')
    time =fields.Float('Time')