import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [ticker, setTicker] = useState('');
  const [entryCondition, setEntryCondition] = useState('');
  const [exitCondition, setExitCondition] = useState('');
  const [results, setResults] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post('http://localhost:5000/backtest', {
      ticker,
      entryCondition,
      exitCondition
    });
    setResults(response.data);
  };

  return (
    <div className="App">
      <h1>Stock Backtesting Dashboard</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Stock Ticker:</label>
          <input type="text" value={ticker} onChange={(e) => setTicker(e.target.value)} />
        </div>
        <div>
          <label>Entry Condition:</label>
          <input type="text" value={entryCondition} onChange={(e) => setEntryCondition(e.target.value)} />
        </div>
        <div>
          <label>Exit Condition:</label>
          <input type="text" value={exitCondition} onChange={(e) => setExitCondition(e.target.value)} />
        </div>
        <button type="submit">Backtest</button>
      </form>
      {results && (
        <div>
          <h2>Results</h2>
          <p>Profit: {results.profit}</p>
          <p>Winning Trades: {results.winning_trades}</p>
          <p>Losing Trades: {results.losing_trades}</p>
          <h3>Trades</h3>
          <ul>
            {results.trades.map((trade, index) => (
              <li key={index}>{`${trade[0]} ${trade[2]} shares at ${trade[3]} on ${trade[1]}`}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
