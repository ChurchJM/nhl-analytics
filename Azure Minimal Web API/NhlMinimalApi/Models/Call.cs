using System.ComponentModel.DataAnnotations.Schema;

[Table("Calls")]
public class Call
{
    public int Id {get; set;}
    public int PenaltyId {get; set;}
    public int RefereeId {get; set;}
}