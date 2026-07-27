public class BoxScoreDTO(DateOnly gameDate, string homeTeam, string awayTeam, List<GoalDTO> homeGoals, List<GoalDTO> awayGoals,
                         List<PenaltyDTO> homePenalties, List<PenaltyDTO> awayPenalties)
{
    public DateOnly GameDate {get; set;} = gameDate;
    public string HomeTeam {get; set;} = homeTeam;
    public string AwayTeam {get; set;} = awayTeam;
    public int HomeScore{
        get { return this.HomeGoals.Count; }
    }
    public int AwayScore{
        get { return this.AwayGoals.Count; }
    }
    public List<GoalDTO> HomeGoals {get; set;} = homeGoals;
    public List<GoalDTO> AwayGoals {get; set;} = awayGoals;
    public List<PenaltyDTO> HomePenalties {get; set;} = homePenalties;
    public List<PenaltyDTO> AwayPenalties {get; set;} = awayPenalties;
}