
class Tools::PropTools
  attr_accessor :lines, :props
  
  def initialize fn
    @filename = fn
    
    @lines = []
    @props = {}
    
    File.open(@filename).each do |line|
      @lines << line
      
      k,v = line.split('=')
      v = v.to_s.strip
      @props[k] = v
    end
  end
  
  def dml
    eff = '2012-01-01'
    prefix = 'qaa'
    
    result = []
    @props.each do |k,v|
      result << "exec tp_property_add 'tradiant.properties', '#{eff}', '#{k}', '#{v}', 'QAA', null, null, null"
    end
    
    result.join("\n")
    
  end
  
  
end