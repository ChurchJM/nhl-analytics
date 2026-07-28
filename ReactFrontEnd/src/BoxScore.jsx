import { useState, useEffect } from 'react';
import './BoxScore.css'

function BoxScore(){
    const [gameId, setGameId] = useState('')
    const [debouncedGameId, setDebouncedGameId] = useState('')
    const [boxScore, setBoxScore] = useState(null)
    const [loading, setLoading] = useState(false);

    // Prevent fetch until 1s has elapsed without user typing.
    useEffect(() => {   
        const timer = setTimeout(() => {
        setDebouncedGameId(gameId); // Update the actual (debounced) query value if Timeout finishes.
        }, 1000);
        
        // Cleanup function run prior to next useEffect call triggered by gameId update.
        // (every character entered by user resets the delay to 1s)
        return () => clearTimeout(timer);
    }, [gameId]);

    // Actual data retrieval happens when debouncedGameId is updated by the above timer.
    useEffect(() => {
        // Game id format is [SSSS][GG][NNNN] where S = season, G = game type, N = game number (i.e., 2021020450)
        if (debouncedGameId.trim().length != 10) {
            // ToDo: Show error message informing user of game id format?
            return;
        }

        let isCurrent = true;
        setLoading(true);

        async function fetchData() {
            try {
                const response = await fetch(`https://nhl-analytics-api-hbbxg6adcshgbgcs.westus3-01.azurewebsites.net/api/boxscores/${debouncedGameId}`);
                const result = await response.json();
                // Only update boxScore state if this is the most recent (e.g., current) query.
                if (isCurrent) setBoxScore(result); 
            } finally {
                if (isCurrent) setLoading(false);
            }
        }

        fetchData();

        // Cleanup function runs prior to next query, ensuring only latest query isCurrent.
        return () => {
            isCurrent = false;
        };
    }, [debouncedGameId]);

    return (
        <>
        <div>
            <label htmlFor="gamdIdInput">Game ID: </label>
            <input
                style={{marginTop: 10}}
                id="gameIdInput"
                type="text"
                placeholder="Example: 2021020567"
                value={gameId}
                onChange={(e) => setGameId(e.target.value)}
            />     
            {boxScore !== null ? (
                <>
                <p>{boxScore['gameDate']}</p>
                <table>
                    <tbody>
                        <tr>
                            <td className="home">HOME: {boxScore["homeTeam"]}</td>
                            <td className="away">AWAY: {boxScore["awayTeam"]}</td>
                        </tr>
                        <tr>
                            <td className="home"><b>{boxScore["homeScore"]}</b></td>
                            <td className="away"><b>{boxScore["awayScore"]}</b></td>
                        </tr>
                    </tbody>
                </table>

                <p>HOME GOALS</p>
                <table className="home">
                    <tbody>
                        <tr className="home" style={{borderBottom: "1px solid black"}}>
                            <td>Player</td>
                            <td>Period</td>
                            <td>Time</td>
                        </tr>
                        {boxScore.homeGoals.map((g) => (
                            <>
                            <tr className="home">
                                <td>#{g.playerNumber} {g.player}</td>
                                <td>{g.period}</td>
                                <td>{g.timeInPeriod}</td>
                            </tr>
                            <tr style={{borderBottom: "1px solid black"}}>
                                <td colSpan={3} style={{textAlign: "right", fontSize:16, fontStyle: 'italic'}}>
                                    {g.assists.map((a, index)=> 
                                        <span>
                                            {index == 0 && 'Assisted By: '}
                                             #{a.playerNumber} {a.player}
                                            {index < g.assists.length - 1 && ', '}
                                        </span>
                                    )}
                                </td>
                            </tr>
                            </>
                        ))}
                    </tbody>
                </table>

                <p>AWAY GOALS</p>
                <table className="away">
                    <tbody>
                        <tr style={{borderBottom: '1px solid black'}}>
                            <td>Player</td>
                            <td>Period</td>
                            <td>Time</td>
                        </tr>
                        {boxScore.awayGoals.map((g) => (
                            <>
                            <tr>
                                <td>#{g.playerNumber} {g.player}</td>
                                <td>{g.period}</td>
                                <td>{g.timeInPeriod}</td>
                            </tr>
                            <tr style={{borderBottom: '1px solid black'}}>
                                <td colSpan={3} style={{textAlign: "right", fontSize:16, fontStyle: 'italic'}}>
                                    {g.assists.map((a, index)=> 
                                        <span>
                                            {index == 0 && 'Assisted By: '}
                                             #{a.playerNumber} {a.player}
                                            {index < g.assists.length - 1 && ', '}
                                        </span>
                                    )}
                                </td>
                            </tr>
                            </>
                        ))}
                    </tbody>
                </table>

                <p>HOME PENALTIES</p>
                <table className="home" style={{tableLayout:'auto'}}>
                    <tbody>
                        <tr style={{borderBottom: '1px solid black'}}>
                            <td>Player</td>
                            <td>Penalty</td>
                            <td>Duration</td>
                            <td>Period</td>
                            <td>Time</td>
                        </tr>
                        {boxScore.homePenalties.toSorted((a,b) => a.period - b.period).map((p) => (
                            <>
                            <tr style={{borderBottom: '1px solid black'}}>
                                <td>#{p.playerNumber} {p.player}</td>
                                <td>{p.penaltyType}</td>
                                <td>{p.penaltyMinutes}</td>
                                <td>{p.period}</td>
                                <td>{p.timeInPeriod}</td>
                            </tr>
                            </>
                        ))}
                    </tbody>
                </table>

                <p>AWAY PENALTIES</p>
                <table className="away" style={{tableLayout: 'auto'}}>
                    <tbody>
                        <tr style={{borderBottom: '1px solid black'}}>
                            <td>Player</td>
                            <td>Penalty</td>
                            <td>Duration</td>
                            <td>Period</td>
                            <td>Time</td>
                        </tr>
                        {boxScore.awayPenalties.toSorted((a,b) => a.period - b.period).map((p) => (
                            <>
                            <tr style={{borderBottom: '1px solid black'}}>
                                <td>#{p.playerNumber} {p.player}</td>
                                <td>{p.penaltyType}</td>
                                <td>{p.penaltyMinutes}</td>
                                <td>{p.period}</td>
                                <td>{p.timeInPeriod}</td>
                            </tr>
                            </>
                        ))}
                    </tbody>
                </table>
                </> 
                ) : (
                <>
                <p>Please enter a game ID.</p>
                <p style={{fontSize:15}}>Format is SSSSTTNNNN, where SSSS = season (e.g., 2021 for 21-22 season), TT = game type (use 02), and NNNN = game number.</p>
                </>)}
        </div>
        </>
    );
}

export default BoxScore