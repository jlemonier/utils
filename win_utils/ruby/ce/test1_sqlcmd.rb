require './sqlcmd'

Sqlcmd.new.run_sql_file 'mssg', './sql/select_10_md.sql'

Sqlcmd.new.run_sql_file 'mssg', './sql/schenker_uo_filepaths_recent.sql'


