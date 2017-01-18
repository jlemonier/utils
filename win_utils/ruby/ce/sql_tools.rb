require "./string_tools"

module SqlTools
  include StringTools
  def sql_insert headers, row, table
    sql = "insert into #{table} (#{headers.join(",")} ) values ( #{sql_rowdata row} ) "
  end 

  # Prevent ' from ruining SQL statments
  # change "1.0" => "1"
  def sql_escape_data s
    s = s.to_s
    s.gsub!("'", "''")
    s = escape_float s
    s
  end
  ## Excel "99" comes out as Float/String 99.0
  def escape_float s
    s = s.to_s
    s.gsub!("\.0", "")
    s
  end
    
  def sql_column s
    s = remove_whitespace s
    "[#{s}]"
  end
  
  # Given a row of data [a,b,c] => 'a', 'b', 'c'
  def sql_rowdata row, integer_columns = []
    # row = row.to_hash if not row.respond_to? :map!
    # If row is ['aaa','bbb'] -- simple data, no problem.
    # If row is [['col','aaa'], ['col2','bbb']] --> then we need to get values from hash
    row = row.to_hash.values # if row[0].kind_of?(Array)
    row = row.map{|s| sql_escape_data s }
    result = "'"+row.join("','") + "'"
    result = result.gsub("'NULL'", "NULL")
  end
  
  def sql_create_table table, headers
    headers2 = headers.map{|h| "#{h} #{sql_column_type h} " }
    # headers2 
    autoid = table.gsub("#","").gsub(/\s/, "") + "_id"
    sql = "create table #{table} (\n#{headers2.join(", \n")},\n[#{autoid}] int identity(1,1) \n) \n\n"
  end
  def sql_column_type column_name
    coltype = " varchar(500) "
    case
    when column_name.match(/shipment_id/)
    when column_name.match(/_id/)
        coltype = " int "
    end
    coltype 
  end
  
end