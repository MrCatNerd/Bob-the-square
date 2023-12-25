import os


class HandleCoins:
    def __init__(self) -> None:
        self.path: str = "Assets/coins.txt"
        self.create_file_if_not_exists()  # Create file if it doesn't exist
        self.read_coins()

    def create_file_if_not_exists(self) -> None:
        if not os.path.exists(self.path):
            with open(self.path, "w") as coins_file:
                coins_file.write("0")

    def read_coins(self) -> None:
        with open(self.path, "r") as coins_file:
            coins = coins_file.read().strip()  # Remove whitespace characters
            if coins.isdigit():
                self.coins = int(coins)
            else:
                self.coins = 0

    def write_new(self, coins) -> None:
        coins = int(coins)
        if self.coins < coins:
            with open(self.path, "w") as coins_file:
                coins_file.write(str(coins))
                self.coins = coins


if __name__ == "__main__":
    handle_coins = HandleCoins()

    # Example usage:
    print("Current coins:", handle_coins.coins)

    new_coins = input("Enter new coins: ")
    handle_coins.write_new(new_coins)

    print("Updated coins:", handle_coins.coins)
