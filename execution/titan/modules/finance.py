"""
TITAN Finance Module
Crypto prices, stock market, financial intelligence.
"""

import json
from datetime import datetime
from typing import Optional

import requests

try:
    from ..config import CRYPTO_WATCHLIST, STOCK_WATCHLIST
except ImportError:
    CRYPTO_WATCHLIST = []
    STOCK_WATCHLIST = []
from ..ai_client import chat as ai_chat


class TitanFinance:
    """Titan's financial intelligence."""

    def __init__(self):
        pass

    # === CRYPTO ===

    def get_crypto_prices(self) -> dict:
        """Get current crypto prices from CoinGecko (free, no API key)."""
        try:
            ids = {
                "BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana",
                "AVAX": "avalanche-2", "LINK": "chainlink", "MATIC": "matic-network",
                "DOT": "polkadot", "ADA": "cardano", "XRP": "ripple",
                "DOGE": "dogecoin", "BNB": "binancecoin",
            }

            # Filter to watchlist
            coin_ids = [ids[s] for s in CRYPTO_WATCHLIST if s in ids]
            ids_str = ",".join(coin_ids)

            url = f"https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": ids_str,
                "vs_currencies": "usd,eur",
                "include_24hr_change": "true",
                "include_market_cap": "true",
            }

            resp = requests.get(url, params=params, timeout=10)
            data = resp.json()

            # Reverse map
            id_to_symbol = {v: k for k, v in ids.items()}

            prices = {}
            for coin_id, info in data.items():
                symbol = id_to_symbol.get(coin_id, coin_id.upper())
                prices[symbol] = {
                    "usd": info.get("usd", 0),
                    "eur": info.get("eur", 0),
                    "change_24h": info.get("usd_24h_change", 0),
                    "market_cap": info.get("usd_market_cap", 0),
                }

            return prices

        except Exception as e:
            return {"error": str(e)}

    async def get_crypto_brief(self) -> str:
        """Get a formatted crypto brief."""
        prices = self.get_crypto_prices()

        if "error" in prices:
            return f"Erreur prix crypto: {prices['error']}"

        lines = [f"🪙 CRYPTO — {datetime.now().strftime('%d/%m %H:%M')}\n"]

        for symbol in CRYPTO_WATCHLIST:
            if symbol not in prices:
                continue
            p = prices[symbol]
            change = p["change_24h"]
            emoji = "🟢" if change >= 0 else "🔴"
            change_str = f"+{change:.1f}%" if change >= 0 else f"{change:.1f}%"

            if p["usd"] >= 1000:
                price_str = f"${p['usd']:,.0f}"
            elif p["usd"] >= 1:
                price_str = f"${p['usd']:.2f}"
            else:
                price_str = f"${p['usd']:.4f}"

            lines.append(f"{emoji} {symbol}: {price_str} ({change_str})")

        return "\n".join(lines)

    # === STOCKS ===

    def get_stock_prices(self) -> dict:
        """Get stock prices from Yahoo Finance (free endpoint)."""
        try:
            prices = {}
            for symbol in STOCK_WATCHLIST:
                url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                params = {"interval": "1d", "range": "2d"}
                headers = {"User-Agent": "Mozilla/5.0"}

                resp = requests.get(url, params=params, headers=headers, timeout=10)
                data = resp.json()

                result = data.get("chart", {}).get("result", [])
                if result:
                    meta = result[0].get("meta", {})
                    price = meta.get("regularMarketPrice", 0)
                    prev_close = meta.get("previousClose", 0)

                    change = 0
                    if prev_close > 0:
                        change = ((price - prev_close) / prev_close) * 100

                    prices[symbol] = {
                        "price": price,
                        "change": change,
                        "currency": meta.get("currency", "USD"),
                    }

            return prices

        except Exception as e:
            return {"error": str(e)}

    async def get_stocks_brief(self) -> str:
        """Get a formatted stocks brief."""
        prices = self.get_stock_prices()

        if "error" in prices:
            return f"Erreur bourse: {prices['error']}"

        if not prices:
            return "Pas de données boursières disponibles."

        lines = [f"📈 BOURSE — {datetime.now().strftime('%d/%m %H:%M')}\n"]

        for symbol in STOCK_WATCHLIST:
            if symbol not in prices:
                continue
            p = prices[symbol]
            change = p["change"]
            emoji = "🟢" if change >= 0 else "🔴"
            change_str = f"+{change:.1f}%" if change >= 0 else f"{change:.1f}%"
            lines.append(f"{emoji} {symbol}: ${p['price']:.2f} ({change_str})")

        return "\n".join(lines)

    # === ANALYSIS ===

    async def get_quick_data(self, query: str) -> str:
        """Quick finance data based on query."""
        query_lower = query.lower()

        if any(w in query_lower for w in ["btc", "bitcoin", "eth", "crypto", "sol"]):
            return await self.get_crypto_brief()

        if any(w in query_lower for w in ["bourse", "stock", "action", "aapl", "nvda", "msft"]):
            return await self.get_stocks_brief()

        # Both
        crypto = await self.get_crypto_brief()
        stocks = await self.get_stocks_brief()
        return f"{crypto}\n\n{stocks}"

    async def analyze_market(self) -> str:
        """AI-powered market analysis."""
        crypto = self.get_crypto_prices()
        stocks = self.get_stock_prices()

        data_text = f"Crypto: {json.dumps(crypto, indent=2)}\nStocks: {json.dumps(stocks, indent=2)}"

        return ai_chat("Expert assistant.", f"""Analyse rapide du marche basee sur ces donnees:\n\n{data_text}""", 512)
