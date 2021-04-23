select
	workbooks.id,
	workbooks.name,
	workbooks.description,
	workbooks.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
	workbooks.updated_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Central',
	'https://eptblp01.riversidehealthcare.net/#/workbooks/' || workbooks.id || '/views',
	workbooks.repository_url,
	workbooks.owner_id
from
	workbooks
