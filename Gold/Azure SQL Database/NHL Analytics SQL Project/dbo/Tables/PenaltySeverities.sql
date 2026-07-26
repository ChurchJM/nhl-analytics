CREATE TABLE [dbo].[PenaltySeverities]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [Name] VARCHAR(50) NOT NULL,
  [Abbreviation] VARCHAR(10) NOT NULL,
  [PowerPlayMinutes] INT NOT NULL,
  [StatisticalMinutes] INT NOT NULL,
  CONSTRAINT PK_PenaltySeverities PRIMARY KEY ([Id])
)
