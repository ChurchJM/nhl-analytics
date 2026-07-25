CREATE TABLE [dbo].[Assists]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [GoalId] INT NOT NULL,
  [SweaterId] INT NOT NULL,
  CONSTRAINT PK_Assists PRIMARY KEY ([Id]),
  CONSTRAINT FK_AssistsGoals FOREIGN KEY ([GoalId]) REFERENCES [Goals]([Id]),
  CONSTRAINT FK_AssistsSweaters FOREIGN KEY ([SweaterId]) REFERENCES [Sweaters]([Id])
)
