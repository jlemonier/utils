# List all jar files into text file for searching

class JarDirs
	def add name, dir
		@dirs << [name, dir]
	end
	
	def to_s
	
	end
end


class CacheJarInfo
	def initialize jar_dirs, work_dir
		@jd = jar_dirs
		@work_dir = work_dir
	end
	
	def refresh
		print jarDirs
	end
	
	
end


jarDirs = JarDirs.new
jarDirs.add "C:/src/agile_13_7/release/lib", 

cji = CacheJarInfo.new jarDirs, "c:/src/jarinfo"
cji.refresh
cji.find

