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
from random import randint

import base64
import logging
_logger = logging.getLogger(__name__)

class dym_booking_service(models.Model):
    _name = 'dym.booking.service'
    _description = 'Booking Service'

    branch_id = fields.Many2one('dym.branch', 'Branch', readonly=True)
    name = fields.Char('Name',readonly=True)
    nama_cust = fields.Char('Nama Customer',readonly=True)
    mobile = fields.Char('Mobile',readonly=True)
    no_polisi = fields.Char('No Polisi',readonly=True)
    type_motor = fields.Selection([('matic','Matic'),('cub','CUB/Bebek'),('sport','Sport')],'Type Motor',readonly=True)
    date_booking = fields.Date('Tanggal Booking',readonly=True)
    jam = fields.Char('Jam Service',readonly=True)
    menit = fields.Char('Menit',readonly=True)
    branch_pilihan = fields.Many2one('dym.branch.street', 'Brach Pilihan', readonly=True)
    keluhan = fields.Text('Keluhan',readonly=True)
    date = fields.Date('Date',readonly=True)
    ref_odm = fields.Char('Ref ODM',readonly=True)
    keterangan_error = fields.Text('Keterangan Error',readonly=True)
    state = fields.Selection([('success','Success'),('fail','Fail')],'State',readonly=True)
    kategori_pit = fields.Selection([('R','Reguler'),('D','DQS')],'Kategori PIT',readonly=True)

    @api.model
    def create(self, values):
        branch_id = self.env['dym.branch'].search([('id','=',values['branch_id'])])

        values['name'] = self.env['ir.sequence'].get_sequence_book(self._cr,self._uid,'BOOK-C/%s'%(branch_id.code))
        values['ref_odm'] = False
        HEADERS = {
                'Content-Type':'application/json',
                'API-KEY':'LEADS',
                'SECRET-KEY':'SEMONGKO',
            }
        DATA = {
            "params":{
                'date':values['date_booking'],
                'jam':values['jam'],
                'menit':values['menit'],
                'branch_id':values['branch_id'],
                'no_polisi':values['no_polisi'],
                'mobile':values['mobile'],
                'keluhan':values['keluhan'],
                'nama_cust':values['nama_cust'],
                'ref_b2b':values['name'],
                'kategori_pit':values['kategori_pit'],
            }
        }
        post_book = requests.post(url = '%s'%('http://192.168.3.59:7501/v1/post_booking'), data=json.dumps(DATA),headers=HEADERS)
        try:
            _logger.info(str(post_book.json()) + '++++++++=========')
            if 'ref_odm' in post_book.json()['result']:
                _logger.info('++++++++++++++++++++++++')
                values['ref_odm'] = post_book.json()['result']['ref_odm']
                values['state'] = 'success'
            else:
                try:
                    values['keterangan_error'] = post_book.json()
                except:
                    values['keterangan_error'] = post_book.text
                values['state'] = 'fail'
        except:
            _logger.info(post_book)
            values['ref_odm'] = 'ERROR'
            values['state'] = 'fail'
            try:
                values['keterangan_error'] = post_book.json()
            except:
                values['keterangan_error'] = post_book.text
        _logger.info(str(values)+ '--------------------')
        book_id = super(dym_booking_service,self).create(values)
        return book_id

class dym_sequence(models.Model):
    _inherit = 'ir.sequence'

    def get_sequence_book(self, cr, uid, first_prefix, padding=5, context=None):
            ids = self.search([('name','=',first_prefix),('padding','=',padding)])
            if not ids:
                prefix = first_prefix + '/%(y)s%(month)s/'
                ids = self.create({'name': first_prefix,
                                    'implementation': 'no_gap',
                                    'prefix': prefix,
                                    'padding': padding})
                
            return self.get_id(ids.id)

    

    
   