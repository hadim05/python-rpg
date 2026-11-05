import random
import json


class character:
    def __init__(self, name, health, attack_power):
        self.gold = 0
        self.defending = False
        self.equipped_weapon = None
        self.inventory = []
        self.max_health = health
        self.level = 1
        self.xp = 0
        self.name = name
        self.__health = health
        self.attack_power = attack_power

    def save_game(self):
        data = {
            "name": self.name,
            "xp": self.xp,
            "level": self.level,
            "gold": self.gold,
            "inventory": self.inventory,
            "health": self.__health,
            "attack power": self.attack_power,
            "equipped_weapon": self.equipped_weapon,
            "max_health": self.max_health,
        }
        with open("save.json", "w") as file:
            json.dump(data, file)

            print("Game saved successfully!")

    def load_game(self):
        try:
            with open("save.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("game save dont exist")
            return

        self.name = data["name"]
        self.xp = data["xp"]
        self.level = data["level"]
        self.gold = data["gold"]
        self.inventory = data["inventory"]
        self.__health = data["health"]
        self.attack_power = data["attack power"]
        self.equipped_weapon = data["equipped_weapon"]
        self.max_health = data["max_health"]

    def earn_gold(self, amount):
        if amount > 0:
            self.gold = self.gold + amount
            print(amount)
            print(self.gold)

    def ai_turn(self, target):
        if not self.is_alive():
            return

        number = random.randint(1, 100)

        if self.health <= self.max_health * 0.30 and "health potion" in self.inventory:
            self.use_potion()

        elif number <= 60:
            self.attack(target)
        elif number >= 61 and number <= 80:
            self.defend()
        else:
            if "health potion" in self.inventory and self.health < self.max_health:
                self.use_potion()
            else:
                self.attack(target)

    def defend(self):
        self.defending = True
        print("defending")

    def add_item(self, item):
        self.inventory.append(item)

    def remove_item(self, item):
        if item in self.inventory:
            if item == self.equipped_weapon:
                self.unequip_weapon()

            self.inventory.remove(item)
            print("item removed succesfully")
        else:
            print("item not found")

    def equip_weapon(self, weapon):
        if weapon in self.inventory:
            if weapon == "sword" and self.equipped_weapon is None:
                self.attack_power += 10
                self.equipped_weapon = weapon
                print("sword equiped")
            else:
                print("cannot eqiup weapon")
        else:
            print("weapon not found")

    def unequip_weapon(self):
        if self.equipped_weapon is not None:
            self.equipped_weapon = None
            self.attack_power = self.attack_power - 10
            print("weapon unequipped")
        else:
            print("no weapon equipped")

    def use_potion(self):
        if "health potion" in self.inventory and self.is_alive():
            self.heal(30)
            self.inventory.remove("health potion")
            print("health potion used")
        else:
            print("health potion not found")

    def gain_xp(self, amount):
        if amount > 0:
            self.xp = self.xp + amount
            while self.xp >= 100:
                self.level = self.level + 1
                self.xp = self.xp - 100
                self.attack_power = self.attack_power + 5

    def take_damage(self, amount):
        if amount > 0:
            if self.defending == True:
                amount = amount / 2
                self.defending = False
            self.__health = self.__health - amount

            if self.__health < 0:
                self.__health = 0

    def heal(self, amount):
        if amount > 0 and self.health > 0:
            self.__health += amount
        if self.__health > self.max_health:
            self.__health = self.max_health

    @property
    def health(self):
        return self.__health

    def __str__(self):
        return f"name: {self.name}| health: {self.__health}| attack: {self.attack_power}|level:{self.level}|xp:{self.xp}|gold:{self.gold}|inventory: {self.inventory}"

    def attack(self, target):
        if self.health > 0:
            number = random.randint(1, 100)

            if number <= 20:
                damage = self.attack_power * 2
                print("Critical hit!")
            else:
                damage = self.attack_power

            target.take_damage(damage)
        else:
            print("Dead characters cannot attack!")

    def is_alive(self):
        if self.health > 0:
            return True
        else:
            return False


class battle:
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2

    def start_battle(self):
        print("Battle started:", self.fighter1.name, "VS", self.fighter2.name)

    def play_round(self):
        self.player_turn()
        if self.fighter2.is_alive():
            self.fighter2.ai_turn(self.fighter1)
            print(self.fighter1.health)
            print(self.fighter2.health)

    def fight_to_death(self):
        while self.fighter1.is_alive() and self.fighter2.is_alive():
            self.play_round()
        if self.fighter1.is_alive():
            self.fighter1.gain_xp(50)
            self.fighter1.earn_gold(25)
            print(self.fighter1.name, "is the winner")
        elif self.fighter2.is_alive():
            self.fighter2.gain_xp(50)
            self.fighter2.earn_gold(25)
            print(self.fighter2.name, "is the winner")

    def player_turn(self):
        print("1. Attack")
        print("2. Defend")
        print("3  use health potion")
        while True:
            choice = input("Choose your next move: ")

            if choice == "1":
                self.fighter1.attack(self.fighter2)
                break
            elif choice == "2":
                self.fighter1.defend()
                break
            elif choice == "3":
                self.fighter1.use_potion()
                break
            else:
                print("Invalid option")


class warrior(character):
    def __init__(self, name, health, attack_power, armor):
        super().__init__(name, health, attack_power)
        self.armor = armor

    def take_damage(self, amount):
        absorbed = min(self.armor, amount)
        self.armor = self.armor - absorbed
        actual_damage = amount - absorbed
        super().take_damage(actual_damage)


class mage(character):
    def __init__(self, name, health, attack_power, mana):
        super().__init__(name, health, attack_power)
        self.mana = mana

    def cast_spells(self, mana_cost):
        if mana_cost > 0 and self.mana >= mana_cost:
            self.mana = self.mana - mana_cost
            print("spell casted sucesfully")
        else:
            print("not enough mana")


class shop:
    def __init__(self):
        self.items = {"health potion": 20, "sword": 50}

    def show_items(self):

        for item, price in self.items.items():
            print(item, ":", price, "gold")

    def buy_item(self, player, item):

        if item in self.items:
            price = self.items[item]
            if player.gold >= price:
                player.gold = player.gold - price
                player.add_item(item)
            else:
                print("not enough gold")
        else:
            print("item not found")

    def sell_item(self, player, item):
        if item in player.inventory and item in self.items:
            price = self.items[item]
            selling_price = price / 2
            player.earn_gold(selling_price)
            player.remove_item(item)
        else:
            print("cannot sell this item")

    def open_shop(self, player):
        print("1. view items")
        print("2. buy items")
        print("3. sell items")
        print("4. leave shop")
        while True:
            choice = input("choose an option")
            if choice == "1":
                self.show_items()
            elif choice == "2":
                item = input("What would you like to buy? ")
                self.buy_item(player, item)
            elif choice == "3":
                item = input("What would you like to sell? ")
                self.sell_item(player, item)
            elif choice == "4":
                print("leaving shop")
                break
            else:
                print("invalid choice")


def main_menu():
    while True:
        print("1. start battle")
        print("2. open shop ")
        print("3. veiw character")
        print("4. save game")
        print("5. laod game")
        print("6. Exit")
        choice = input("choose yor next move")
        if choice == "1":
            if hero1.health > 0:
                hero2 = character("Goblin", 80, 15)
                fight = battle(hero1, hero2)
                fight.fight_to_death()
            else:
                print("u are dead load a saved fle to continou")
        elif choice == "2":
            rpg_shop.open_shop(hero1)
        elif choice == "3":
            print(hero1)
            print("Equipped weapon:", hero1.equipped_weapon)
            print("Max health:", hero1.max_health)
        elif choice == "4":
            hero1.save_game()
        elif choice == "5":
            hero1.load_game()
        elif choice == "6":
            print("exit")
            break
        else:
            print("invalid option")


hero1 = character("arthur", 100, 20)
rpg_shop = shop()

main_menu()
