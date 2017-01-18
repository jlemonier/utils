require './database'
require 'tempfile'

class Sqlcmd
  attr_accessor :output_mode
  def initialize
    @output_mode = 'resultset'
  end
  
  # run a string
  def run_sql dbkey, sql, output_type = 'resultset', delim = delim_default, debug = false
    output = Tempfile.new("#{dbkey}_sql_", "./sqltemp")
    db = Database.lookup dbkey
    
    sql = "set nocount on; #{sql}"
    puts "\n\nOn #{db}: \n\tRunning SQL: \n\n\t\t#{sql[0...5000]}" if not debug
    puts "\n\nOn #{db}: \n\tRunning SQL: \n\n\t\t#{sql}" if debug
    
    cmd = "sqlcmd.exe -S #{db.server} -d #{db.dbname} -W -s#{delim} -Q \"#{sql}\" -o #{output.path} "
    # puts "\n\t\tRunning: #{cmd}"
    system(cmd)
    
    # data = File.read(output)
    # puts File.size(output)
    # puts "#{data}"
    
    # print_first_row sqlcmd_to_resultset(output) if 1
    
    case output_type
    when 'resultset'
      return sqlcmd_to_resultset(output)
    when 'file'
      return output
    when 'tab'
      data = File.read(output).gsub(delim, '\t')
      lines = data.split('\n')
      lines.delete_at 1
      lines.delete_at lines.size
      # puts "Total Lines: lines.size
      return lines.join('\n')
    end
    
    
  end 

  def run_sql_file dbkey, file, output_type = 'resultset', delim = delim_default
    sql = File.read(file)
    self.run_sql dbkey, sql, output_type, delim
  end  

  def sqlcmd_to_resultset(data)
    delim = delim_default
    rows = []
    headers = []
    File.open(data).each_with_index do |line, i|
      line = line.strip
      # puts "#{i}) #{line}"
      if i == 0
        headers = line.split(delim)
      elsif i == 1
        # --- row random? 
      else 
        cols = line.split(delim)
        row = Hash[headers.zip cols]
        rows << row
      end
    end
    # rows = rows[0...-1]
    # rows.each {|r| puts r}
    rows
  end
  
  def delim_default
    '`'
  end
  
  def print_first_row resultset
    resultset.each do |row|
      row.each {|k,v| puts("#{k} ==> #{v}")}
      break
    end
  end
      
end
