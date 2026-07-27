using System.ComponentModel.DataAnnotations.Schema;

[Table("Referees")]
public class Referee
{
    public int Id {get; set;}
    public required string First {get; set;}
    public required string Last {get; set;}
}