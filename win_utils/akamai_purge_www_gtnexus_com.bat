SET AK_USER=jason.lemonier@gtnexus.com
SET AK_PASS=Cache.Crazy.789

ECHO AK_USER:%AK_USER%
ECHO AK_PASS:%AK_PASS%

curl https://api.ccu.akamai.com/ccu/v2/queues/default -k -H "Content-Type:application/json" -d @akamai_purge_gtnexus.com.json -u %AK_USER%:%AK_PASS%
