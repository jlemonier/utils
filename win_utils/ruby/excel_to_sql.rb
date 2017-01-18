# RUBYLIB=R:\dev\gtroot1\app\models;R:\dev\gtroot1\lib
# R:\dev\gtroot1\app\models\tools\excel_tools.rb
# R:\dev\gtroot1\app\controllers\upload_controller.rb
# R:\dev\gtroot1\lib\sql_tools.rb

# R:\dev\gtroot1\app\models\tools
# 

# See RUBYPATH which includes directories in Rails app: R:\dev\gtroot1\...
# SET RUBY (to see environment variables)
# require 'R:\\dev\\gtroot1\\tools\\excel_tools.rb'
require 'R:\\dev\\gtroot1\\app\\models\\tools\\excel_tools.rb'
require 'sql_tools'

uploaded_io = "\\\\gthqfile1\\Transfer\\jlemonier\\Adidas_PO_Backlog\\adidas_po_info_v3.xls"

et = Tools::ExcelTools.new File.new(uploaded_io), uploaded_io
sheets_sql = et.excel_sheets_to_sql

