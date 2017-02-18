# -*- coding: utf-8 -*-

from openerp.osv import orm
from openerp import SUPERUSER_ID

from openerp.http import request


class QWeb(orm.AbstractModel):
    _inherit = 'ir.qweb'

    def render(self, cr, uid, id_or_xml_id, qwebcontext=None, loader=None, context=None):
        context = context or {}
        if qwebcontext and qwebcontext.get('lang_direction', None):
            
            return super(QWeb, self).render(
                cr,
                uid,
                id_or_xml_id,
                qwebcontext=qwebcontext,
                loader=loader,
                context=context)
        lang_obj = self.pool.get('res.lang')
        lang = context.get('lang', None)
        if not lang:
            if qwebcontext.get('lang', None):
                lang = qwebcontext.get('lang')
            elif uid:
                user = self.pool.get('res.users').browse(cr, uid, uid, context=context)
                lang = user.partner_id.lang
            else:
                lang = 'en_US'
        directions = lang_obj.get_languages_dir(cr, uid, [], context=context)
        direction = directions.get(lang, 'ltr')
        qwebcontext['lang_direction'] = qwebcontext.get('lang_direction', None) or direction
        
        return super(QWeb, self).render(
            cr,
            uid,
            id_or_xml_id,
            qwebcontext=qwebcontext,
            loader=loader,
            context=context)
