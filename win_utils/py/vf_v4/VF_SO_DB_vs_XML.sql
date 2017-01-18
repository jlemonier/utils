
-- v5 csv loaded with PoLineNumber correctly - 

if 'no create #vf' = 'create #vf' begin

drop table #vf
-- Table alias

-- VF connect invoices to xml data
-- select * from tt_om_vendordoc vd where vd.shippingordernum in ('5010159481')
-- select * from tt_om_org_invoicestatus
-- select top 50 * from tt_om_vendordoc_lineitem order by 1 desc
-- select top 500 * from #tmp where CommercialInvoiceNumber in ('122866')

select 
	  inv.om_invoice_id
	, inv.invoicenum
	, vd.shippingordernum
	, vdl.om_poline_num
	, t.POLineNumber
	, vdl.vdocline_objidkey
	, vdsa.color
	, vdsa.size
	, vdsa.dimension

	-- , vdsa.upc		upc_vd_sku_asst, t.upc			upc_so_xml
	, vdsa.quantity quantity_sku_asst
	, vds.qty		qty_sku
	, t.quantity	quantity_so_xml
	, vds.gross_amt gross_amt_sku_asst
	-- , t.quantity * t.FirstCostPrice		gross_amt_so_xml_calc
	, vdsa.size		size_vd_sku_asst
	, t.size		size_so_xml
	, vdsa.color	color_sku_asst
	, t.color		color_so_xml
	, vdsa.dimension dim_sku_asst
	, t.dimension   dim_so_xml

	, t.upc			upc_so_xml
	-- , t.color		color_inv_xml

	, vdl.firstcost		firstCost_so_line
	, t.FirstCostPrice	firstCostPrice_inv_xml

	-- , t.ShippingOrderNumber
	, inv.om_org_invoicestatus_id
	, st.name invstatus
	, st.code invstatus_code
	, inv.ispaymentprocessed
	, inv.gross_amt

	, t.filename
	-- , pmtinfo.paymentid, pmtinfo.endtoendid
	
	, inv.customs_amt
	, inv.net_amt
	, inv.discount_amt
	, inv.claim_amt

	, vd.om_vendordoc_id
	, vdl.om_vendordoc_lineitem_id
	, vds.om_vendordoc_sku_id
	, vdsa.om_assortment_id
	-- , 'vd table' vd_table, vd.*
	-- , 'vd line' vd_line, vdl.*
	-- , 'vd sku' vd_sku, vds.*
	-- , 'vd sku asst' vd_sku_asst, vdsa.*
	-- , inv.*
	-- drop table #vf
	into #vf

from		tt_om_invoice				inv
-- left  join	tt_pmtremittance			pmtremit	on pmtremit.om_invoice_id		= inv.om_invoice_id
-- left  join	tt_pmtinfo					pmtinfo     on pmtinfo.pmtinfo_id			= pmtremit.pmtinfo_id
left  join  tt_om_org_invoicestatus		st			on st.om_org_invoicestatus_id	= inv.om_org_invoicestatus_id

inner join  tt_om_vendordoc				vd			on vd.om_vendordoc_id			= inv.om_vendordoc_id			and vd.isobsolete  = 0	and vd.isactive = 1 
inner join  tt_om_vendordoc_lineitem	vdl			on vdl.om_vendordoc_id			= vd.om_vendordoc_id			and vdl.isobsolete = 0
-- inner join  tt_om_poline				pol			on pol.om_poline_id				= vdl.om_poline_id				and pol.isactive    = 1

inner join  tt_om_vendordoc_sku			vds			on vds.om_vendordoc_lineitem_id = vdl.om_vendordoc_lineitem_id	and vds.isobsolete = 0
inner join  tt_om_assortment			vdsa		on vdsa.om_assortment_id		= vds.om_assortment_id

-- Now find matches from XML

