select
  views.id,
  views.name,
  'TABLEAUURL/#/views/' || workbooks.repository_url || '/' || views.sheet_id as URL,
  views.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific',
  views.updated_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific',
  views.index,
  views.owner_id
from
  views
  left outer join workbooks on workbooks.id = views.workbook_id

  --leave out custom views for now.
/*
UNION ALL

  select 
   cust.id,
   cust.name,
  'TABLEAUURL/#/views/' || workbooks.repository_url || '/' || views.sheet_id
  || '/' || cust.luid || '/' ||  cust.url_id as URL,
  views.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific',
  views.updated_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific',
  999 as index,
  cust.creator_id,
   CASE WHEN cust.public = FALSE THEN 'N' ELSE 'Y' End as DefaultVisibility
   FROM customized_views cust
   JOIN views views
   on views.id = cust.view_id 
 join workbooks workbooks on workbooks.id = views.workbook_id
where
  views.sheettype = 'dashboard' and cust.Hidden = FALSE*/