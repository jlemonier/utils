sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdatePO1.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdatePO2.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdatePO3.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdatePO4.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdatePOmaster.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/NegUpdateProcessTmp.sql 
sqlcmd -S qadb1b -d JitterBit_dev -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13/updateupsrecords.sql 
echo "JitterBit code deployed.  pause added at bottom of script to check for errors in console" 
pause
