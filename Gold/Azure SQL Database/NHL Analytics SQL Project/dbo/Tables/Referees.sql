CREATE TABLE [dbo].[Referees]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [First] VARCHAR(50) NOT NULL,
  [Last] VARCHAR(50) NOT NULL,
  CONSTRAINT PK_Referees PRIMARY KEY ([Id])
)
