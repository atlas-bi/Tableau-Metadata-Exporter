select
	workbooks.id,
	workbooks.name,
	workbooks.description,
	workbooks.created_at,
	workbooks.updated_at,
	'https://tableau_server/#/workbooks/' || workbooks.id || '/views',
	workbooks.repository_url,
	workbooks.owner_id
from
	workbooks
