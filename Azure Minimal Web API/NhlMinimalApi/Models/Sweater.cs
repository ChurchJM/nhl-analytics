using System.ComponentModel.DataAnnotations.Schema;

[Table("Sweaters")]
public class Sweater
{
    public int Id {get; set;}
    public int PlayerId {get; set;}

    [ForeignKey(nameof(PlayerId))]
    public required Player Player {get; set;}
    public int TeamId {get; set;}

    [ForeignKey(nameof(TeamId))]
    public required Team Team {get; set;}
    public int Number {get; set;}
    public required string Position {get; set;}
    public DateOnly EffectiveDate {get; set;}
}