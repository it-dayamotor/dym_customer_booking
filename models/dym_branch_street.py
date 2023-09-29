import time
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)
import requests
import json

class dym_branch_street(models.Model):
    _name = 'dym.branch.street'
    _description = 'Branch Street'
    _rec_name = 'display_name'
    _order = 'city_name asc'

    name = fields.Char('Branch')
    code = fields.Char('Code')
    display_name = fields.Char('Display Branch')
    city_id = fields.Many2one('dym.city','City')
    city_name = fields.Char('City Name')

    def update_data_branch_street(self):
        HEADERS = {
            'Content-Type':'application/json',
            'API-KEY':'LEADS',
            'SECRET-KEY':'SEMONGKO'
        }
        DATA =  {
                    "params": {
                        'password':'(Hitominojuunin) InYourEyes'
                    }
                }
        
        get_data = requests.post(url='http://192.168.3.99/v1/post_branch_street',data=json.dumps(DATA),headers=HEADERS,verify=False)
        get_data_json = get_data.json()
        _logger.info(get_data_json['result']['branch'])

        if 'result' in get_data_json:
            for b in get_data_json['result']['branch']:
                cek_branch = self.env['dym.branch.street'].sudo().search([('id','=',int(b['id']))])
                if cek_branch:
                    cek_branch.sudo().write({
                        'name':b['name'],
                        'code':b['code'],
                        'display_name':b['display_name'],
                        'city_id':b['city_id'],
                        'city_name':b['city_name']
                    })
                else:
                    self._cr.execute(""" insert into dym_branch_street (id,name,code,display_name,city_id,city_name) values ('%s','%s','%s','%s','%s','%s')"""%(b['id'],b['name'],b['code'],b['display_name'].replace("'",""),b['city_id'],b['city_name']))