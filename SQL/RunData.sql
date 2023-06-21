select 
histEvents.created_at as EventDate
, histUsers.user_id as UserID
, histViews.view_id as DashboardID
, 1 as nviews
, GENERATE_SERIES(1,1)

 FROM public.historical_events as histEvents
JOIN public.hist_views as histViews on histViews.Id = histEvents.hist_view_id
join public.hist_users as histUsers on histUsers.id = histEvents.hist_actor_user_id
join public.historical_event_types typs on typs.type_id = histEvents.historical_event_type_id
where  typs.action_type = 'Access'