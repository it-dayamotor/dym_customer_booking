import time
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import Warning
import logging
import psycopg2
_logger = logging.getLogger(__name__)

class dym_branch(models.Model):
    _name = 'dym.branch'
    _description = 'Branch'
    _rec_name = 'display_name'

    name = fields.Char('Branch')
    code = fields.Char('Code')
    display_name = fields.Char('Display Branch')
    branch_status = fields.Char('Branch Status')
    street = fields.Text('Street')

    def _cron_retrieve_data(self):
        try:
            retrieve_data_and_insert()
            logging.info('Data retrieved successfully')
        except Exception as e:
            logging.error('Error retrieving data: %s', str(e))

def retrieve_data_and_insert():
      dbname = 'B2CDM'
      user = 'b2c'
      password = 'dayamotor'
      host = '192.168.3.126'
      port = '5432'

      # dbname = 'B2CDM'
      # user = 'b2c'
      # password = 'dayamotor'
      # host = '192.168.3.66'
      # port = '5432'

      conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
      cursor = conn.cursor()

      different_dbname = 'DP_ODMPRODS'
      different_user = 'proj80_dymsm'
      different_password = 'proj80_dymsm'
      different_host = '192.168.3.98'
      different_port = '5432'

      different_conn = psycopg2.connect(dbname=different_dbname, user=different_user, password=different_password, host=different_host, port=different_port)
      different_cursor = different_conn.cursor()
      
      # For fetch data in different database partly
      offset = 0
      limit = 500000

      while True:
         different_cursor.execute("""SELECT id, name, code, display_name, branch_status, street FROM "dym_branch";
                                       """.format(limit, offset))
         different_results = different_cursor.fetchall()

         # Inserting data into the existing database
         for result in different_results:
               cursor.execute("""INSERT INTO dym_branch (id, name, code, display_name, branch_status, street) 
                           VALUES (%s, %s, %s, %s, %s, %s)""", 
                           (result[0], result[1], result[2], result[3], result[4], result[5])
                           )
               print(result)

         # Update offset for the next iteration
         offset += limit

         # Break the loop if there are no more records
         if len(different_results) < limit:
               break

      # Committing changes and closing database connections
      conn.commit()
      cursor.close()
      conn.close()
      different_cursor.close()
      different_conn.close()

      