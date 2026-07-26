use [NhlAnalytics];
go

select 
    min([g].[Id]) as GoalId,
    [ga].[Season],
    [ga].[GameNumber],
    min(floor([g].[SecondsIn]/1200)+1) as [Period],
    min(right(convert(varchar(8), dateadd(second, [g].[SecondsIn]%1200, 0), 108), 5)) AS [TimeInPeriod],
    min(concat([gp].[First], ' ', [gp].[Last])) as Scorer, 
    string_agg(concat([ap].[First], ' ', [ap].[Last]), ', ') within group (order by [ap].[Last])as Assists
from Assists a
    left join Sweaters [as] on [as].Id = a.SweaterId
    left join Players [ap] on [ap].Id = [as].PlayerId
    left join Goals g on g.Id = a.GoalId
    left join Sweaters [gs] on [gs].Id = g.SweaterId
    left join Players [gp] on [gp].Id = [gs].PlayerId
    left join Games [ga] on [ga].Id = g.GameId
where [ga].[Season] = 20212022 and [ga].[GameNumber] <= 10
group by [ga].[Season], [ga].[GameNumber], g.Id
order by [ga].[GameNumber]