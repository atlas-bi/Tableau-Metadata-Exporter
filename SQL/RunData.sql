--Query to find run data
--to find other events go to: historical_event_types
SELECT
        he.created_at  AT TIME ZONE 'UTC-6'   AS last_event_date ,		
        hu.user_id ,
        --he.historical_event_type_id      AS event_type_id ,
		--historical_event_types.name as event_type_name,
        hist_views.view_id 
		--hist_views.name as view_name
        --he.hist_workbook_id ,		
		--hist_workbooks.name as workbook_name
    FROM historical_events he
        LEFT JOIN hist_users hu ON he.hist_actor_user_id = hu.id
		left join hist_views on hist_views.id=he.hist_view_id
		inner join views on views.id=hist_views.view_id
		left join hist_workbooks on hist_workbooks.id=he.hist_workbook_id
		left join historical_event_types on historical_event_types.type_id=he.historical_event_type_id
    WHERE 
        he.historical_event_type_id IN ( 
            84     --access view
            )
        AND age(he.created_at) <= INTERVAL '730 days'
		AND views.sheettype = 'dashboard'    
order by 1 desc
