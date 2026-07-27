using System.ComponentModel.DataAnnotations.Schema;

[Table("Goals")]
public class Goal{
    public int Id {get; set;}
    public int GameId {get; set;}
    public int SweaterId {get; set;}
    
    [ForeignKey(nameof(SweaterId))]
    public required Sweater Sweater {get; set;}
    public required string GoalStrength {get; set;}
    public int SecondsIn {get; set;}

    // Nullable because goals can be unassisted.
    public List<Assist>? Assists {get; set;}
}