import json
import os
import random

# ==============================
# Weapon Class
# ==============================
class Weapon:
    def __init__(self, name, damage, durability):
        self.name = name
        self.damage = damage
        self.durability = durability

    def is_broken(self):
        return self.durability <= 0

    def use(self):
        if self.durability > 0:
            self.durability -= 1
        # Damage decreases when durability is low (below 3)
        if self.durability <= 0:
            return 0
        elif self.durability < 3:
            return max(1, self.damage // 2)
        return self.damage

    def repair(self, amount):
        self.durability += amount

    def to_dict(self):
        return {
            "name": self.name,
            "damage": self.damage,
            "durability": self.durability
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["damage"], data["durability"])


# ==============================
# Base Survivor Class
# ==============================
class Survivor:
    def __init__(self, name, health, weapon):
        self.name = name
        self.health = health
        self.max_health = health
        self.weapon = weapon
        self.role = "Survivor"

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def attack(self):
        if self.weapon.is_broken():
            print(f"  {self.name}'s {self.weapon.name} is broken and cannot attack!")
            return 0
        damage = self.weapon.use()
        return damage

    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "weapon": self.weapon.to_dict(),
            "role": self.role
        }

    @classmethod
    def from_dict(cls, data):
        weapon = Weapon.from_dict(data["weapon"])
        role = data.get("role", "Survivor")
        if role == "Soldier":
            obj = Soldier(data["name"], data["max_health"], weapon)
        elif role == "Medic":
            obj = Medic(data["name"], data["max_health"], weapon)
            obj.medkit_uses = data.get("medkit_uses", 3)
        elif role == "Engineer":
            obj = Engineer(data["name"], data["max_health"], weapon)
            obj.toolbox_durability = data.get("toolbox_durability", 5)
        else:
            obj = Survivor(data["name"], data["max_health"], weapon)
        obj.health = data["health"]
        return obj


# ==============================
# Soldier Class
# ==============================
class Soldier(Survivor):
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)
        self.role = "Soldier"


# ==============================
# Medic Class
# ==============================
class Medic(Survivor):
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)
        self.role = "Medic"
        self.medkit_uses = 3

    def heal(self, target):
        if self.medkit_uses <= 0:
            print(f"  {self.name} has no medkits left!")
            return
        if not target.is_alive():
            print(f"  {target.name} is already dead. Cannot heal.")
            return
        heal_amount = min(20, target.max_health - target.health)
        target.health += heal_amount
        self.medkit_uses -= 1
        print(f"  {self.name} heals {target.name} for {heal_amount} HP. "
              f"({target.health}/{target.max_health} HP) | Medkits left: {self.medkit_uses}")

    def to_dict(self):
        d = super().to_dict()
        d["medkit_uses"] = self.medkit_uses
        return d

    @classmethod
    def from_dict(cls, data):
        weapon = Weapon.from_dict(data["weapon"])
        obj = cls(data["name"], data["max_health"], weapon)
        obj.health = data["health"]
        obj.medkit_uses = data.get("medkit_uses", 3)
        return obj


# ==============================
# Engineer Class
# ==============================
class Engineer(Survivor):
    def __init__(self, name, health, weapon):
        super().__init__(name, health, weapon)
        self.role = "Engineer"
        self.toolbox_durability = 5

    def build_defense(self, game):
        if self.toolbox_durability <= 0:
            print(f"  {self.name}'s toolbox is depleted!")
            return
        game.defense_level += 5
        self.toolbox_durability -= 1
        print(f"  {self.name} builds defenses! Defense level is now {game.defense_level}. "
              f"| Toolbox uses left: {self.toolbox_durability}")

    def repair_weapon(self, target):
        if self.toolbox_durability <= 0:
            print(f"  {self.name}'s toolbox is depleted!")
            return
        if target.weapon.is_broken():
            repair_amount = 5
        else:
            repair_amount = 3
        target.weapon.repair(repair_amount)
        self.toolbox_durability -= 1
        print(f"  {self.name} repairs {target.name}'s {target.weapon.name} by {repair_amount}. "
              f"Durability now: {target.weapon.durability} | Toolbox uses left: {self.toolbox_durability}")

    def to_dict(self):
        d = super().to_dict()
        d["toolbox_durability"] = self.toolbox_durability
        return d

    @classmethod
    def from_dict(cls, data):
        weapon = Weapon.from_dict(data["weapon"])
        obj = cls(data["name"], data["max_health"], weapon)
        obj.health = data["health"]
        obj.toolbox_durability = data.get("toolbox_durability", 5)
        return obj


