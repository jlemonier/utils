require 'sql_deploy'

# class SqlDeploy
#	def initialize server, db, run_cmds = false, log_cmds = true

# Env:
	qa      = SqlDeploy.new('qadb1b', 'JitterBit_dev'	, false, true)  # ONLY Log
	preprod = SqlDeploy.new('ndb1a', 'JitterBit'		, false, true)	# ONLY Log
	prod    = SqlDeploy.new('pdb1a', 'JitterBit'		, false, true)	# ONLY Log

	# \\\\gthqfile1\Engineering\docs\QA\PatchFiles\14.5.0\P1_Patches\P1_PSO-990_JasonL_po_perf_Aug13
	
	patch_dir = %w{ \\\\gthqfile1\Engineering\docs\QA\PatchFiles\14.7.0\P1_Patches\1_tobedeployed\P1_PSO-2572_Jason }[0] 
	
	qa.add_dir 		patch_dir; 
	preprod.add_dir patch_dir; 
	prod.add_dir 	patch_dir; 
	
	qa.deploy
	preprod.deploy
	prod.deploy
	
# Need 2 extra \\ for network drives at the beginning only.
	# \\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\1_tobedeployed\P1_PSO-984-NDB1A_JitterBit_July29
	# jitterbit1.add_dir %w{\\\\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\1_tobedeployed\P1_PSO-984-NDB1A_JitterBit_July29\Step1_setup_logging}[0] 
	# jitterbit1.add_dir %w{\\\\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\1_tobedeployed\P1_PSO-984-NDB1A_JitterBit_July29\Step2_add_logging  }[0] 
	# jitterbit1.add_dir %w{\\\\gthqfile1\engineering\docs\QA\PatchFiles\14.4.0\P1_Patches\1_tobedeployed\P1_PSO-984-NDB1A_JitterBit_July29\Step3_improve_performance  }[0] 
	
	# jitterbit1.add_dir %w{ C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\proc }[0] 


# "deploy" will run or log the commands to a file
# jitterbit1.deploy

#########################################################################################################################
# Now unnecessary after setting env var: RUBYLIB=D:\utils\ruby:...
# http://stackoverflow.com/questions/6671318/understanding-rubys-load-paths
# $LOAD_PATH.unshift(File.dirname(__FILE__))
#########################################################################################################################
# jitterbit1.add_dir %w{ C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\proc }[0] 
# jitterbit1.add_dir "C:\\code\\gtnexus\\development\\modules\\main\\tradiant\\release\sql\rel\jitterbit\proc"
# jitterbit1.add_dir %w{ C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\func }[0] 
# C:\code\gtnexus\development\modules\main\tradiant\release\sql\rel\jitterbit\func
#########################################################################################################################
