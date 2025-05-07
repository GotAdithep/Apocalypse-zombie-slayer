import pygame
import csv

class Database:
    def __init__(self, game, file_path="database.csv"):
        self.game = game                   # Reference to the Game object
        self.player = game.player          # Reference to the Player object

        # Ensure the player has an 'attack_count' attribute (if not, initialize it).
        if not hasattr(self.player, 'attack_count'):
            self.player.attack_count = 0

        # Lists to store data every interval (now every 10 seconds)
        self.damage_taken = []             # Damage values each 10 sec
        self.coin_collect = []             # Net coin change each 10 sec (if negative, record 0)
        self.zombie_killed = []            # Number of zombie kills each 10 sec
        self.player_attack_count = []      # Number of attacks (left clicks) each 10 sec
        self.zombie_type = []              # Types of zombies killed (recorded immediately per kill)

        self.last_check_time = pygame.time.get_ticks()  # Timer for interval checks
        self.last_coin_count = game.coin_count          # Coin count at last check
        self.last_zombie_killed = game.zombies_killed     # Zombie kill count at last check
        self.last_attack_count = self.player.attack_count # Attack count at last check

        self.file_path = file_path

    def register_zombie_kill(self, zombie_type):

        self.zombie_type.append(zombie_type)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_check_time >= 10000:

            damage_amount = round(200 - self.player.health, 2)
            self.damage_taken.append(damage_amount)
            
            coins_change = self.game.coin_count - self.last_coin_count
            if coins_change < 0:
                self.coin_collect.append(0)
            else:
                self.coin_collect.append(coins_change)
            
            new_zombie_killed = self.game.zombies_killed - self.last_zombie_killed
            self.zombie_killed.append(new_zombie_killed)
            
            attack_change = self.player.attack_count - self.last_attack_count
            self.player_attack_count.append(attack_change)
            
            self.last_coin_count = self.game.coin_count
            self.last_zombie_killed = self.game.zombies_killed
            self.last_attack_count = self.player.attack_count
            self.last_check_time = current_time

            print(f"Damage collected: {damage_amount}, Total damage records: {self.damage_taken}")
            print(f"Coin collect (net): {self.coin_collect[-1]}, Total coin records: {self.coin_collect}")
            print(f"Zombies killed in interval: {new_zombie_killed}, Total zombie kill records: {self.zombie_killed}")
            print(f"Player attack count in interval: {attack_change}, Total attack records: {self.player_attack_count}")
            print(f"Zombie types recorded: {self.zombie_type}")

    def save_data_to_csv(self):

        data = {
            "damage_taken(10sec)": self.damage_taken,
            "coin_collect(10sec)": self.coin_collect,
            "zombie_killed(10sec)": self.zombie_killed,
            "player_attack_count(10sec)": self.player_attack_count,
            "zombie_type(10sec)": self.zombie_type
        }
        with open(self.file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            max_length = max(len(v) for v in data.values())
            for i in range(max_length):
                row = []
                for key in data.keys():
                    row.append(str(data[key][i]) if i < len(data[key]) else "")
                writer.writerow(row)
        print(f"Data saved to {self.file_path}.")

    def load_data_from_csv(self):

        db = {}
        with open(self.file_path, "r") as fp:
            reader = csv.reader(fp)
            headers = next(reader)
            for header in headers:
                db[header] = []
            for row in reader:
                for i, value in enumerate(row):
                    if i < len(headers):
                        db[headers[i]].append(value)
        return db