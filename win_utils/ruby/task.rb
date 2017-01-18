require 'time'


class Task
	def initialize(hash)
		@h = hash
	end
	
	def starttime
		parse_date @h['starttime']
	end
	def endtime
		parse_date @h['endtime']
	end
	def server
		"#{@h['servername']} "
	end
	def time2
		"FROM: #{starttime} TO: #{endtime} - #{server} - id=#{id} "
	end
	def id
		"#{@h[@h.keys[0]]}"
	end
	
	def key
		"#{@h['module']}||#{@h['submodule']}"
	end
	
	def name
		"#{@h['module']}/#{@h['submodule']}"
	end
	
	def sql 
		"select system_stat_id, module, submodule, starttime, endtime, createtime, modtime, stat_type_id, src from tt_system_stat where system_stat_id in (#{t1.id}, #{t2.id})"
	end
	
	def overlap
		"#{t2.starttime-t1.endtime}" rescue ' ? '
	end
	
	def prevTask
		@prevTask
	end
	
	# return nil if NO overlap
	def print_overlap_info(prevTaskParam)
		@prevTask ||= prevTaskParam
		prevEnd  = prevTask.endtime
		curStart = self.starttime

		if prevEnd.to_s.size < 1
			print "\nFound previous task NEVER COMPLETED.  Likely due to system restart: #{self.name}  \n\t#{t1.time2} \n\t#{t2.time2} \n"
			print sql
		elsif curStart < prevEnd
			print "\nFound overlapping task: #{self.name}  \n\t#{t1.time2} DID NOT FINISH before task below started \n\t#{t2.time2}"
			print "\n\t\t 2nd task started too early by: #{overlap} seconds \n"
			print "\t#{sql}\n"
			
			return 1
		end
		return 0
	end
	
	private
	
	def parse_date(s, format = "%F %T")
		# DateTime.parse(s, format)
		Time.parse(s) rescue nil
	end

	# Quick reference to t1 or 1st task
	def t1
		prevTask
	end
	# Quick reference to t2 or 2nd task
	def t2
		self
	end
	
end
