select _users.id,
_users.licensing_role_name
from _users, _sites
WHERE _sites.Id = _users.Site_Id
and _sites.status = 'active'
order by _users.id
