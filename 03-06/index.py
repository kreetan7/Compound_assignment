import requests
import statistics
import time

API_URL = "https://api.coingecko.com/api/v3/simple/price"

class CryptoAnalyzer:
    def __init__(self, coin="bitcoin", currency="usd"):
        self.coin = coin
        self.currency = currency
        self.price_history = []

    def fetch_price(self):
        params = {
            "ids": self.coin,
            "vs_currencies": self.currency
        }

        try:
            response = requests.get(API_URL, params=params, timeout=5)
            data = response.json()
            price = data[self.coin][self.currency]
            return price
        except Exception as e:
            print("Error fetching price:", e)
            return None

    def collect_prices(self, count=10, delay=2):
        print(f"\nCollecting {count} price samples...\n")

        for i in range(count):
            price = self.fetch_price()

            if price:
                self.price_history.append(price)
                print(f"Sample {i+1}: {price} {self.currency.upper()}")

            time.sleep(delay)

    def analyze(self):
        if not self.price_history:
            print("No data to analyze")
            return

        avg_price = statistics.mean(self.price_history)
        max_price = max(self.price_history)
        min_price = min(self.price_history)

        print("\n--- Analysis Result ---")
        print(f"Average Price: {avg_price:.2f}")
        print(f"Highest Price: {max_price:.2f}")
        print(f"Lowest Price : {min_price:.2f}")
        print("----------------------")

    def simple_prediction(self):
        if len(self.price_history) < 2:
            print("Not enough data for prediction")
            return

        trend = self.price_history[-1] - self.price_history[0]

        print("\n--- Trend Prediction ---")

        if trend > 0:
            print("Market trend: UP 📈")
        elif trend < 0:
            print("Market trend: DOWN 📉")
        else:
            print("Market trend: STABLE")

def main():
    print("\n=== Crypto Price Analyzer ===")

    coin = input("Enter cryptocurrency (bitcoin/ethereum/dogecoin): ").lower()
    samples = int(input("Number of samples to collect: "))

    analyzer = CryptoAnalyzer(coin)
    analyzer.collect_prices(samples)

    analyzer.analyze()
    analyzer.simple_prediction()

if __name__ == "__main__":
    main()