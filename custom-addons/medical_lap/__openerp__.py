# -*- coding: utf-8 -*-
{
    'name': 'Medical Lap',
    'version': '8.0.1.1.0',
    'category': 'medical',
    'depends': ['base','sale','purchase','account','product','document', 'medical_insurance', 'medical'],
    'data': [
        "security/medical_security.xml",
        "security/ir.model.access.csv",
        'views/medical_view.xml',
        #'views/medical_sequences.xml',
        'views/medical_lab_view.xml',
        'data/lab_test_data.xml',
        'views/medical_view_report.xml',
        'views/lab_test_demo.xml',
        'views/lab_result_demo.xml',
    ],
    'author': 'Eman Taha',
    'installable': True,
    'application': True,
    'auto_install': False,
}
