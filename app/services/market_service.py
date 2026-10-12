from typing import Dict, Any, List
import yfinance as yf

class MarketDataService:
    @staticmethod
    def get_current_price(ticker: str) -> float:
        """Fetch the latest market price for a given ticker."""
        try:
            data = yf.Ticker(ticker)
            price = data.fast_info.get("lastPrice")
            if price is None:
                hist = data.history(period="1d")
                if not hist.empty:
                    price = hist["Close"].iloc[-1]
            return round(float(price), 2) if price else 0.0
        except Exception:
            return 0.0

    @staticmethod
    def get_benchmark_performance(symbol: str = "^GSPC", period: str = "1y") -> List[Dict[str, Any]]:
        """Fetch historical performance for S&P 500 (^GSPC) or other index benchmark."""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        performance = []
        for date, row in hist.iterrows():
            performance.append({
                "date": date.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2)
            })
        return performance
