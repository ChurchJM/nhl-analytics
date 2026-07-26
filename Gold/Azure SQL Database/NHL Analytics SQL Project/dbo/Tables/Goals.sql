CREATE TABLE [dbo].[Goals]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [GameId] INT NOT NULL,
  [SweaterId] INT NOT NULL,
  [GoalStrength] VARCHAR(10) NOT NULL,
  [SecondsIn] INT NOT NULL,
  CONSTRAINT PK_Goals PRIMARY KEY ([Id]),
  CONSTRAINT FK_GoalsGames FOREIGN KEY ([GameId]) REFERENCES [Games]([Id]),
  CONSTRAINT FK_GoalsSweaters FOREIGN KEY ([SweaterId]) REFERENCES [Sweaters]([Id])
)
