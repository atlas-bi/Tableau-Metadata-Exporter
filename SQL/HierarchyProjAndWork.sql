SELECT
  parentId,
  childID,
  ROW_NUMBER() OVER (
    partition by parentId
    order by
      childId
  ) as Index
FROM(
    select
      concat('Project', '', projects.id) as parentID,
      concat('Workbook', '', workbooks.id) as childID
    from
      projects
      join workbooks on workbooks.project_id = projects.id
    UNION
    SELECT
      concat('Project', '', parProj.id),
      concat('Project', '', proj.id)
    from
      projects proj
      JOIN projects parProj on proj.parent_project_id = parProj.id
  ) as main
order by
  parentId,
  Index