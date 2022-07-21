__author__ = "Alon B.R."

from os.path import join


class HandleCoins:
    def __init__(self) -> None:
        self.path: str = join("Assets", "coins.txt")
        with open(self.path, "r+") as coins_file:
            coins_file.seek(0)
            coins = coins_file.read()
            if len(coins) > 0:
                coins = int(coins)
                self.coins = coins
            else:
                coins_file.seek(0)
                coins_file.truncate()
                coins_file.write("0")
                self.coins = 0

    def write_new(self, coins) -> None:
        if self.coins < int(coins):
            with open(self.path, "w") as coins_file:
                coins_file.seek(0)
                coins_file.truncate()
                coins_file.write(str(coins))
                self.coins = coins


if __name__ == "__main__":
    handle_coins = HandleCoins()
