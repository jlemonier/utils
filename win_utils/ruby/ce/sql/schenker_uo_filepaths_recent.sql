	select top 177 d.mssg_doc_id uo_mssg_doc_id, d.filepath
	from   tt_mssg_doc d
	where  1 = 1
		and d.filepath like '\\pft2a\ftpdrop$\mercator\transfer\schenker_na\in\orders\updateobject\%Schenker_CIS_CE%'
		and d.mssg_config_id = 4258	-- Update Object for Schenker -- TODO - confirm ONLY one
		and d.createtime >= getdate() - 2  -- '2013-09-14 10:00'