using System.ComponentModel.DataAnnotations.Schema;
using Microsoft.EntityFrameworkCore;
using Microsoft.Net.Http.Headers;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Game> Games => Set<Game>();
    public DbSet<Goal> Goals => Set<Goal>();
    public DbSet<Assist> Assists => Set<Assist>();
    public DbSet<Penalty> Penalties => Set<Penalty>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Goal>()
            .Navigation(g => g.Assists)
            .AutoInclude();
        
        modelBuilder.Entity<Goal>()
            .Navigation(g => g.Sweater)
            .AutoInclude();
        
        modelBuilder.Entity<Assist>()
            .Navigation(a => a.Sweater)
            .AutoInclude();
        
        modelBuilder.Entity<Sweater>()
            .Navigation(s => s.Player)
            .AutoInclude();
        
        modelBuilder.Entity<Sweater>()
            .Navigation(s => s.Team)
            .AutoInclude();
        
        modelBuilder.Entity<Game>()
            .Navigation(g => g.HomeTeam)
            .AutoInclude();
        
        modelBuilder.Entity<Game>()
            .Navigation(g => g.AwayTeam)
            .AutoInclude();
        
        modelBuilder.Entity<Penalty>()
            .Navigation(p => p.Sweater)
            .AutoInclude();

        modelBuilder.Entity<Penalty>()
            .Navigation(p => p.PenaltyType)
            .AutoInclude();
        
        modelBuilder.Entity<PenaltyType>()
            .Navigation(p => p.PenaltySeverity)
            .AutoInclude();
    }
}