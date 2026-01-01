import logging
import sys
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        # Initialize client with testnet flag
        self.client = Client(api_key, api_secret, testnet=testnet)
        
        # Explicitly point to Futures Testnet URL
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        self._setup_logging()
        logging.info("Bot initialized. Ready for Testnet interaction.")

    def _setup_logging(self):
        """Requirement: Log API requests, responses, and errors."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("trading_bot.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _handle_order(self, order_func, **kwargs):
        """Generic wrapper to handle API calls and errors."""
        try:
            logging.info(f"Sending Request: {kwargs}")
            response = order_func(**kwargs)
            logging.info(f"API Response: {response}")
            return response
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error(f"Order Failed: {e.status_code} - {e.message}")
            return None

    def place_market_order(self, symbol, side, quantity):
        return self._handle_order(
            self.client.futures_create_order,
            symbol=symbol.upper(),
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )

    def place_limit_order(self, symbol, side, quantity, price):
        return self._handle_order(
            self.client.futures_create_order,
            symbol=symbol.upper(),
            side=side.upper(),
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=str(price)
        )

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
      """Bonus: Corrected Stop-Limit order type for Futures."""
      return self._handle_order(
        self.client.futures_create_order,
        symbol=symbol.upper(),
        side=side.upper(),
        type='STOP',           # Changed from 'STOP_LOSS_LIMIT' to 'STOP'
        timeInForce='GTC',
        quantity=quantity,
        price=str(price),      # The price you want to sell at
        stopPrice=str(stop_price) # The price that triggers the order
    )

def get_valid_input(prompt, type_=str, choices=None):
    """Utility to validate CLI input."""
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                raise ValueError("Input cannot be empty.")
            
            converted_value = type_(value)
            
            if choices and converted_value.upper() not in choices:
                raise ValueError(f"Must be one of {choices}")
            
            return converted_value.upper() if type_ == str else converted_value
        except ValueError as e:
            print(f"Invalid input: {e}")

def main():
    print("\n" + "="*40)
    print("   BINANCE FUTURES TESTNET BOT")
    print("="*40)

    api_key = input("Enter API Key: ").strip()
    api_secret = input("Enter API Secret: ").strip()

    if not api_key or not api_secret:
        print("Error: API Credentials required.")
        return

    bot = BasicBot(api_key, api_secret)

    # 1. Collect Order Parameters
    symbol = get_valid_input("Enter Symbol (e.g., BTCUSDT): ")
    side = get_valid_input("Side (BUY/SELL): ", choices=['BUY', 'SELL'])
    order_type = get_valid_input("Order Type (MARKET/LIMIT/STOP_LIMIT): ", 
                                 choices=['MARKET', 'LIMIT', 'STOP_LIMIT'])
    quantity = get_valid_input("Quantity: ", type_=float)

    # 2. Execute based on type
    result = None
    if order_type == "MARKET":
        result = bot.place_market_order(symbol, side, quantity)
    
    elif order_type == "LIMIT":
        price = get_valid_input("Limit Price: ", type_=float)
        result = bot.place_limit_order(symbol, side, quantity, price)
    
    elif order_type == "STOP_LIMIT":
        stop_price = get_valid_input("Stop Price: ", type_=float)
        limit_price = get_valid_input("Limit Price: ", type_=float)
        result = bot.place_stop_limit_order(symbol, side, quantity, limit_price, stop_price)

    # 3. Requirement: Output Execution Status
    if result:
        print("\n" + "-"*40)
        print("✅ ORDER SUCCESSFUL")
        print(f"Order ID:  {result.get('orderId')}")
        print(f"Status:    {result.get('status')}")
        print(f"Type:      {result.get('type')}")
        print(f"Avg Price: {result.get('avgPrice', 'N/A')}")
        print("-"*40)
    else:
        print("\n❌ ORDER FAILED. See trading_bot.log for details.")

if __name__ == "__main__":
    main()