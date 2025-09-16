import React from "react";

export default function CoinTable({ coins, onSelect, selected }) {

    
  return (
    <table className="coin-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Price (USD)</th>
          <th>24h %</th>
          <th>24h Volume</th>
        </tr>
      </thead>

      <tbody>
        {coins.map((coin, index) => {
          const isSelected = selected === coin.cg_id;
          const priceChange = coin.price_change_percentage_24h;

          return (
            <tr
              key={coin.cg_id}
              className={isSelected ? "selected" : ""}
              onClick={() => onSelect(coin.cg_id)}
            >
              <td>{index + 1}</td>
              <td>
                {coin.name}{" "}
                <span className="symbol">({coin.symbol?.toUpperCase()})</span>
              </td>
              <td>${Number(coin.current_price).toLocaleString()}</td>
              <td className={priceChange >= 0 ? "up" : "down"}>
                {priceChange?.toFixed(2)}%
              </td>
              <td>
                ${Number(coin.total_volume || coin.volume_24h || 0).toLocaleString()}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
