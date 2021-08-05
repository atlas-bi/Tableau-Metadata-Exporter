SELECT first_table."time" as EventDate, 
first_table.user_id as UserID, 
first_table.view_id as DashboardID,
first_table.nviews,
generate_series(1, first_table.nviews) 

FROM public.views_stats as first_table
