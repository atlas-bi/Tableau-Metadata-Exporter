select
  concat('Project', '', projects.id) as parentID,
  concat('Workbook', '', workbooks.id) as childID
from
  projects
  left outer join workbooks on workbooks.project_id = projects.id
