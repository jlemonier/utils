
class Tools::TextTools  ## < ActiveRecord::Base

  def self.text2html data
    Rails.logger.info "Here *****"
    result = ""
    data ||= ""
    data.split("\n").each_with_index do |row, i|
      result += "\n  <tr>"
      tag = (i == 0) ? "th" : "td"
      row.split(/\s+/).each do |cell|
        cell = cell.strip
        result += "\n    <#{tag}>#{cell}</#{tag}>" 
      end
      result += "\n  </tr>"
    end
    Rails.logger.info result
    result
    
  end

end