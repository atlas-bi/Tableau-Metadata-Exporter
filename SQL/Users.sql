select
  _users.id,
  _users.domain_short_name || '\' || _users.name
from
    _users
order by
    _users.id
