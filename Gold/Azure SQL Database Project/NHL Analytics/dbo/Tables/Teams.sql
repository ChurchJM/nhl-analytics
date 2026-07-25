CREATE TABLE [dbo].[Teams]
(
  [Id] INT NOT NULL IDENTITY(1,1),
  [FullName] VARCHAR(50) NOT NULL,
  [Abbreviation] VARCHAR(3) NOT NULL,
  CONSTRAINT PK_Teams PRIMARY KEY ([Id])
)
