select 
sub.Id as Id
, sub.target_type as TargetType
, sub.target_id as TargetId
, sub.created_at AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific' as Created
, sub.last_sent AT TIME ZONE 'UTC' AT TIME ZONE 'US/Pacific' as LastRun
, usr.id as UserId
, usr.domain_short_name || '\' || usr.name as UserName
, sub.subject as Description
, runs.details as Details

 FROM subscriptions sub
left JOIN public.most_recent_subscription_runs runs
on runs.subscription_id = sub.id
LEFT JOIN public._users usr on usr.Id = sub.user_id

