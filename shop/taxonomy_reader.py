'''
Created on 5 Mar 2013

@author: martin
'''


#        

import MySQLdb as mdb
import sys
from shop.shop.models import *

def readTaxonomyFromMysql():
    con = None
    
    try:
    
        con = mdb.connect('192.168.1.31', 'root', 
            'acf42acf', 'ijdb');
    
        cur = con.cursor()
        cur.execute("SELECT c0.id AS c0_id, c0.name AS c0_name, "+
                    " c1.id, c1.name, c2.id, c2.name "+
                    "FROM category_level0 AS c0 "+
                    "JOIN category_level1 AS c1 ON ( c0.id = c1.uplink ) "+
                    "JOIN category_level2 AS c2 ON ( c1.id = c2.uplink )")
    
        rows = cur.fetchall()
    
        for row in rows:
            taxonomy = Taxonomy(cat0_name=row[1], cat1_name=row[3], cat2_name=row[5])
            taxonomy.save()
            print row
        
        
    except mdb.Error, e:
      
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
            
        if con:    
            con.close()
from tempfile import TemporaryFile#
from xlwt import Workbook
def exportTaxonomyXLS():
    taxonomy = Taxonomy.objects.all().order_by("cat0_name")
    book = Workbook()
    sheet1 = book.add_sheet('ProductTaxonomy')
    rowidx = 0
    for tax in taxonomy:
        
        sheet1.write(rowidx,0,tax.cat0_name)
        sheet1.write(rowidx,1,tax.cat1_name)
        sheet1.write(rowidx,2,tax.cat2_name)
        rowidx +=1
    
    book.save('simple.xls')
    book.save(TemporaryFile())
        
from xlrd import *
def importTaxonomyXLS():
    workbook = open_workbook('simple.xls')
    worksheet = workbook.sheet_by_index(0)
    num_rows = worksheet.nrows - 1
    #num_cells = worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        print row
        # two cells
        cell_value_0 = worksheet.cell_value(curr_row, 0)
        cell_value_1 = worksheet.cell_value(curr_row, 1)
        cell_value_2 = worksheet.cell_value(curr_row, 2)
        taxonomy = Taxonomy(cat0_name=cell_value_0, cat1_name=cell_value_1, cat2_name=cell_value_2)
        taxonomy.save()
        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
        #print curr_row, curr_cell
        #cell_type = worksheet.cell_type(curr_row, curr_cell)
        #cell_value = worksheet.cell_value(curr_row, curr_cell)
        #print '    ', cell_type, ':', cell_value
        
            

def deleteTaxonomy():
    Taxonomy.objects.all().delete()

if __name__ == '__main__':
    #deleteTaxonomy()
    importTaxonomyXLS()
    
    