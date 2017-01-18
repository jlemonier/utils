require "sql_tools"

module Tools
 class ExcelTools  ## < ActiveRecord::Base
  include SqlTools
  
  attr_accessor :file, :filename, :resultset, :files
  
  def initialize file, filename
    @file = file
    @filename = filename
    @sheets = {}
    Spreadsheet.client_encoding = 'UTF-8'
  end  

  ## Given Excel sheets in @file:
  ### template is the string
  ### XXXX YYYY as columns
  ### 1111 2222 as data row 1 => produce Sheet1__1111__2222.xml
  ### 3333 4444 as data row 2 => produce Sheet1__3333__4444.xml
  ##### replace XXXX with 1111, etc. inside the template
  def generate_files template, outputdir, filename
    @template = template
    @files = []
    book = Spreadsheet.open @file
    book.worksheets.each_with_index do |sheet, i|
      if i > 0
        return
      end
      @resultset = sheet2resultset sheet
      @resultset.each do |record| ## record is a hash {"XXX" => "111", "YYY" => "222"}
        newfilename = replace_strings(filename.dup, record)         ## .dup critical here or filename is corrupted later in loop
        newfilename = add_suffix(filename, record.values.join("__")) if newfilename == filename
        newfilepath = File.join(outputdir, newfilename)
        template2 = replace_strings(template.dup, record)
        # File.open(local_filename, 'w') {|f| f.write(doc) }
        File.open(newfilepath, 'w') {|f| f.write(template2) }
        @files << newfilepath
      end
    end
    
  end

  ## Given Excel Sheet
  ### Return Array of Hashes (1 hash per record w/ keys from column 1)
  ### AAA BBB
  ### 111 222
  ### 333 444
  ### ==>>
  ### [ {"AAA"=>"111", "BBB"=>"222"}, {"AAA"=>"333", "BBB"=>"444"}  ]
  def sheet2resultset sheet
    data = []
    headerrow = sheet.row 0
    headers = {}
    headerrow.each_with_index {|col,  i| headers[i] = col}
    
    sheet.each_with_index do |row, i|
      if i > 0
        record = {}
        row.each_with_index do |data, i|
          colname = headers[i] || "ZZZZnotfound"
          data = escape_float(data)
          record[colname] = data
        end
        data << record
      end
    end
    data
  end
  
  ## add_suffix "somefile.xml", "_1234" => somefile_1234.xml""
  def add_suffix filename, suffix
    parts = filename.split("\.")
    base = parts[0..-2]
    parts2 = base << suffix << parts[-1]
    fn = parts2.join(".")
  end
  
  ## hash defines key => value for updating template
  def replace_strings(str, rhash)
    s = str.to_s
    return s if ! (s && rhash)
    
    rhash.each do |k,v|
      s.gsub!(k.to_s, v.to_s)
    end    
    s
  end

  ## excel_sheets_to_sql
  ### return hash: {sheet1 => sql1, sheet2 => sql2, etc.}
  def excel_sheets_to_sql go = 50
    if true # begin
      book = Spreadsheet.open @file
      sheets = {}
      book.worksheets.each do |sheet|
        @sheets[sheet.name] = sheet_to_sql sheet
      end
    end # rescue
    @sheets
  end

  def sheet_to_sql sheet, go = 50
    headers = sheet.row 0
    headers.map!{|h| sql_column(h) }
    sql = []
    sheetname = sheet.name
    tablename = "#"+sheetname.gsub(/\s/,"")
    sql << "-- Creating temp table #{tablename} based on file: #{@filename} worksheet: #{sheetname} "
    sql << sql_create_table(tablename, headers)
    sql << "set nocount on"
    
    sheet.each_with_index do |row, i|
      sql << sql_insert(headers, row, tablename) if i > 0
      ## Need go statements for small transactions
      sql << "go" if i % go == 0
    end
    
    ## Validation SQL to check temp table  
    sql << "\n\nselect count(*) from #{tablename} \nselect top 5 * from #{tablename}"
    sql.join("\n")
  end
    

  def excel_sheets_to_data
      ## data for display
      rowdata = []
      row.each do |col|
        rowdata << col
      end
      @data << rowdata    
  end  
  
  def self.example_sql_results
    @example_sql_results = <<EXAMPLE_SQL_RESULTS

-- Creating temp table #mysheet1 based on file: shipment_examples.xls worksheet: mysheet1 
create table #mysheet1 (
[shipment_id]  varchar(500)  , 
[containernum]  varchar(500)  ,
[mysheet1_id] int identity(1,1) 
) 


set nocount on
go
insert into #mysheet1 ([shipment_id],[containernum] ) values ( '101231M03','HJCU4438282' ) 
insert into #mysheet1 ([shipment_id],[containernum] ) values ( '101231M02','HJCU4438277' ) 
insert into #mysheet1 ([shipment_id],[containernum] ) values ( 'XXXYYY111222','ABCD1234567' ) 


select count(*) from #mysheet1 
select top 5 * from #mysheet1
    
EXAMPLE_SQL_RESULTS

  @example_sql_results

end

  # text
  def self.example_data_results
    datatext = <<EXAMPLE_DATA_RESULTS
shipment_id containernum  mysheet1_id om_cm_id  customer_org_id
101231M03 HJCU4438282 1 23543973  45135
101231M02 HJCU4438277 2 23543972  45135
101231M03 HJCU4438282 3 23543973  45135
101231M02 HJCU4438277 4 23543972  45135
XXXYYY111222  ABCD1234567 5 NULL  NULL      
EXAMPLE_DATA_RESULTS

    @example_data_results = Tools::TextTools.text2html datatext
    
  end
  
 end   
end
  
