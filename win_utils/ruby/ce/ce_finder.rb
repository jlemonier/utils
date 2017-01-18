require "./csv_tools"
require "./sql_tools"
require "tempfile"
require "csv"

class CeFinder
  def get_ce_sql uo_resultset
    @resultset = uo_resultset
    
    prepare_ce_filepath
    write_csv_tmp_file
    produce_sql_tmp_table "#ce_find"
    
    # @csv = CSV.read("/#{Rails.public_path}/uploads_prices/"+params[:file], {:encoding => "CP1251:UTF-8", :col_sep => ";", :row_sep => :auto, :headers => :false})
    # @csv = CSV.foreach(params[:update_object_file], {:col_sep => "\t", :headers => true})      
    # filepath
    # puts "here ********************"
    # puts @sql
    @sql
  end

  private
  
  def write_csv_tmp_file
    @csvfile = Tempfile.new("ce_find1")
    @csvfilename = @csvfile.path
    CSV.open(@csvfile, 'wb') do |w|
      # puts "SSSSSS size: #{@resultset.size}  "
      @resultset.each_with_index do |row, i|
        # puts "in write_csv_tmp_file: #{i}) #{row}"
        # row = row.map{|d| d.gsub(/\W+/, '')} if 1 == i  # Remove bullshit SQL Server characters from header line
        w << row.values 
      end
    end
  end
  
  def produce_sql_tmp_table tmptable = nil
    @sqlfile = Tempfile.new("ce_sql")
    
    # puts("\n\n\n***** ce_finder.product_sql_tmp_table *** ")
    # puts(File.read(@csvfilename))
    # puts("ce_finder.product_sql_tmp_table *** *****")
    
    ct = CsvTools.new(@csvfilename)    
    @sql = "-- #{@sqlfile.path}  \n"
    @sql += ct.csv_to_sql tmptable
    
    @sql += """
  -- select count(*) num_update_objects from #ce_find 
  -- select top 5 'showing 5 update_object rows.  Next step will store CE matching mssg_doc_ids into #ce_found', * from #ce_find

    -- SQL to create tmp table must be as small as possible
    -- d.mssg_doc_id, d.filename uo.ce_filepath ce_filepath_searched
    -- , d.mssg_doc_id ce_mssg_doc_id, d.filepath ce_filepath_found, d.filename ce_filename
    -- , uo.*
  
  select d.mssg_doc_id ce_mdid, d.filename ce_filename, d.createtime ce_createtime
    , uo.uo_mssg_doc_id uo_mdid
  from    #ce_find  uo
  left join tt_mssg_doc  d  on  d.filepath = uo.filepath
                -- and d.createtime >= '2013-08-03 18:00' -- interesting ... 

    """
    
    File.open(@sqlfile, 'wb') {|f| f.write @sql }
    
  end 

  # Add Header 
  # XXXX Loop through TAB-delimited file from SQL
  # Set 4th (5th) column to be ce_filepath based on 7th (8th) uo_filepath
  def prepare_ce_filepath
    headers = @resultset[0].keys    
    headers2 = Hash[headers.zip headers]

    @resultset.each_with_index { |record, i| 
      # puts("#{i} ---- #{record}")
      record['filepath'] = uo_to_ce record['filepath']  
      # puts("#{i} ++++ #{record}") 
    }

    # Add the HEADERS after
    @resultset.insert(0, headers2)
  end 
  
  # -- Update Object: \\pft2a\ftpdrop$\mercator\transfer\schenker_na\in\orders\updateobject\=1151+1334756104+0+0=Schenker_CIS_CE_20130913003901_806_1_1.xml
  #  -- CE File:      \\pft2a\ftpdrop$\partners\schenker_na         \in\orders\event       \to_Schenker_CE\      Schenker_CIS_CE_20130913003901_806
  
  # \\pft2a\ftpdrop$\partners\schenker_na\in\orders\event\to_Schenker_CE\Schenker_CIS_CE_20130913003901_806
  
  # -- Milestone:     \\pft2a\ftpdrop$\mercator\transfer\schenker_na\in\orders\event       \=1151+1334756104+0+0=Schenker_CIS_CE_20130913003901_806_SHP_1_ms.xml
  
  # (    d.filepath = '\\pft2a\ftpdrop$\mercator\transfer\schenker_na\in\orders\updateobject\=1151+1334756104+0+0=Schenker_CIS_CE_20130913003901_806_1_1.xml'
  #   or d.filepath = '\\pft2a\ftpdrop$\partners\schenker_na\in\orders\event\to_Schenker_CE\Schenker_CIS_CE_20130913003901_806' )
  def uo_to_ce uo
    ce = uo.gsub(/=.*=/, '')
    ce = ce.gsub("mercator\\transfer\\schenker_na\\in\\orders\\updateobject\\", "partners\\schenker_na\\in\\orders\\event\\to_Schenker_CE\\")
    ce = ce.split("_")[0..-3].join("_")    # removes: _1_1.xml
    
    # \\pft2a\ftpdrop$\\partners\schenker_na\in\orders\event\to_Schenker_CE\Schenker_CIS_CE_20130913003901_806_1_1.xml
    # \\pft2a\ftpdrop$\\partners\schenker_na\in\orders\event\to_Schenker_CE\Schenker_CIS_CE_20130913003901_806_1_1.xml
    
    # Schenker_CIS_CE_20130804024248_185 -- +18
  end
end