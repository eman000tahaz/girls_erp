# -*- coding: utf-8 -*-

from openerp.osv import orm
import openerp

class res_lang(orm.Model):
    _inherit = 'res.lang'

    @openerp.tools.ormcache(skiparg=3)
    def _get_languages_dir(self, cr, uid, id, context=None):
        ids = self.search(cr, uid, [('active', '=', True)], context=context)
        langs = self.browse(cr, uid, ids, context=context)
        return dict([(lg.code, lg.direction) for lg in langs])

    def get_languages_dir(self, cr, uid, ids, context=None):
        return self._get_languages_dir(cr, uid, ids)

    def write(self, cr, uid, ids, vals, context=None):
        self._get_languages_dir.clear_cache(self)
        return super(res_lang, self).write(cr, uid, ids, vals, context)