# ==============================
# Zombie Class
# ==============================
class Zombie:
    def __init__(self, health, attack_power):
        self.health = health
        self.max_health = health
        self.attack_power = attack_power

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def attack(self, target):
        damage = self.attack_power
        target.take_damage(damage)
        print(f"  The zombie attacks {target.name} for {damage} damage! "
              f"({target.health}/{target.max_health} HP remaining)")


# ==============================
# Main Game Class
# ==============================
class ZombieGame:
    def __init__(self):
        self.squad = []
        self.zombie = None
        self.defense_level = 0
        self.day = 1

    def show_status(self):
        print("\n" + "=" * 65)
        print(f"  DAY {self.day}  |  Defense Level: {self.defense_level}")
        print("=" * 65)
        print(f"  {'ID':<4} {'Name':<12} {'Role':<10} {'HP':<10} {'Weapon':<14} {'Dur':<5} {'Special'}")
        print("-" * 65)
        for i, s in enumerate(self.squad):
            status = "(DEAD)" if not s.is_alive() else ""
            hp_str = f"{s.health}/{s.max_health}"
            broken = " [BROKEN]" if s.weapon.is_broken() else ""
            weapon_str = s.weapon.name + broken

            special = ""
            if isinstance(s, Medic):
                special = f"Medkits: {s.medkit_uses}"
            elif isinstance(s, Engineer):
                special = f"Toolbox: {s.toolbox_durability}"

            print(f"  [{i}]  {s.name:<12} {s.role:<10} {hp_str:<10} {weapon_str:<14} "
                  f"{s.weapon.durability:<5} {special} {status}")
        print("-" * 65)
        if self.zombie and self.zombie.is_alive():
            print(f"  ZOMBIE  |  HP: {self.zombie.health}/{self.zombie.max_health}"
                  f"  |  Attack: {self.zombie.attack_power}")
        else:
            print("  No zombie present.")
        print("=" * 65)

    def setup_game(self):
        rifle   = Weapon("Rifle",    25, 8)
        pistol  = Weapon("Pistol",   15, 10)
        wrench  = Weapon("Wrench",   12, 10)
        shotgun = Weapon("Shotgun",  30, 6)

        self.squad = [
            Soldier("Marcus",  100, rifle),
            Medic("Elena",      80, pistol),
            Engineer("Tyson",   90, wrench),
            Soldier("Riya",    100, shotgun),
        ]
        self.zombie = Zombie(60, 18)
        self.defense_level = 0
        self.day = 1
        print("\n  Squad assembled. A zombie approaches...")

    def save_game(self, filename="save.json"):
        try:
            data = {
                "squad": [s.to_dict() for s in self.squad],
                "zombie": {
                    "health": self.zombie.health,
                    "max_health": self.zombie.max_health,
                    "attack_power": self.zombie.attack_power
                } if self.zombie else None,
                "defense_level": self.defense_level,
                "day": self.day
            }
            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  Game saved to '{filename}'.")
        except PermissionError:
            print(f"  ERROR: No permission to write '{filename}'.")
        except Exception as e:
            print(f"  ERROR saving game: {e}")

    def load_game(self, filename="save.json"):
        if not os.path.exists(filename):
            print(f"  ERROR: Save file '{filename}' not found.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.squad = [Survivor.from_dict(s) for s in data["squad"]]
            zd = data["zombie"]
            if zd:
                self.zombie = Zombie(zd["health"], zd["attack_power"])
                self.zombie.max_health = zd.get("max_health", zd["health"])
            else:
                self.zombie = None
            self.defense_level = data["defense_level"]
            self.day = data["day"]
            print(f"  Game loaded from '{filename}'.")
        except json.JSONDecodeError:
            print("  ERROR: Save file is corrupted or invalid JSON.")
        except KeyError as e:
            print(f"  ERROR: Save file is missing expected data: {e}")
        except Exception as e:
            print(f"  ERROR loading game: {e}")

    def zombie_turn(self):
        if not self.zombie or not self.zombie.is_alive():
            return
        alive = [s for s in self.squad if s.is_alive()]
        if not alive:
            return
        target = random.choice(alive)
        raw_damage = self.zombie.attack_power
        actual_damage = max(0, raw_damage - self.defense_level)
        target.take_damage(actual_damage)
        print(f"\n  >> The zombie lunges at {target.name} for "
              f"{raw_damage} - {self.defense_level} (defense) = {actual_damage} damage!"
              f"  ({target.health}/{target.max_health} HP)")
        if not target.is_alive():
            print(f"  !! {target.name} has fallen!")

    def _pick_survivor(self, prompt="Select survivor ID: ", alive_only=True):
        """Helper: prompt for a valid survivor index. Returns survivor or None."""
        for i, s in enumerate(self.squad):
            tag = "" if s.is_alive() else " (DEAD)"
            print(f"    [{i}] {s.name} ({s.role}){tag}")
        try:
            idx = int(input(f"  {prompt}"))
            if idx < 0 or idx >= len(self.squad):
                print("  Invalid selection.")
                return None
            chosen = self.squad[idx]
            if alive_only and not chosen.is_alive():
                print(f"  {chosen.name} is dead.")
                return None
            return chosen
        except ValueError:
            print("  Please enter a number.")
            return None

    def play(self):
        self.setup_game()

        while True:
            self.show_status()

            # --- Win condition ---
            if self.zombie and not self.zombie.is_alive():
                self.day += 1
                new_hp  = 60 + (self.day - 1) * 20
                new_atk = 18 + (self.day - 1) * 5
                self.zombie = Zombie(new_hp, new_atk)
                print(f"\n  *** Zombie defeated! A stronger zombie appears on Day {self.day}! ***")
                print(f"      New Zombie  HP: {new_hp}  |  Attack: {new_atk}")
                continue

            # --- Lose condition ---
            if not any(s.is_alive() for s in self.squad):
                print("\n  *** All survivors have fallen. GAME OVER. ***\n")
                break

            # --- Menu ---
            print("\n  What will you do?")
            print("  [1] Attack Zombie")
            print("  [2] Heal (Medic only)")
            print("  [3] Build Defense (Engineer only)")
            print("  [4] Repair Weapon (Engineer only)")
            print("  [5] Save Game")
            print("  [6] Load Game")
            print("  [7] Exit")

            choice = input("\n  Enter choice: ").strip()

            if choice == "1":
                # Attack Zombie
                if not self.zombie or not self.zombie.is_alive():
                    print("  No zombie to attack.")
                    continue
                print("\n  Choose attacker:")
                attacker = self._pick_survivor("Attacker ID: ")
                if attacker is None:
                    continue
                damage = attacker.attack()
                if damage > 0:
                    self.zombie.take_damage(damage)
                    print(f"  {attacker.name} attacks the zombie for {damage} damage! "
                          f"(Zombie HP: {self.zombie.health}/{self.zombie.max_health})")
                    if not self.zombie.is_alive():
                        print("  *** The zombie is dead! ***")
                        continue   # skip zombie turn, handle at top of loop
                self.zombie_turn()

            elif choice == "2":
                # Heal
                medics = [s for s in self.squad if isinstance(s, Medic) and s.is_alive()]
                if not medics:
                    print("  No alive Medics in your squad.")
                    continue
                print("\n  Choose Medic:")
                medic = self._pick_survivor("Medic ID: ")
                if medic is None or not isinstance(medic, Medic):
                    print("  That survivor is not a Medic.")
                    continue
                print("\n  Choose target to heal:")
                target = self._pick_survivor("Target ID: ")
                if target is None:
                    continue
                medic.heal(target)
                self.zombie_turn()

            elif choice == "3":
                # Build Defense
                engineers = [s for s in self.squad if isinstance(s, Engineer) and s.is_alive()]
                if not engineers:
                    print("  No alive Engineers in your squad.")
                    continue
                print("\n  Choose Engineer:")
                eng = self._pick_survivor("Engineer ID: ")
                if eng is None or not isinstance(eng, Engineer):
                    print("  That survivor is not an Engineer.")
                    continue
                eng.build_defense(self)
                self.zombie_turn()

            elif choice == "4":
                # Repair Weapon
                engineers = [s for s in self.squad if isinstance(s, Engineer) and s.is_alive()]
                if not engineers:
                    print("  No alive Engineers in your squad.")
                    continue
                print("\n  Choose Engineer:")
                eng = self._pick_survivor("Engineer ID: ")
                if eng is None or not isinstance(eng, Engineer):
                    print("  That survivor is not an Engineer.")
                    continue
                print("\n  Choose whose weapon to repair:")
                target = self._pick_survivor("Target ID: ")
                if target is None:
                    continue
                eng.repair_weapon(target)
                self.zombie_turn()

            elif choice == "5":
                fname = input("  Save filename (press Enter for 'save.json'): ").strip()
                if not fname:
                    fname = "save.json"
                self.save_game(fname)

            elif choice == "6":
                fname = input("  Load filename (press Enter for 'save.json'): ").strip()
                if not fname:
                    fname = "save.json"
                self.load_game(fname)

            elif choice == "7":
                print("  Goodbye. Stay safe out there.")
                break

            else:
                print("  Invalid option. Please enter 1-7.")


# ==============================
# Main Function
# ==============================
def main():
    game = ZombieGame()
    game.play()


if __name__ == "__main__":
    main()
