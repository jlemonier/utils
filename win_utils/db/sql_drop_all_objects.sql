-- select 'drop procedure msen.'+name+' -- \n go', *	-- had msen instead of dbo
/*

select 'drop view '+name+' -- \n go', * 
	from sysobjects where (name like 't%_' or name like 'ts_%') and xtype = 'V'

-- Foreign Keys before Tables
select 'alter table '+tbl.name+ ' drop constraint '+fk.name+' -- \n go', * 
	from		sysobjects fk 
	inner join	sysobjects tbl on tbl.id = fk.parent_obj
	where fk.xtype in ( 'F'
	and   tbl.category = 0	-- 2 is System Table

-- Tables
select 'drop table ['+u.name+'].['+o.name+']; -- go', * 
	from		sysobjects o 
	inner join	sysusers   u on u.uid = o.uid
	and   o.category = 0	-- 2 is System Table
	where xtype = 'U'
	order by o.uid, o.name

select 'drop function ['+u.name+'].['+o.name+']; -- go', * 
	from		sysobjects o 
	inner join	sysusers   u	on	u.uid = o.uid	
								and o.category = 0	-- 2 is System Table
	where xtype in ('FN','TF', 'IF')
	order by o.uid, o.name

select 'drop synonym ['+u.name+'].['+o.name+']; -- go', * 
	from		sysobjects o 
	inner join	sysusers   u	on	u.uid = o.uid	
								and o.category = 0	-- 2 is System Table
	where xtype in ('SN')
	order by o.uid, o.name


-- Anything left that is not system related?
select p.*, o.* 
	from		sysobjects o 
	left join	sysobjects p on p.id = o.parent_obj
	where 1=1
	-- and   o.xtype not in ('U','P','V','S')
	and   o.category not in (2)
	and   p.category not in (2)

*/

