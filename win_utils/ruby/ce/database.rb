
class Database
  attr_accessor :dbkey, :server, :dbname

  def self.init
    return if @databases
    @databases = {}
    @databases["mssg"] = Database.new('mssg', 'pdb1a'   , 'mssg_newtradmarket')
    @databases["pnet"] = Database.new('pnet', 'pnetdb1a', 'newtradmarket')
  end

  def to_s
    "#{server}.#{dbname}"
  end
  
  def self.lookup dbkey
    self.init
    return @databases[dbkey]
  end

  def initialize dbkey, server, dbname
    @dbkey = dbkey
    @server = server
    @dbname = dbname
  end  
  
end