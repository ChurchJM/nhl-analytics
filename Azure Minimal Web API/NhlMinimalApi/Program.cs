using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

app.MapGet("/", () => "I'm alive!");

// app.MapGet("/api/goals/{id:int}", async (int id, AppDbContext db) =>
// {
//     var goal = await db.Goals.FirstOrDefaultAsync(g => g.Id == id);

//     return goal is not null
//         ? Results.Ok(goal) 
//         : Results.NotFound(new { message = $"Goal with ID {id} was not found." });
// });

app.MapGet("/api/boxscores/{gameId:int}", async (int gameId, AppDbContext db) =>
{
    var game = await db.Games.Where(g => g.Id == gameId).FirstOrDefaultAsync();
    if(game is null)
        return Results.NotFound(new { message = $"Game with ID {gameId} was not found." });
    
    var goals = await db.Goals.Where(g => g.GameId == gameId).ToListAsync();    
    var penalties = await db.Penalties.Where(p => p.GameId == gameId).ToListAsync();

    DateOnly gameDate = game.GameDate;
    string homeTeam = game.HomeTeam.Abbreviation;
    string awayTeam = game.AwayTeam.Abbreviation;

    List<GoalDTO> homeGoals = new List<GoalDTO>();
    List<GoalDTO> awayGoals = new List<GoalDTO>();
    foreach(Goal goal in goals)
    {
        int _gameId = goal.GameId;
        string team = goal.Sweater.Team.Abbreviation;
        int _period = Convert.ToInt32(goal.SecondsIn/1200)+1;
        string _timeInPeriod = TimeSpan.FromSeconds(goal.SecondsIn%1200).ToString(@"mm\:ss");
        string _scorer = goal.Sweater.Player.First + " " + goal.Sweater.Player.Last;

        List<AssistDTO> _assists = new List<AssistDTO>();
        if(goal.Assists is not null)
        {
            foreach(Assist assist in goal.Assists)
            {
                string _assister = assist.Sweater.Player.First + " " + assist.Sweater.Player.Last; 
                AssistDTO _assist = new(_assister, assist.Sweater.Number);
                _assists.Add(_assist);
            }
        }
        GoalDTO _goal = new(_scorer, goal.Sweater.Number, _period, _timeInPeriod, _assists);
        if(team == homeTeam)
            homeGoals.Add(_goal);
        else
            awayGoals.Add(_goal);
    }

    List<PenaltyDTO> homePenalties = new List<PenaltyDTO>();
    List<PenaltyDTO> awayPenalties = new List<PenaltyDTO>();
    foreach(Penalty penalty in penalties)
    {
        string team = penalty.Sweater.Team.Abbreviation;
        string offender = penalty.Sweater.Player.First + " " + penalty.Sweater.Player.Last;
        int _period = Convert.ToInt32(penalty.SecondsIn/1200)+1;
        string _timeInPeriod = TimeSpan.FromSeconds(penalty.SecondsIn%1200).ToString(@"mm\:ss");

        PenaltyDTO _penalty = new PenaltyDTO(penalty.PenaltyType.Name, penalty.PenaltyType.PenaltySeverity.Name, 
                                             penalty.PenaltyType.PenaltySeverity.StatisticalMinutes, offender, penalty.Sweater.Number, 
                                             _period, _timeInPeriod);
        if(team == homeTeam)
        {
            homePenalties.Add(_penalty);
        }
        else
        {
            awayPenalties.Add(_penalty);
        }
    }

    BoxScoreDTO boxScore = new BoxScoreDTO(gameDate, homeTeam, awayTeam, homeGoals, awayGoals, homePenalties, awayPenalties);

    return Results.Ok(boxScore);
});

app.Run();
