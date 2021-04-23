select
  concat('Workbook', '', workbooks.id) as parentID,
  concat('View', '', views.id) as childID,
  views.index as viewsIndex
from
  workbooks
  left outer join views on views.workbook_id = workbooks.id
where
  sheettype = 'dashboard'
