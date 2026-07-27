using System.ComponentModel.DataAnnotations.Schema;

[Table("Teams")]
public class Team
{
    public int Id {get; set;}
    public required string FullName {get; set;}
    public required string Abbreviation {get; set;}
}
