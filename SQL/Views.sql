select
  views.id,
  views.name,
  'TABLEAUURL/#/views/' || workbooks.repository_url || '/' || views.sheet_id as URL,
  views.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
  views.updated_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
  views.index,
  views.owner_id
from
  views
  left outer join workbooks on workbooks.id = views.workbook_id
