CREATE TABLE [dbo].[Games]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [HomeTeamId] INT NOT NULL,
  [AwayTeamId] INT NOT NULL,
  [Season] INT NOT NULL,
  [GameType] INT NOT NULL,
  [GameNumber] INT NOT NULL,
  [GameDate] DATE NOT NULL,
  CONSTRAINT PK_Games PRIMARY KEY ([Id]),
  CONSTRAINT FK_Games_HomeTeam FOREIGN KEY ([HomeTeamId]) REFERENCES [Teams]([Id]),
  CONSTRAINT FK_Games_AwayTeam FOREIGN KEY ([AwayTeamId]) REFERENCES [Teams]([Id])
)
