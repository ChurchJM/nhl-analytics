using System.ComponentModel.DataAnnotations.Schema;

[Table("PenaltySeverities")]
public class PenaltySeverity
{
    public int Id {get; set;}
    public required string Name {get; set;}
    public required string Abbreviation {get; set;}
    public int PowerPlayMinutes {get; set;}
    public int StatisticalMinutes {get; set;}
}