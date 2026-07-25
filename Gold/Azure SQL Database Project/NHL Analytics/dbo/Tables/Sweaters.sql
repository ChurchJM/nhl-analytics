CREATE TABLE [dbo].[Sweaters]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [PlayerId] INT NOT NULL,
  [TeamId] INT NOT NULL,
  [Number] INT NOT NULL,
  [Position] VARCHAR(1) NOT NULL,
  [EffectiveDate] DATE NOT NULL,
  CONSTRAINT PK_Sweaters PRIMARY KEY ([Id]),
  CONSTRAINT FK_SweatersPlayers FOREIGN KEY ([PlayerId]) REFERENCES [Players]([Id]),
  CONSTRAINT FK_SweatersTeams FOREIGN KEY ([TeamId]) REFERENCES [Teams]([Id])
)
