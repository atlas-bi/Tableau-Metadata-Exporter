select
  concat('Workbook', '', workbooks.id) as parentID,
  concat('View', '', views.id) as childID,
  views.index as viewsIndex
from
  workbooks
  JOIN views on views.workbook_id = workbooks.id

--was looking at custom views.
/*
UNION ALL
select
  concat('Workbook', '', workbooks.id) as parentID,
  concat('View', '', cust.id) as childID,
  999 as viewsIndex
from
  workbooks
  join views on views.workbook_id = workbooks.id
  JOIN customized_views cust on cust.view_id = views.id
*/