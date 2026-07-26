CREATE TABLE [dbo].[Players]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [First] VARCHAR(50) NOT NULL,
  [Last] VARCHAR(50) NOT NULL,
  [Nationality] VARCHAR(50) NOT NULL,
  [BirthDate] DATE NOT NULL,
  CONSTRAINT PK_Players PRIMARY KEY ([Id])
)