left join  #tmp						t
	-- SO / CI / PO
	on  t.ShippingOrderNumber		= vd.shippingordernum
	and t.CommercialInvoiceNumber	= vd.invoicenum
	and t.PurchaseOrderNumber		= vdl.ponum

	-- Assortment: Color + Size + Dimension
	and t.Color						= vdsa.color
	and t.Size						= vdsa.size
	and (t.Dimension = vdsa.dimension or len(vdsa.dimension) < 1 or vdsa.dimension is null )
	and t.POLineNumber				= vdl.om_poline_num		-- same in VDL and POL
	-- and t.upc						= vdsa.upc

	-- PO-line / VD-line
	left join tt_om_prod	px 
		on px.code = t.ItemNumber  and px.org_id = 12408
		---->> Note om_prod_id check below

where 1=1
	-- and inv.invoicenum in ('122866')
	and inv.isactive = 1
    and inv.customer_org_id=12408 --VF
	and inv.isactive					= 1

	-- Must ensure the SO-line matches!  but do not remove DB Assortment from query if no match.  This prevents duplicates.
	and vdl.om_prod_id			= isnull(px.om_prod_id, vdl.om_prod_id)

    and inv.om_org_invoicestatus_id	in (2,3)
    and inv.ispaymentprocessed		= 0

	-- Filter down to SO.xml that we are analyzing now ...
	and vd.shippingordernum in (select distinct ShippingOrderNumber from #tmp)

-- Exclude Invoices linked to Memos: Debits or Credits
	and not exists 
	(select 1
		from tt_om_invoicememo			invm		
		where	invm.invoicenum				= inv.invoicenum
		and		invm.customerorg_id			= inv.customer_org_id
		and		invm.isactive				= 1
	)
order by 
	  inv.om_invoice_id
	, inv.invoicenum
	, vd.shippingordernum
	, vdl.vdocline_objidkey
	, vdsa.color
	, vdsa.size
	, vdsa.dimension

end

select top 1 * from #vf
select top 1 * from #tmp

if 'counts' = 'counts' begin
	select 'Analyzing Counts'
	select count(*) db2xml_count	from #vf										-- 87699 in VF table
	select count(*) xml_asst_count	from #tmp										-- 62638
	select count(*) from #vf	where quantity_so_xml is null						-- 1788	-- rows to be fixed
	select count(distinct om_vendordoc_sku_id) from #vf -- 63450 unique sku_ids

	select CommercialInvoiceNumber, ShippingOrderNumber, PurchaseOrderNumber, ItemNumber, Color, Size, Dimension
		, count(*)
		from #tmp
		group by CommercialInvoiceNumber, ShippingOrderNumber, PurchaseOrderNumber, ItemNumber, Color, Size, Dimension
		having count(*) > 1

end

if 'check duplicates in #vf' = 'check duplicates in #vf' begin
	select om_invoice_id, invoicenum, shippingordernum, vdocline_objidkey, color, size, dimension
		, count(*) rows
		, max(upc_so_xml) upc_max
		, min(upc_so_xml) upc_min
		
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

end

if 'clean #tmp' = 'clean #tmp done' begin
	-- drop table #so
	-- Make sure ONLY data for needed SO #s are in #tmp
	select distinct shippingordernum into #so from #vf

	-- 986 should not be there in #tmp
	delete
	-- select shippingordernumber 
		from #tmp
		where shippingordernumber not in (select distinct shippingordernum from #so)

select top 50 *
	from		tt_om_po		po
	inner join	tt_om_poline	pol on pol.om_po_id = po.om_po_id
	where po.ponum in ('4500909708')



end

select top 3 * from #vf
select top 3 * from #tmp


if 'no check SO 5010165626' = 'check SO 5010165626' begin

select * from #tmp t
	where t.shippingordernumber in ('5010165626')

select vdl.om_poline_id, vdl.om_poline_num, pol.om_poline_num, *
	from		tt_om_vendordoc_lineitem	vdl
	inner join	tt_om_poline				pol on pol.om_poline_id = vdl.om_poline_id
	where vdl.vdocline_objidkey in ('{5010166782}{4500935992}{450093599200020}{3849276}')


	
end