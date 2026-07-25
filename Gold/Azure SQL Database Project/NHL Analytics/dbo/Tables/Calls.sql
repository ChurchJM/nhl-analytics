CREATE TABLE [dbo].[Calls]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [PenaltyId] INT NOT NULL,
  [RefereeId] INT NOT NULL,
  CONSTRAINT PK_Calls PRIMARY KEY ([Id]),
  CONSTRAINT FK_CallsPenalties FOREIGN KEY ([PenaltyId]) REFERENCES [Penalties]([Id]),
  CONSTRAINT FK_CallsReferees FOREIGN KEY ([RefereeId]) REFERENCES [Referees]([Id])
)
