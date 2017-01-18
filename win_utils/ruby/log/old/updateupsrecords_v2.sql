/****** Object:  StoredProcedure [dbo].[updateupsrecords]    Script Date: 7/10/2014 15:34:30 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

-- Creating Procedure "dbo.updateupsrecords"
CREATE PROCEDURE [dbo].[updateupsrecords]
	@upsid int, 
	@recordtype varchar(50), 
	@delimtype varchar(20), 
	@positionid int, 			-- field_info.field_position ranges from 7 => 36.  Never 1.
	@newcontent varchar(8000), 	-- 'D'
	@procover bit = 0, 			-- 0
	@retval int OUT,
	@env_suffix varchar(100)
AS

declare @reccnt integer=0;
declare @valtemp varchar(8000);

-- No need for try/catch here, cannot fail
begin try
	select 	@reccnt = count(*)  
	from 	ups_temp
	where 	record_type	= @recordtype 
	and 	ups_id 		= @upsid ;
end try
begin catch
	set @reccnt=0;
end catch

if @reccnt > 0 
begin

	select @valtemp = dbo.split_part(rtrim(record_data),@delimtype,@positionid) 
	from ups_temp
	where record_type= @recordtype 
	and ups_id = @upsid ;
	
	if @valtemp != @newcontent  or @procover = 1
	begin
		
		update ups_temp
		set record_data =             
			(case when @positionid = 1 
				  then (case when dbo.instr(rtrim(record_data),@delimtype,@positionid)=0 
				  			 then @newcontent
		                     else @newcontent+right(rtrim(record_data),len(rtrim(record_data))-(dbo.instr(rtrim(record_data),@delimtype,@positionid)-1))                    
		                end)
		          
		          when dbo.instr(rtrim(record_data),@delimtype,@positionid-1) = len(rtrim(record_data)) 
		          then rtrim(record_data)+@newcontent
		          
		          when dbo.instr(rtrim(record_data),@delimtype,@positionid) = 0 
		          then left(rtrim(record_data),dbo.instr(rtrim(record_data),@delimtype,@positionid-1))+@newcontent
		          
		          else left(rtrim(record_data),dbo.instr(rtrim(record_data),@delimtype,@positionid-1))+@newcontent+right(rtrim(record_data),len(rtrim(record_data))-(dbo.instr(rtrim(record_data),@delimtype,@positionid)-1))
		     end )
		where record_type	= @recordtype 
		and   ups_id 		= @upsid ;
	end

	set @retval = 1;

end
else 
begin

	begin try
		select @reccnt  = count(*) from ups_data_historical
		where record_type= @recordtype 
		and ups_id = @upsid ;
	end try
	begin catch
		set @reccnt=0;
	end catch

	if @reccnt > 0
	begin

		select @valtemp = dbo.split_part(rtrim(record_data),@delimtype,@positionid) 
		from ups_data_historical
		where record_type= @recordtype 
		and ups_id = @upsid ;

		if @valtemp != @newcontent or @procover = 1
		begin
			
			update ups_data_historical set env_suffix = @env_suffix where record_type= @recordtype and ups_id = @upsid ;
			insert into ups_temp select * from ups_data_historical where record_type= @recordtype and ups_id = @upsid ;

			update ups_temp
			set record_data = (case when @positionid = 1 then
			                  (case when dbo.instr(rtrim(record_data),@delimtype,@positionid)=0 then @newcontent
			                        else 
			                        @newcontent+right(rtrim(record_data),len(rtrim(record_data))-(dbo.instr(rtrim(record_data),@delimtype,@positionid)-1))                    
			                  end)
			            when dbo.instr(rtrim(record_data),@delimtype,@positionid-1) = len(rtrim(record_data)) then 
			                  rtrim(record_data)+@newcontent
			            when dbo.instr(rtrim(record_data),@delimtype,@positionid) = 0 then
			                 left(rtrim(record_data),dbo.instr(rtrim(record_data),@delimtype,@positionid-1))+@newcontent
			            else
			            left(rtrim(record_data),dbo.instr(rtrim(record_data),@delimtype,@positionid-1))+@newcontent+right(rtrim(record_data),len(rtrim(record_data))-(dbo.instr(rtrim(record_data),@delimtype,@positionid)-1))
			            end ),
			                        donotsend = 0
			where record_type= @recordtype 
			and ups_id = @upsid ;
			
			set @retval = 3;
		end
	
		set @retval= 4;
	end
	
set @retval = 5;
end

return

GO
