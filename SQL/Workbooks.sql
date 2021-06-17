select distinct
  workbooks.id,
  workbooks.name,
  workbooks.description,
  workbooks.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
  workbooks.updated_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
  'https://tableau/#/views/' || workbooks.repository_url || '/' || views.sheet_id,
  workbooks.repository_url,
  workbooks.owner_id
from
  workbooks
  left outer join views on workbooks.id = views.workbook_id
where views.index=1
