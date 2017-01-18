=begin

if we had data like the below:

REF*CR*Closed*ReleaseStatus

It would be a Close

BEG*05*ZZ*A107703279*20130316090619*20130315*814001-ZAI-11-A107703279

=EITHER(
                IF(LOOKUP(Ref# Element:REF Segment:Transaction WHERE 
                                Desc'n Element:REF Segment:Transaction = "ReleaseStatus") = "Closed", "Close"),
                IF(TSPurpCd Element:BEG Segment:Transaction = "00", "Create"),
                IF(TSPurpCd Element:BEG Segment:Transaction = "01", "Cancel"),
                IF(TSPurpCd Element:BEG Segment:Transaction = "05", "Update"),
                NONE
                    )

					
\\pft2a\cyclone\in\CatchAll\ZZTCEdiId\850					
=end

require 'find'
require 'pathname'

start = Time.now
# adidas PO Dir
dir = "\\\\pft2a\\cyclone\\in\\CatchAll\\ZZTCEdiId\\850"
# dir = "E:\\GT\\Bugs\\Adidas_PO_Pipe\\SampleEDI"

i = 0
Find.find(dir) { |f| 
	fn = File.basename f
	next if File.directory?(f)
	i += 1

	data = File.read(f)
	# print "\n\n#{f} \n"
	sections = data.split("~")
	sections.each_with_index do |sec, s|
		if s < -300
			print "		#{fn}:#{s} \n"
			print "			#{sec[0,100]} \n"
		end
		# sec: BEG*05*ZZ*0107652834*20130318170801*20130227*804028-ZAI-11-0107652834
		# 05 is purpose code, 0107652834 is PO #

		if sec.start_with? "BEG"
			beg = sec.split("*") 
			purpose,ponum = beg[1], beg[3]
			now = Time.now
			print "#{fn},#{i},#{ponum},#{purpose},#{File.mtime(f)},#{f},#{now-start} seconds elapsed for parsing,\n"
		end

		
	end
	
	# break if i > 10
}



=begin

ISA*00*          *00*          *ZZ*TCEdiId        *ZZ*GTNEXUS        *130316*0911*^*00406*009810382*0*P*\~GS*PO*TCEdiId*ADIDAS*20130316*0911*9810382*X*004060~ST*850*0001~BEG*05*ZZ*0107629725*20130316210512*20130227*514010-ZAI-11-0107629725~CUR*BY*USD~REF*ZZ*10214201143*ORDERUID~REF*CR*A13F02858-100*CustomerOrderNumber~REF*CR*2013-03-16*PoBatchDate~REF*CR*T001Y269.001*SubsidiaryId~REF*CR*50*DistributionChannel~REF*CR*0502*ClientNumber~REF*CR*514010*CustomerNumber~REF*CR*APU002*FactoryNumber~REF*CR*2013-03-16*LastUpdateDate~REF*CR*001*PurchasingGroupCode~REF*CR*Released*ReleaseStatus~REF*CR*1002*PurchasingOrganization~REF*CR*APU002*OriginalFactory~REF*CR*00090*ProductionLeadTime~REF*CR*2013-05-31*PlanDate~REF*CR*P2*ClassCode~REF*CR*2013-04-30*CustomerRequestDate~REF*CR*GR*CustomCountryForTax~REF*CR*EL094410037*VatNumber~REF*CR*A13F02858-100*ErpOrderNumber~REF*CR*0000000113327723*IdocNumber~REF*CR*N*ShasOrder~REF*CR**ShasReady~REF*CR*Other VAS/SHAS Customer*CustomerType~REF*CR**ShasCustomer~REF*CR*A-Grade (M1&M2)*OrderTypeDescription~REF*CR**RetailerDepartmentNumber-Hidden~REF*CR**RetailerDescription-Hidden~REF*CR*Scan & Pack*Workflow~REF*CR*false*AllowMixedPoPacking~REF*CR*GLBUCC0001*LabelID~REF*CR*CNYTN*PortOfLoading~REF*CR**AccountNumber~REF*CR*Damco*LspAdidasCode~REF*CR*Bulk*Classification~REF*CR*Y*Integrated3pl~REF*CR*true*MultipleContainers~REF*CR*GRPIR*PortOfDischarge~REF*CR*P1*CustomerSizeRun-Hidden~REF*CR*M*Gender-Hidden~REF*CR*E*BarcodeType-Hidden~REF*CR**TotalCartonPieces-Hidden~REF*CR**NumberOfCartons-Hidden~REF*CR**NumberOfUnits-Hidden~REF*CR**CaseLotText-Hidden~REF*CR**CaseLot2Text-Hidden~REF*CR**CaseLot2Qty-Hidden~REF*CR**CaseLot2Ratio-Hidden~REF*CR**CaseLot3Text-Hidden~REF*CR**CaseLot3Qty-Hidden~REF*CR**CaseLot3Ratio-Hidden~REF*CR**CaseLot4Text-Hidden~REF*CR**CaseLot4Qty-Hidden~REF*CR**CaseLot4Ratio-Hidden~REF*CR**CaseLot5Text-Hidden~REF*CR**CaseLot5Qty-Hidden~REF*CR**CaseLot5Ratio-Hidden~REF*CR*03*Classification-Hidden~REF*CR*00010*GpsItemLineNumber-Hidden~REF*CR*0051*ConfirmationDelay-Hidden~REF*CR**PoExtendedDataStatusIndicator-Hidden~REF*CR*--*DeliveryDelay-Hidden~REF*CR**PriorityIndicator-Hidden~REF*CR**ShasCodeNonUs-Hidden~REF*CR*T4*TechnicalNotation-Hidden~REF*CR*CON12 PES SUIT*ModelName-Hidden~REF*CR*ZU115*ModelNumber-Hidden~REF*CR*02*Division-Hidden~REF*CR*11*Brand-Hidden~REF*CR*T2060101*WorkingNumber-Hidden~REF*CR*11*ShippingInstruction-Hidden~REF*CR*2013-05-31*FirstProductionDate-Hidden~REF*CR*2013-05-31*LastProductionDate-Hidden~REF*CR*2013-05-31*Podd-Hidden~REF*CR*--*BusinessModelAttribute-Hidden~REF*CR*06*Category-Hidden~REF*CR*2013-05-31*PoStatisticalDeliveryDate-Hidden~REF*CR*UNIRED/BLACK/WHT*MaterialColorDescription-Hidden~REF*CR*DE*ZZCUST_CNTRY_Hidden~REF*CR*0064*ConfirmationDelayPd_Hidden~REF*CR**DeliveryDelayPd_Hidden~REF*CR*CON12 PES SUIT      UNIRED/BLACK/WHT*articleName-Hidden~REF*CR*X16869*articleNumber-Hidden~REF*CR*--*PoDelUpdateDelay-Hidden~REF*CR*GR*DestinationCountry_Hidden~REF*CR**CustomerSizeRunDesc-Hidden~REF*CR*Bulk*OrderGroup-Hidden~REF*CR**Region-Hidden~REF*CR*ADIDAS*BrandDescription-Hidden~REF*CR*FOOTBALL/SOCCER*SportsDescription_Hidden~REF*CR*false*TiCritical~REF*CR*514010*CustomerNumber-Hidden~REF*CR*ZAI*OrderType~FOB*CC***01*FOB*UN*CNYTN~ITD*38***********BVO4~DTM*003*20130227~DTM*001*20130615~DTM*AAH*20130316~TD5****S~TD4*OPT***Is Partial Shipment Allowed*Y~TD4*TS***Is Transshipment Allowed*Y~N1*BY*Mediterranean Logistics S.A.*94*514010~N3*Thessi Rikia~N4*Aspropirgos**19300*GR~REF*CR**Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*DP*514010~N1*SE*Bowker Asia Ltd.*94*APU~N3*481 Castle Peak Road~N4*Hong Kong***HK~REF*CR* Block B, 6/F Hong Kong Spinners In*Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*DP*APU~PER*AJ****TE*+852 3156 2829*FX*+852 3156 2827~N1*AG*adidas LO Guangzhou*94*001~N3*12/F DongShan Plaza*69 Xianlie Road Central~N4*Guangzhou***CN~N1*CN*adidas Hellas~N3*112 Vouliagmenis str & 1 Zamanou*Glyfada~N4*Athens**16674*GR~REF*CR*CustomsCnsgee*AdidasRoleCode~PER*AJ*Mademtzidi Despoina***TE*0030-210-89-30-800*FX*0030 210 96 90 070~N1*O2*Bowker Asia Ltd./China*94*APU002~N3*380-388 He Yuan Wide Road~N4*Guangdong**517000*CN~REF*CR* He Yuan*Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*DP*APU002~N1*N1*Mediterranean Logistics S.A.~N3*Thessi Rikia*Aspropirgos~N4*Attiki**19300*GR~REF*CR*NotifyParty1*AdidasRoleCode~PER*AJ*Mrs Potiraki Katerina***TE*(+30) 2111808400*FX*(+30) 2111808423~N1*N2*Mediterranean Logistics S.A.*94*default~N3*Thessi Rikia~N4*Aspropirgos**19300*GR~REF*CR**Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~N1*ABE*adidas Hellas S.A.*94*610~N2*c/o adidas Int'l Trading B.V.~N3*Hoogoorddreef 9a~N4*Amsterdam ZO**1101 BA*NL~REF*CR*Atlas Arena, Afrika Building*Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*CR*ZA*AdidasRoleCode~REF*CR*empty*AdidasAltId~REF*CR**ContactPosition~REF*DP*610~N1*ABE*adidas Hellas S.A.*94*004800~N2*ATRINA CENTER, 6TH FLR~N3*38-40, 26TH OCTOBER STR~N4*THESSALONIKI**54627*GR~REF*CR**Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*CR*ZB*AdidasRoleCode~REF*CR*empty*AdidasAltId~REF*CR**ContactPosition~REF*DP*004800~N1*ABE*adidas Hellas*94*none~N3*112 Vouliagmenis str & 1 Zamanou*Glyfada~N4*Athens**16674*GR~REF*CR*TransportConsignee*AdidasRoleCode~REF*CR*empty*AdidasAltId~REF*CR**ContactPosition~PER*AJ****TE*0030-210-89-30-800*FX*0030 210 96 90 070~N1*ST*GL_BND_MEDLOG 3PL BONDE*94*514010~N3*Thessi Rikia*-~N4*ASPROPYRGOS**19300*GR~REF*CR**Name3~REF*CR**Name4~REF*CR**PoBox~REF*CR**Floor~REF*CR*empty*AdidasAltId~REF*DP*514010~PO1*0107629725-X16869-00*100*PC*13.763**IN*X16869*GE*CON12 PES SUIT      UNIRED/BLACK/WHT*CH*CN~REF*55*0001~REF*CR*P1*CustomerSizeRun~REF*CR*M*Gender~REF*CR*E*BarcodeType~REF*CR**TotalCartonPieces~REF*CR**NumberOfCartons~REF*CR**NumberOfUnits~REF*CR**CaseLotText~REF*CR**CaseLot2Text~REF*CR**CaseLot2Qty~REF*CR**CaseLot2Ratio~REF*CR**CaseLot3Text~REF*CR**CaseLot3Qty~REF*CR**CaseLot3Ratio~REF*CR**CaseLot4Text~REF*CR**CaseLot4Qty~REF*CR**CaseLot4Ratio~REF*CR**CaseLot5Text~REF*CR**CaseLot5Qty~REF*CR**CaseLot5Ratio~REF*CR*03*Classification~REF*CR*00010*GpsItemLineNumber~REF*CR*0051*ConfirmationDelay~REF*CR**PoExtendedDataStatusIndicator~REF*CR**DeliveryDelay~REF*CR**PriorityIndicator~REF*CR**ShasCodeNonUs~REF*CR*T4*TechnicalNotation~REF*CR*CON12 PES SUIT*ModelName~REF*CR*ZU115*ModelNumber~REF*CR*02*Division~REF*CR*11*Brand~REF*CR*T2060101*WorkingNumber~REF*CR*11*ShippingInstruction~REF*CR*2013-05-31*FirstProductionDate~REF*CR*2013-05-31*LastProductionDate~REF*CR*2013-05-31*Podd~REF*CR**BusinessModelAttribute~REF*CR*06*Category~REF*CR*2013-05-31*PoStatisticalDeliveryDate~REF*CR*UNIRED/BLACK/WHT*MaterialColorDescription~REF*CR*DE*ZZCUST_CNTRY~REF*CR*0064*ConfirmationDelayPd~REF*CR**DeliveryDelayPd~REF*CR**PoDelUpdateDelay~REF*CR*GR*DestinationCountry~REF*CR**CustomerSizeRunDesc~REF*CR**Region~REF*CR*ADIDAS*BrandDescription~REF*CR*FOOTBALL/SOCCER*SportsDescription~REF*CR*514010*CustomerNumber~REF*CR*0107629725-X16869-00010*ItemKey~DTM*038*20130531~TD5****S~TXI*TX**0******MO~N1*ST*GL_BND_MEDLOG 3PL BONDE~SLN*0001**I*30*PC*13.73***IZ*4*EN*4051932612751~N9*55*0001~N9*CR*46*ManufacturingSize~N9*CR*611212000000*HtsCode1~N9*CR**Ifi1~N9*CR*TRACK SUITS;KNIT;OF SYNTHETIC FIBRES*TariffDescription1~N9*CR*073*Quota1~N9*CR*19*TechnicalPrintIndex~N9*CR*30*Zzmti2~N9*CR*0001*GpsScheduleLineNumber~N9*CR*360*GpsThreeDigitSize~N9*CR*4051932612751*Upc-Hidden~N9*CR*0107629725-X16869-00010-0001-360*ItemKey~SLN*0002**I*40*PC*13.73***IZ*5*EN*4051932612768~N9*55*0002~N9*CR*48*ManufacturingSize~N9*CR*611212000000*HtsCode1~N9*CR**Ifi1~N9*CR*TRACK SUITS;KNIT;OF SYNTHETIC FIBRES*TariffDescription1~N9*CR*073*Quota1~N9*CR*21*TechnicalPrintIndex~N9*CR*32*Zzmti2~N9*CR*0002*GpsScheduleLineNumber~N9*CR*380*GpsThreeDigitSize~N9*CR*4051932612768*Upc-Hidden~N9*CR*0107629725-X16869-00010-0002-380*ItemKey~SLN*0003**I*20*PC*13.73***IZ*6*EN*4051932612775~N9*55*0003~N9*CR*50*ManufacturingSize~N9*CR*611212000000*HtsCode1~N9*CR**Ifi1~N9*CR*TRACK SUITS;KNIT;OF SYNTHETIC FIBRES*TariffDescription1~N9*CR*073*Quota1~N9*CR*23*TechnicalPrintIndex~N9*CR*34*Zzmti2~N9*CR*0003*GpsScheduleLineNumber~N9*CR*400*GpsThreeDigitSize~N9*CR*4051932612775*Upc-Hidden~N9*CR*0107629725-X16869-00010-0003-400*ItemKey~SLN*0004**I*10*PC*14.06***IZ*7*EN*4051932612782~N9*55*0004~N9*CR*52*ManufacturingSize~N9*CR*611212000000*HtsCode1~N9*CR**Ifi1~N9*CR*TRACK SUITS;KNIT;OF SYNTHETIC FIBRES*TariffDescription1~N9*CR*073*Quota1~N9*CR*25*TechnicalPrintIndex~N9*CR*35*Zzmti2~N9*CR*0004*GpsScheduleLineNumber~N9*CR*410*GpsThreeDigitSize~N9*CR*4051932612782*Upc-Hidden~N9*CR*0107629725-X16869-00010-0004-410*ItemKey~CTT*1~AMT*TT*1378.02~SE*301*0001~GE*1*9810382~IEA*1*009810382~

=end
