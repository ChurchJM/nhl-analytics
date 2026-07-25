CREATE TABLE [dbo].[Penalties]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [GameId] INT NOT NULL,
  [SweaterId] INT NOT NULL,
  [PenaltyTypeId] INT NOT NULL,
  [SecondsIn] INT NOT NULL,
  CONSTRAINT PK_Penalties PRIMARY KEY ([Id]),
  CONSTRAINT FK_PenaltiesGames FOREIGN KEY ([GameId]) REFERENCES [Games]([Id]),
  CONSTRAINT FK_PenaltiesSweaters FOREIGN KEY ([SweaterId]) REFERENCES [Sweaters]([Id]),
  CONSTRAINT FK_PenaltiesPenaltyTypes FOREIGN KEY ([PenaltyTypeId]) REFERENCES [PenaltyTypes]([Id])
)
