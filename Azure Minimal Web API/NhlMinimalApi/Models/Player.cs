using System.ComponentModel.DataAnnotations.Schema;

[Table("Players")]
public class Player
{
    public int Id {get; set;}
    public required string First {get; set;}
    public required string Last {get; set;}
    public required string Nationality {get; set;}
    public DateOnly BirthDate {get; set;}
}