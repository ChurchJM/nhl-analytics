using System.ComponentModel.DataAnnotations.Schema;

[Table("Games")]
public class Game
{
    public int Id {get; set;}
    public int HomeTeamId {get; set;}

    [ForeignKey(nameof(HomeTeamId))]
    public required Team HomeTeam {get; set;}
    public int AwayTeamId {get; set;}

    [ForeignKey(nameof(AwayTeamId))]
    public required Team AwayTeam {get; set;}
    public int Season {get; set;}
    public int GameType {get; set;}
    public int GameNumber {get; set;}
    public DateOnly GameDate {get; set;}
}