public class PenaltyDTO(string penaltyType, string penaltySeverity, int penaltyMinutes, 
                        string player, int playerNumber, int period, string timeInPeriod)
{
    public string PenaltyType {get; set;} = penaltyType;
    public string PenaltySeverity {get; set;} = penaltySeverity;
    public int PenaltyMinutes {get; set;} = penaltyMinutes;
    public string Player {get; set;} = player;
    public int PlayerNumber {get; set;} = playerNumber;
    public int Period {get; set;} = period;
    public string TimeInPeriod {get; set;} = timeInPeriod;
}