sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateASN1.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateASN2.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateASNmaster.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdatePO1.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdatePO2.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdatePO3.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdatePO4.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdatePOmaster.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateProcessTmp.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateSO1.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateSO2.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateSO3.sql 
sqlcmd -S pdb1a -d JitterBit -i \\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason/NegUpdateSOmaster.sql 
echo "JitterBit code deployed.  pause added at bottom of script to check for errors in console" 
pause
