REM For several tests in short-time, consider commenting this out for fewer sessions or not.
curl -k -c cookies.txt -L "https://demo.gtnexus.com/login.jsp?login=jatherton2&password=SaaS_2010" 

curl -k -b cookies.txt -F "selectMsgType=5" -F "fileinput=@c:\gt\demo\543777_test.xml" -L "https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet?selectMsgType=5"

REM curl -k -b cookies.txt -L "https://demo.gtnexus.com/desk/welcome.jsp"
REM curl -k -b cookies.txt -L "https://demo.gtnexus.com/sysmgmt/sm0.jsp"
REM curl -k -b cookies.txt -L "https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet" --form fileinput=c:\gt\demo\543777_test.xml --form selectMsgType=5
REM order of 2 -F statements mattered because of code in Servlet ... but this works!!

