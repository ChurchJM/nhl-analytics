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

The pipeline is organized according the Medallion design pattern (bronze, silver, and gold layers). In the bronze layer, raw data is retrieved from the sources above. In the silver layer, relevant data is cleaned and irrelevant data is discarded. Tables are also built and related in the silver layer (although this should probably be moved to the gold layer). In the gold layer, the data is deployed to a fully normalized Azure SQL Database, one of the final data products. The other (planned) data product is a star schema data warehouse for analytics.

Dependencies in the data pipeline are complex (see diagram below) and would greatly benefit from orchestration. I plan to move the pipeline to an [Apache Airflow](https://airflow.apache.org/) DAG when time permits.

<img width="1022" height="400" alt="pipeline_dependencies" src="https://github.com/user-attachments/assets/5073ab9b-b1b2-46c8-ae9d-ca4fe3133ed4" />
_Dependencies (e.g., execution order) for Python scripts in the data pipeline._

<img width="1470" height="826" alt="schema" src="https://github.com/user-attachments/assets/e5f99fb4-dc1a-4a51-8bbf-92ef594e53c1" />
