-- VF Analysis Temp

	-- and vdsa.upc is not null	-- UPC is not always there?  Need help from SO team
	-- and t.upc is null			-- Shows assortments that should probably not exist with quantity > 0

	-- and t.ShippingOrderNumber in ('7000025106')
	-- and vd.shippingordernum in ('7000025106')
	-- order by 

-- select * from #tmp t where t.ShippingOrderNumber in ('7000025106')
-- select * from tt_om_org_invoicestatus
if 1=2 begin
	select top 3 * from tt_om_vendordoc				order by 1 desc
	select top 3 * from tt_om_vendordoc_lineitem	order by 1 desc
	select top 3 * from tt_om_vendordoc_sku			order by 1 desc
	select * from tt_om_prod where code in ('RB1116') -->> om_prod_id => 3272854
end

end

-- Invoice Analysis
if 3=3 begin



	-- 4838 VF vdoc_sku db<==>xml rows have duplicate assortments
	select om_invoice_id, invoicenum, shippingordernum, vdocline_objidkey, color, size, dimension
		, count(*) rows
		, max(om_vendordoc_sku_id) sku_id_max
		, min(om_vendordoc_sku_id) sku_id_min
		, max(qty_sku) qty_max
		, min(qty_sku) qty_min

		, max(quantity_so_xml) qty_so_xml_max
		, min(quantity_so_xml) qty_so_xml_min
		
		, max(filename)	filename_mssgdocid_max
		, min(filename) filename_mssgdocid_min
		from #vf
		group by om_invoice_id, invoicenum, shippingordernum, vdocline_objidkey, color, size, dimension
		having count(*) > 1 and 
			max(quantity_so_xml) <> min(quantity_so_xml)
		order by count(*) desc


select top 3 * from #vf

	-- Copy, make distinct list
	-- select * into #tmp2	from #tmp

	-- 80601573.xml
	select top 10 CommercialInvoiceNumber, upc, quantity, sku, ShippingOrderNumber, PurchaseOrderNumber, ItemNumber, Color, Size, Dimension, * 
		from #tmp2 t
		where CommercialInvoiceNumber in ('7000025053')
		and   t.upc in ('618935244798')
		order by t.CommercialInvoiceNumber, t.upc, t.ShippingOrderNumber, t.PurchaseOrderNumber, t.ItemNumber, t.Color, t.Size, t.Dimension

	select * from #vf 
		where invoicenum in ('7000025053')		
		and   upc in ('618935244798')

	select CommercialInvoiceNumber, ShippingOrderNumber, PurchaseOrderNumber, ItemNumber, Color, Size, Dimension
		, count(*)
		from #tmp
		group by CommercialInvoiceNumber, ShippingOrderNumber, PurchaseOrderNumber, ItemNumber, Color, Size, Dimension
		having count(*) > 1
		
/*
tmp_id	Color	CommercialInvoiceNumber	Dimension	Firs
tCostPrice	FullHTSNumber	ItemNumber	MsgRecipient	MsgSender	PurchaseOrderNumber	Quantity	ShippingOrderNumber	Size	Sku	Status	TransportationMode	UPC	filename
38862	NAVY	5010165897	.	4.65	6404199000	VEE0NVY	VFC	VFCNGCEU	V160251	18	5010165897	105	VEE0NVY-NAVY-105-.	Submitted	Ocean	700051694806	93556678.xml
38863	NAVY	5010165897	.	4.65	6404199000	VEE0NVY	VFC	VFCNGCEU	V160251	42	5010165897	115	VEE0NVY-NAVY-115-.	Submitted	Ocean	715752002034	93556678.xml
	*/

	-- select top 10 * from tt_om_invoicememo order by 1 desc
	-- select top 3 * from #vf
	-- select top 3 * from #vf where quantity_so_xml is null

	select t.shippingordernumber, db.shippingordernum
		from #tmp t

	-- drop table #vf_so_db_list

	select distinct shippingordernumber into #vf_so_db_list from #tmp
	insert into #vf_so_xml_list select token 


	select count(distinct shippingordernumber) xml_so_count from #tmp	-- 2783 in xml
	select count(distinct shippingordernum) db_so_count from #vf		-- 2750 SOs

	select count(*) db_asst_count from #vf  
	select count(*) xml_asst_count from #tmp

	select count(distinct shippingordernum) vf_so_count
		, count(*) vf_asst_count from #vf where quantity_so_xml is null

	select top 3 * from #vf
	select top 3 * from #tmp
	/*
	om_invoice_id	invoicenum	shippingordernum	quantity_sku_asst	qty_sku	quantity_so_xml	gross_amt_sku_asst	size_vd_sku_asst	size_so_xml	color_sku_asst	color_so_xml	dim_sku_asst	dim_so_xml	firstCost_so_line	firstCostPrice_inv_xml	om_org_invoicestatus_id	invstatus	invstatus_code	ispaymentprocessed	gross_amt	filename	paymentid	endtoendid	customs_amt	net_amt	discount_amt	claim_amt	om_vendordoc_id	om_vendordoc_lineitem_id	om_vendordoc_sku_id	om_assortment_id
	595126	123658	123658	416	421	NULL	1763.99	L	NULL	671A	NULL	NULL	NULL	4.19	NULL	2	Documents Presented	002	0	126611.87	NULL	NULL	NULL	126611.87	126611.87	0	0	649499	4518786	6450490	17883551
	595126	123658	123658	258	247	NULL	1034.93	M	NULL	671A	NULL	NULL	NULL	4.19	NULL	2	Documents Presented	002	0	126611.87	NULL	NULL	NULL	126611.87	126611.87	0	0	649499	4518786	6450491	17883552
	595126	123658	123658	116	110	NULL	460.9	S	NULL	671A	NULL	NULL	NULL	4.19	NULL	2	Documents Presented	002	0	126611.87	NULL	NULL	NULL	126611.87	126611.87	0	0	649499	4518786	6450492	17883553
	*/
	-- select shippingordernum, 

	select count(*) vf_so_xml_asst_count from #tmp 
	select * from #vf where quantity_so_xml is null

	-- Current Invoice Amount
	select a.invoicenum
		, count(distinct om_vendordoc_sku_id) skus_db
		-- , sum(distinct om_vendordoc_sku_id) skus_db
		, sum(gross_amt_sku_asst) gross_amt_current
		, sum(b.gross_amt_xml)
		
		from #vf a
		left join (
			-- Correct Invoice Amount
			select invoicenum, count(distinct om_vendordoc_sku_id) skus_xml, sum(gross_amt_sku_asst) gross_amt_xml
				from #vf
				where quantity_so_xml is null
				group by invoicenum
		) b on b.invoicenum = a.invoicenum
		
		group by a.invoicenum

end