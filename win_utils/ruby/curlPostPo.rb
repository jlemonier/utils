require "tmpdir"
# make 600 copies of each
dirs = ["c:\\gt\\demo\\V1", "c:\\gt\\demo\\V2"]

po_re = /<OrderNumber>(.*)<\/OrderNumber>/

fcurl = File.new("demo1200.bat", "w")
line = 'curl -k -c cookies.txt -L "https://demo.gtnexus.com/login.jsp?login=jatherton2&password=SaaS_2010" -o postResults.log '
fcurl.write("#{line} \nREM Login completed, cookies saved. \n\n" )

## 546731
## 577671
ponums = [546731, 577671 ]
pokey = /XXXXXXXXXX/
i = -1
dirs.each do |dir|
  i = i + 1
  startpo = ponums[i%ponums.length]
  print "#{dir} i=#{i} startpo=#{startpo} \n"
  
  Dir.chdir(dir)
  Dir.glob("template*").each do |f|
    fn = [dir, f].join("\\")
    puts f, fn
    data = File.new(fn).read
    (1..600).each do |xx|
      ponum = startpo + xx
      print "Create #{ponum} \n"
      data2 = data.sub pokey, ponum.to_s
      
      fnpo  = "#{ponum}.xml"
      f = File.new(fnpo, "w")
      f.write(data2)
      f.close

      line = "echo Posting #{fnpo} \n  curl -k -b cookies.txt -F \"selectMsgType=5\" -F \"fileinput=@#{dir}\\#{fnpo}\" -L \"https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet?selectMsgType=5\" -o postResults.log  \n\n"
      fcurl.write(line)
    end
    
    # po = po_re.match(data)
    
  end
  
end


=begin
REM For several tests in short-time, consider commenting this out for fewer sessions or not.
curl -k -c cookies.txt -L "https://demo.gtnexus.com/login.jsp?login=jatherton2&password=SaaS_2010"


curl -k -b cookies.txt -F "selectMsgType=5" -F "fileinput=@c:\gt\demo\543777_test.xml" -L "https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet?selectMsgType=5"
=end