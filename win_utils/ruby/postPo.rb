#
require 'rest_client'

def stripHtml(s)
  s.gsub!(/(<[^>]*>)|\n|\t/s) {" "}
  return s
end

def pageinfo(s)
  s.split("\n").each { |line| puts "#{line}" if line =~ /title/  }
end

def printit (x)
  # print "#{stripHtml(x)} \n"
  print "#{x} \n"
end

def post(url, params, cookies)
  begin
    r2 = RestClient.post(login, fields, :cookies => cookies) 
    printit (r2.cookies)
    pageinfo (r2)
  rescue => e
    pageinfo (e.response)
  end  
end

def get(url, params = {}, cookies = {})
  r1 = RestClient.get url
  cookies = r1.cookies
  print "\n#{url} => #{cookies} \n\n"
  pageinfo (r1)
  
end

# get1 = RestClient.get 'http://gemtacular.com/gems'
# print "#{get1[0]}"

xmlFile = 'C:\\GT\\demo\\543777_test.xml'

demo = "https://demo.gtnexus.com/"
login = "#{demo}login.jsp"
sm0 =   "#{demo}sysmgmt/sm0.jsp"
ibxml = "#{demo}servlet/ProcessInboundXMLServlet"

fields = {}
fields["login"] = "jatherton2"
fields["password"] = "SaaS_2010"
fields["selectMsgType"] = "5"
# fields["fileinput"] = File.new(xmlFile)

get(login)
get(login)
=begin
  r1 = RestClient.get login
  cookies = r1.cookies
  printit (r1.cookies)
  pageinfo(r1)
=end

fields["fileinput"] = File.new(xmlFile)

r2 = RestClient.post(
  ibxml,
  fields,
  {:cookies => cookies}
)
pageinfo(r2)

if false
  response = RestClient.get 'http://example.com/action_which_sets_session_id'
  response.cookies
  # => {"_applicatioN_session_id" => "1234"}

  response2 = RestClient.post(
    'http://localhost:3000/',
    {:param1 => "foo"},
    {:cookies => {:session_id => "1234"}}
  )
end
# r3 = RestClient.post ibxml, fields, cookies 
# printit(r3)

# fields2 = 
# fields2.merge(:fileinput => File.new(xmlFile))
# resource.put :login => "jatherton2", :password => "Saas_2010"
=begin
rc = RestClient.post 'https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet/', fields
print "#{rc}"
=end
=begin
  for x in 1..3 do
    print "#{x}\n"
  end
  
  (1..50).each do |x|
    x2 = x*x
    print "#{x} => #{x2} \n"
  end
=end



