curl -k -c cookies.txt -L "https://demo.gtnexus.com/login.jsp?login=jatherton2&password=SaaS_2010"  
REM Login completed, cookies saved. 

curl -k -b cookies.txt -F "selectMsgType=5" -F "fileinput=@c:\gt\demo\V1\546732.xml" -L "https://demo.gtnexus.com/servlet/ProcessInboundXMLServlet?selectMsgType=5" 2>> postResults.err >> postResults.log
