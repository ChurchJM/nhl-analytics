# NHL Analytics Project
This project prepares National Hockey League (NHL) data for analytics. There are three main components:
1. A Python data pipeline which consumes and processes data from three NHL APIs and from post-game HTML summaries.
2. A C# Entity Framework minimal web API that exposes the processed data.
3. A simple front-end React app for viewing and validating the final data products.

## Data Pipeline
A number of NHL APIs are (unofficially) available to the public and documented at https://github.com/Zmalski/NHL-API-Reference. The three endpoints consumed by the data pipeline are as follows:
1. [Get Landing](https://github.com/Zmalski/NHL-API-Reference#get-landing). Contains "game-level" events, including goals, assists, and penalties.
2. [Get Boxscore](https://github.com/Zmalski/NHL-API-Reference#get-boxscore). Contains "player-level" statistics, including scoring, hits, time-on-ice, etc. for each player in the game.
3. [Get Player Information](https://github.com/Zmalski/NHL-API-Reference#get-player-information). Contains historical information about NHL players (birth date, nationality, previous season statistics, etc.).
* NHL post-game HTML summaries (i.e., https://www.nhl.com/scores/htmlreports/20222023/GS020688.HTM) are also processed via web scraping to get the referees and linesmen who officiated each game.

The pipeline is organized according the Medallion design pattern (bronze, silver, and gold layers). In the bronze layer, raw data from the 21/22-25/26 NHL seasons is retrieved from the sources above. In the silver layer, relevant data is cleaned and irrelevant data is discarded. Tables are also built and related in the silver layer (although this should probably be moved to the gold layer). In the gold layer, the data is deployed to a fully normalized Azure SQL Database, one of the final data products. The other (planned) data product is a star schema data warehouse for analytics.

Dependencies in the data pipeline are complex (see diagram below) and would greatly benefit from orchestration. I plan to move the pipeline to an [Apache Airflow](https://airflow.apache.org/) DAG when time permits.

<img width="1022" height="400" alt="pipeline_dependencies" src="https://github.com/user-attachments/assets/5073ab9b-b1b2-46c8-ae9d-ca4fe3133ed4">

*Dependencies (e.g., execution order) for Python scripts in the data pipeline.* 

The SQL schema is shown in the next figure. Some tables are basically just the result of parsing .json from the NHL APIs (i.e., Players) while others contain "new" information derived from the raw data (i.e., Sweaters). The schema is completely normalized, with one exception; three columns in the Games table (Season, GameType, and GameNumber) can be extracted from the Id. For example, from the Id 2022020345, Season (20222023; the first four digits + the next year), GameType (02; regular season game; the middle two digits), and GameNumber (345; the last four digits) can all be derived.

<img width="1470" height="826" alt="schema" src="https://github.com/user-attachments/assets/e5f99fb4-dc1a-4a51-8bbf-92ef594e53c1">

*Schema of the Azure SQL database deployed by the data pipeline.*

## C# Entity Framework Minimal Web API
A lightweight web API sits in front of the database, publicly exposing the data without authentication. Currently there is only one endpoint (more are coming) which returns reconstituted box scores/game summaries.
* https://nhl-analytics-api-hbbxg6adcshgbgcs.westus3-01.azurewebsites.net/api/boxscores/{GameId}. GameId (i.e., 2022020345) is formatted as discussed above: SSSSTTNNNN, where SSSS = Season, TT = GameType, and NNNN = GameNumber.

The API project includes model classes for every table in the database, as well as a few data transfer object (DTO) classes. The DTO classes serve to flatten the game summary data and serve it as a single .json payload.

## Simple Front-End React Application

## Future Work
* Implement data pipeline in Airflow.
* Expand API/React app into a full react + d3.js dashboard for visual data validation.
