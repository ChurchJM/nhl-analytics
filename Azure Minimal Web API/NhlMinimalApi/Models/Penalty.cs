using System.ComponentModel.DataAnnotations.Schema;

[Table("Penalties")]
public class Penalty
{
    public int Id {get; set;}
    public int GameId {get; set;}
    public int SweaterId {get; set;}
    
    [ForeignKey(nameof(SweaterId))]
    public required Sweater Sweater {get; set;}
    public int PenaltyTypeId {get; set;}

    [ForeignKey(nameof(PenaltyTypeId))]
    public required PenaltyType PenaltyType {get; set;}
    public int SecondsIn {get; set;}
}