using System.ComponentModel.DataAnnotations.Schema;

[Table("Assists")]
public class Assist
{
    public int Id {get; set;} 
    public int GoalId {get; set;}
    public int SweaterId {get; set;}

    [ForeignKey(nameof(SweaterId))]
    public required Sweater Sweater {get; set;}
}