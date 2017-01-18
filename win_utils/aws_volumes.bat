@echo off
cls
title aws volume check

e:
cd \code\projects\PRODOPS\ops\aws\ec2_describe

python aws_volumes.py


