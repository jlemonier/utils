require "./sql_tools"

class CsvTools  ## < ActiveRecord::Base
  include SqlTools
  
  attr_accessor :filename
  
  def initialize filename
    @filename = filename
  end  

  # SQL Studio puts bullshit characters into first column name
  def clean_string s
    s.gsub(/\s/, "")
  end

  def csv_to_sql tmptable = nil, go = 50
    fnout = "#{@filename}.sql"
    tmptable = "##{@filename.gsub(/[.]/, "_")}".gsub(/.*\//, "") if not tmptable
    tmptable = clean_string(tmptable)
    # tablename = "##{tmptable}.gsub(/\s/,"")"
    
    csvout = CSV.open(fnout, "wb")
    headers = nil
    i = 0
    sql = []
    CSV.foreach(filename, :headers => true) do |row|
      i += 1
      # puts "In csv_to_sql - #{i}) #{row}"
      if i == 1
        headers = row.headers
        headers = headers.map{|h| clean_string h}
        
        sql << "-- Creating temp table #{tmptable} based on file: #{@filename} "
        sql << sql_create_table(tmptable, headers)
        sql << "set nocount on"
      end
      sql << sql_insert(headers, row, tmptable)
      ## Need go statements for small transactions
      sql << "go" if i % go == 0
    end
    
    ## Validation SQL to check temp table  
    sql << "\n\n-- select count(*) from #{tmptable} \n-- select top 5 * from #{tmptable}"
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

  private  

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
        row.each_with_index do |data2, i2|
          colname = headers[i2] || "ZZZZnotfound"
          data2 = escape_float(data)
          record[colname] = data
        end
        data << record
      end
    end
    data
  end  
end   
  
