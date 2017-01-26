# -*- coding: utf-8 -*-
{

    'name': 'EA^2 Medical Security',
    'version': '1.0.0.0',
    'author': 'Aya Mohammed',
    'category': 'Medical',
    'depends': [
        'medical_demo',
        'medical_lab',
    ],
    'license': 'AGPL-3',
    'data': [
        'views/aea_medical_menuitems.xml',
        'security/medical_security.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
