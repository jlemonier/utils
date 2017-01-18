module StringTools
  
  def remove_whitespace s
    s.gsub!(/\s+/, "") if s
    s
  end

end