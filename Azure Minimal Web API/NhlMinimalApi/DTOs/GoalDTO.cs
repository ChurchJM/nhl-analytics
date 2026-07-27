public class GoalDTO(string player, int playerNumber, int period, string timeInPeriod, List<AssistDTO> assists)
{
    public string Player { get; set; } = player;
    public int PlayerNumber { get; set; } = playerNumber;
    public int Period { get; set; } = period;
    public string timeInPeriod { get; set; } = timeInPeriod;
    public List<AssistDTO>? Assists { get; set; } = assists;
}