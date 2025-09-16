import React, { useEffect, useState } from 'react';
import API from '../services/api';
import CoinTable from '../components/CoinTable';
import CoinChart from '../components/CoinChart';
import ChatAssistant from '../components/ChatAssistant';

export default function Dashboard() {
  const [coins, setCoins] = useState([]);
  const [selectedCoin, setSelectedCoin] = useState(null);
  const [prices, setPrices] = useState([]);
  const [sortBy, setSortBy] = useState('market_cap');

  useEffect(() => {
    fetchTopCoins();
  }, [sortBy]);

  useEffect(() => {
    if (selectedCoin) fetchHistory(selectedCoin);
  }, [selectedCoin]);

  async function fetchTopCoins() {
    try {
      const res = await API.get('/coins/', {
        params: { limit: 10, sort_by: sortBy },
      });
      console.log(res.data)
      setCoins(res.data);
      if (!selectedCoin && res.data.length) {
        setSelectedCoin(res.data[0].cg_id);
      }
    } catch (err) {
      console.error('Failed to fetch top coins', err);
    }
  }

  async function fetchHistory(cg_id) {
    try {
      const res = await API.get(`/coins/${cg_id}/history/`);
      setPrices(res.data.prices || []);
    } catch (err) {
      console.error('Failed to fetch history', err);
      setPrices([]);
    }
  }

  return (
    <div className="dashboard">
      {/* Left side: controls, table, chart */}
      <div className="dashboard-left">
        <div className="controls">
          <label>
            Sort by:{' '}
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="market_cap">Market Cap</option>
              <option value="total_volume">24h Volume</option>
              <option value="price_change_percentage_24h">
                24h % Change
              </option>
            </select>
          </label>
        </div>

        <CoinTable
          coins={coins}
          onSelect={setSelectedCoin}
          selected={selectedCoin}
        />

        {selectedCoin && (
          <>
            <h3>30-day trend: {selectedCoin}</h3>
            <CoinChart prices={prices} />
          </>
        )}
      </div>

      {/* Right side: chat assistant */}
      <div className="dashboard-right">
        <ChatAssistant />
      </div>
    </div>
  );
}
