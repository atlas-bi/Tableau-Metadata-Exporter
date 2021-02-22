select
	views.id,
	views.name,
	'https://tableau_server/#/views/' || workbooks.repository_url || '/' || views.sheet_id,
	views.created_at,
	views.updated_at,
	views.index,
	views.owner_id
from
	views
left outer join workbooks on workbooks.id=views.workbook_id
where sheettype='dashboard'
