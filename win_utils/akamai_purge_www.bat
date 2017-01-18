@ECHO ON
@CLS
@REM https://jira.gtnexus.info/browse/ITOP-6241
@REM https://api.ccu.akamai.com/ccu/v2/docs/
@REM Requires setting %AK_USER% & %AK_PASS% as environment variables.
@REM -k required since we are setting SSL errors. ?

@REM curl https://api.ccu.akamai.com/ccu/v2/queues/default    -H "Content-Type:application/json" -d '{"type":"cpcode", "objects":["144241","144242"]}' -u %AK_USER%:%AK_PASS%

SET AK_USER=gtnexus_akamai_web
SET AK_USER=jason.lemonier@gtnexus.com
SET AK_USER=\\_sysops@gtnexus.com

SET AK_PASS=%AK_PASS%

ECHO AK_USER:%AK_USER%
ECHO AK_PASS:%AK_PASS%

curl https://api.ccu.akamai.com/ccu/v2/queues/default -k -H "Content-Type:application/json" -d @akamai_purge_gtnexus.com.json -u %AK_USER%:%AK_PASS%

@REM Windows fails with curl due to ' " {" vs {\" etc
@REM curl https://api.ccu.akamai.com/ccu/v2/queues/default -k -H "Content-Type:application/json" -d '{ "type" : "cpcode", "objects" : [ "144241" , "144242" ] }' -u %AK_USER%:%AK_PASS%
@REM curl https://api.ccu.akamai.com/ccu/v2/queues/default -k -H "Content-Type:application/json" -d '{"type":"cpcode", "objects":["144241"]}' -u %AK_USER%:%AK_PASS%
@REM curl https://api.ccu.akamai.com/ccu/v2/errors/unauthorized-cpcode -k -u %AK_USER%:%AK_PASS%