from odoo import models,fields,api
import time
from datetime import datetime, timedelta
from odoo import netsvc
from odoo.exceptions import Warning
from random import randint
import requests
import json
import urllib
import hashlib
from time import mktime
from odoo import http
from odoo.http import request
from odoo.http import Response

import base64
import logging
_logger = logging.getLogger(__name__)

class dym_customer_booking_controller(http.Controller):

    @http.route('/booking/new',type='http', auth='public',website=True)
    def handler_booking_new(self,**kwargs):
        values={}
        values['jam'] = ['08','09','10','11','13','14','15']
        values['menit'] = ['00','10','15','20','25','30','35','40','45','50','55']
        branch = request.env['dym.branch.street'].sudo().search([])
        item = []
        for x in branch:
            item.append({'city_id':x.city_id.id,'city_name':x.city_name})
        item_list = [dict(s) for s in set(frozenset(d.items()) for d in item)]
        # item_list = set(item)
        # values['branch_rec'] = branch
        values['city_rec'] = sorted(item_list, key=lambda k: (k['city_name']))

        return http.request.render("dym_customer_booking.booking_service", values)

    @http.route('/cek/city',type='json', auth='public')
    def handler_cek_city(self,**kwargs):
        values=kwargs
        if values['city']:
            branch = request.env['dym.branch.street'].sudo().search([('city_id','=',int(values['city']))])
            items = []
            if branch:
                for x in branch:
                    items.append({
                        'id':x.id,
                        'display_name':x.display_name
                    })
            values['branch_rec'] = items
            values['city_id'] = values['city']
            _logger.info(str(values) + 'tahtansndansd;lasldkasdkaskdjasdasdw8888888888888888888')
        else:
            values['branch_rec'] = False
            values['city_id'] = False
        return values


    @http.route('/booking_success',type='http', auth='public',website=True)
    def handler_booking_success(self,**kwargs):
        values={}
        _logger.info(str(kwargs))

        if kwargs:
            book_new = request.env['dym.booking.service'].sudo().create({
                'branch_id':int(kwargs['branch_id']),
                'nama_cust':kwargs['nama'],
                'mobile':kwargs['mobile'],
                'no_polisi':kwargs['no_polisi'],
                'type_motor':kwargs['type_motor'],
                'date_booking':datetime.strptime(kwargs['tgl_servis'],'%m/%d/%Y').strftime('%Y-%m-%d'),
                'jam':kwargs['jam_servis'],
                'menit':kwargs['menit_service'],
                'branch_pilihan':kwargs['branch_id'],
                'keluhan':kwargs['keluhan'],
                'date':datetime.now(),
                'kategori_pit':kwargs['kategori_pit'],
            })
            _logger.info(str(book_new.ref_odm) + '00000000')
            values['no_booking'] = book_new.ref_odm
        _logger.info(str(values) + '999999999999')
        return http.request.render("dym_customer_booking.booking_success", values)
