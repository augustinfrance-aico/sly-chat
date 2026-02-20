"""
TITAN Crypto DeFi Module
DeFi analytics, gas tracker, whale alerts, token info.
"""

import requests
from datetime import datetime


class TitanDeFi:
    """Deep crypto intelligence."""

    def gas_tracker(self) -> str:
        """Get Ethereum gas prices."""
        try:
            resp = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle", timeout=10)
            data = resp.json().get("result", {})
            if isinstance(data, dict):
                return (
                    f"⛽ ETH GAS TRACKER\n\n"
                    f"🟢 Low: {data.get('SafeGasPrice', '?')} Gwei\n"
                    f"🟡 Average: {data.get('ProposeGasPrice', '?')} Gwei\n"
                    f"🔴 High: {data.get('FastGasPrice', '?')} Gwei"
                )
        except Exception:
            pass
        return "Gas tracker indisponible (API key needed)."

    def token_info(self, token: str) -> str:
        """Get detailed token info from CoinGecko."""
        try:
            token_map = {
                "btc": "bitcoin", "eth": "ethereum", "sol": "solana",
                "avax": "avalanche-2", "link": "chainlink", "matic": "matic-network",
                "ada": "cardano", "dot": "polkadot", "xrp": "ripple",
                "doge": "dogecoin", "shib": "shiba-inu", "bnb": "binancecoin",
                "uni": "uniswap", "aave": "aave", "arb": "arbitrum",
            }
            coin_id = token_map.get(token.lower(), token.lower())
            resp = requests.get(
                f"https://api.coingecko.com/api/v3/coins/{coin_id}",
                params={"localization": "false", "tickers": "false", "community_data": "false", "developer_data": "false"},
                timeout=10,
            )
            data = resp.json()
            market = data.get("market_data", {})

            price = market.get("current_price", {}).get("usd", 0)
            change_24h = market.get("price_change_percentage_24h", 0)
            change_7d = market.get("price_change_percentage_7d", 0)
            change_30d = market.get("price_change_percentage_30d", 0)
            mcap = market.get("market_cap", {}).get("usd", 0)
            volume = market.get("total_volume", {}).get("usd", 0)
            ath = market.get("ath", {}).get("usd", 0)
            ath_change = market.get("ath_change_percentage", {}).get("usd", 0)
            rank = data.get("market_cap_rank", "?")

            return (
                f"🪙 {data.get('name', token).upper()} ({data.get('symbol', '').upper()})\n"
                f"{'=' * 25}\n\n"
                f"💰 Prix: ${price:,.2f}\n"
                f"📊 24h: {change_24h:+.1f}%\n"
                f"📈 7j: {change_7d:+.1f}%\n"
                f"📉 30j: {change_30d:+.1f}%\n\n"
                f"🏆 Rang: #{rank}\n"
                f"💎 Market Cap: ${mcap:,.0f}\n"
                f"📊 Volume 24h: ${volume:,.0f}\n\n"
                f"🏔 ATH: ${ath:,.2f} ({ath_change:+.1f}%)"
            )
        except Exception as e:
            return f"Token '{token}' non trouve: {e}"

    def fear_greed(self) -> str:
        """Crypto Fear & Greed Index."""
        try:
            resp = requests.get("https://api.alternative.me/fng/", timeout=10)
            data = resp.json()["data"][0]
            value = int(data["value"])
            classification = data["value_classification"]

            bar = "█" * (value // 10) + "░" * (10 - value // 10)

            if value <= 25:
                emoji = "😱"
            elif value <= 45:
                emoji = "😰"
            elif value <= 55:
                emoji = "😐"
            elif value <= 75:
                emoji = "😊"
            else:
                emoji = "🤑"

            return (
                f"📊 FEAR & GREED INDEX\n\n"
                f"{emoji} {value}/100 — {classification}\n"
                f"[{bar}]\n\n"
                f"0 = Extreme Fear | 100 = Extreme Greed"
            )
        except Exception:
            return "Fear & Greed Index indisponible."

    def trending_coins(self) -> str:
        """Get trending coins on CoinGecko."""
        try:
            resp = requests.get("https://api.coingecko.com/api/v3/search/trending", timeout=10)
            coins = resp.json().get("coins", [])[:7]

            lines = ["🔥 TRENDING CRYPTO\n"]
            for c in coins:
                item = c.get("item", {})
                name = item.get("name", "?")
                symbol = item.get("symbol", "?")
                rank = item.get("market_cap_rank", "?")
                lines.append(f"  #{rank} {name} ({symbol})")

            return "\n".join(lines)
        except Exception:
            return "Trending indisponible."

    def compare(self, coin1: str, coin2: str) -> str:
        """Compare two cryptocurrencies."""
        info1 = self.token_info(coin1)
        info2 = self.token_info(coin2)
        return f"{info1}\n\n{'=' * 30}\n\n{info2}"
