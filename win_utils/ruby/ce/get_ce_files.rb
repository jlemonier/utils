require './sqlcmd'
require './ce_finder'

class FindCe
  attr_accessor :custcode
  
  def get_ce_files custcode
    @custcode = custcode
    puts "\n1) FindCe.get_ce_files #{custcode} starting "
    
    uo_resultset = get_uo_filepaths
    puts "\n2) Update Object Filepaths Found: #{uo_resultset.size} "
    
    puts "\n3) Passing uo_resultset to ce_finder ..."
    # uo_resultset.each_with_index {|r,i| puts "\t\t#{i}) #{r}"}
    ce_sql = CeFinder.new.get_ce_sql uo_resultset
    
    show "SQL to find CE Files after manipulating Update Object Filepaths ", ce_sql
    
    ce_data = get_ce_mssg_doc_ids ce_sql
    
    puts "\nce mssg_doc_ids found ... "
    
    ce_data2 = ce_data.split("\n")
    puts ce_data2[0...9].join("\n")
    puts "\nFound #{ce_data2.size-2} rows (first 2 lines are headers and dashes)."
    # puts ce_data
    ce_data
  end
    
  def get_ce_mssg_doc_ids ce_sql
    Sqlcmd.new.run_sql 'mssg', ce_sql, 'tab'
  end  
  
  def get_uo_filepaths
    Sqlcmd.new.run_sql_file 'mssg', './sql/schenker_uo_filepaths_recent.sql', 'resultset'
  end

  def data_dir
    "./data"
  end

  def show msg, text_or_array, lines = 10
    d = text_or_array
    # puts d
    # puts d.class
    d = d.split("\n") # if d is_a? String
    puts "#{msg} -- size:#{text_or_array.size} -- array-size: #{d.size} "
    puts d[0...lines].join("\n")
    puts " ......... "
  end

end

FindCe.new.get_ce_files 'ICSGT1'
