CREATE TABLE [dbo].[PenaltyTypes]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [PenaltySeverityId] INT NOT NULL,
  [Name] VARCHAR(100) NOT NULL,
  CONSTRAINT PK_PenaltyTypes PRIMARY KEY ([Id]),
  CONSTRAINT FK_PenaltyTypesPenaltySeverities FOREIGN KEY ([PenaltySeverityId]) REFERENCES [PenaltySeverities]([Id])
)
