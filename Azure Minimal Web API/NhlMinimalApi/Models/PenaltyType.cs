using System.ComponentModel.DataAnnotations.Schema;

[Table("PenaltyTypes")]
public class PenaltyType
{
    public int Id {get; set;}
    public int PenaltySeverityId {get; set;}

    [ForeignKey(nameof(PenaltySeverityId))]
    public required PenaltySeverity PenaltySeverity {get; set;}
    public required string Name {get; set;}
}