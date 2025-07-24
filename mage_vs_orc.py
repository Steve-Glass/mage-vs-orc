#!/usr/bin/env python3
"""
Mage vs. Orc - Turn-based Terminal Combat Game

A Pokemon-style turn-based combat game where a Mage battles the Orc King.
The player controls the Mage and selects moves each turn, while the Orc King
responds with random moves until one character's HP reaches zero.
"""

import random
import os
import sys


class Move:
    """Represents a combat move with damage, effects, and description."""
    
    def __init__(self, name, damage, description, special_effect=None):
        self.name = name
        self.damage = damage
        self.description = description
        self.special_effect = special_effect
    
    def __str__(self):
        return f"{self.name} ({self.damage} damage): {self.description}"


class Character:
    """Base class for all combat characters."""
    
    def __init__(self, name, max_hp, move_set):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.move_set = move_set
    
    def is_alive(self):
        """Check if character still has HP remaining."""
        return self.current_hp > 0
    
    def take_damage(self, damage):
        """Apply damage to character, ensuring HP doesn't go below 0."""
        self.current_hp = max(0, self.current_hp - damage)
    
    def heal(self, amount):
        """Restore HP, ensuring it doesn't exceed maximum."""
        self.current_hp = min(self.max_hp, self.current_hp + amount)
    
    def get_hp_display(self):
        """Return formatted HP display string."""
        hp_bar_length = 20
        hp_percentage = self.current_hp / self.max_hp
        filled_bars = int(hp_percentage * hp_bar_length)
        empty_bars = hp_bar_length - filled_bars
        
        hp_bar = "█" * filled_bars + "░" * empty_bars
        return f"{self.name}: {self.current_hp}/{self.max_hp} HP [{hp_bar}]"
    
    def get_random_move(self):
        """Select a random move from the character's move set."""
        return random.choice(self.move_set)


class Mage(Character):
    """The player-controlled Mage character with magical abilities."""
    
    def __init__(self):
        # Define the Mage's unique move set
        move_set = [
            Move("Fireball", 25, "Launches a blazing sphere of fire"),
            Move("Lightning Bolt", 30, "Strikes with crackling electricity"),
            Move("Heal", 0, "Restores 20 HP", special_effect="heal_20"),
            Move("Magic Missile", 20, "An unerring bolt of magical energy")
        ]
        super().__init__("Mage", 100, move_set)


class OrcKing(Character):
    """The AI-controlled Orc King with brutal physical attacks."""
    
    def __init__(self):
        # Define the Orc King's unique move set
        move_set = [
            Move("Axe Swing", 28, "A devastating swing of the battle axe"),
            Move("Battle Roar", 15, "A terrifying roar that rattles enemies", special_effect="intimidate"),
            Move("Charge", 22, "Rushes forward with crushing force"),
            Move("Slam", 26, "Brings down both fists with tremendous power")
        ]
        super().__init__("Orc King", 120, move_set)


class Game:
    """Main game controller handling the battle loop and user interface."""
    
    def __init__(self):
        self.mage = Mage()
        self.orc_king = OrcKing()
        self.turn_count = 1
    
    def clear_screen(self):
        """Clear the terminal screen for better readability."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_title(self):
        """Display the game title and setup."""
        print("=" * 50)
        print("       🧙‍♂️  MAGE VS. ORC KING  👹")
        print("=" * 50)
        print("A turn-based battle to the death!")
        print()
    
    def display_battle_status(self):
        """Show current HP status for both characters."""
        print("BATTLE STATUS:")
        print("-" * 30)
        print(self.mage.get_hp_display())
        print(self.orc_king.get_hp_display())
        print()
    
    def display_move_menu(self):
        """Show available moves for the player to choose from."""
        print(f"Turn {self.turn_count} - Choose your move:")
        print("-" * 30)
        for i, move in enumerate(self.mage.move_set, 1):
            print(f"{i}. {move}")
        print()
    
    def get_player_move_choice(self):
        """Get and validate player's move selection."""
        while True:
            try:
                choice = input("Enter move number (1-4): ").strip()
                move_index = int(choice) - 1
                
                if 0 <= move_index < len(self.mage.move_set):
                    return self.mage.move_set[move_index]
                else:
                    print("Invalid choice! Please enter a number between 1 and 4.")
                    
            except ValueError:
                print("Invalid input! Please enter a number.")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                sys.exit(0)
    
    def execute_move(self, attacker, defender, move):
        """Execute a move and return the result message."""
        result_message = f"{attacker.name} uses {move.name}!"
        
        # Handle special effects
        if move.special_effect == "heal_20":
            attacker.heal(20)
            result_message += f" {attacker.name} recovers 20 HP!"
        elif move.special_effect == "intimidate":
            # Battle Roar does damage plus intimidation effect
            defender.take_damage(move.damage)
            result_message += f" {defender.name} takes {move.damage} damage and is intimidated!"
        else:
            # Regular damage move
            defender.take_damage(move.damage)
            result_message += f" {defender.name} takes {move.damage} damage!"
        
        return result_message
    
    def check_battle_end(self):
        """Check if the battle has ended and return the winner."""
        if not self.mage.is_alive():
            return "defeat"
        elif not self.orc_king.is_alive():
            return "victory"
        return None
    
    def display_battle_end(self, result):
        """Display the final battle result."""
        print("=" * 50)
        if result == "victory":
            print("🎉 VICTORY! 🎉")
            print("The Mage has defeated the Orc King!")
            print("Your magical prowess has saved the realm!")
        else:
            print("💀 DEFEAT! 💀")
            print("The Orc King has overwhelmed the Mage!")
            print("The realm falls to darkness...")
        print("=" * 50)
    
    def play_turn(self):
        """Execute a single turn of combat."""
        # Display current battle state
        self.display_battle_status()
        
        # Player's turn
        self.display_move_menu()
        player_move = self.get_player_move_choice()
        print()
        
        # Execute player move
        player_result = self.execute_move(self.mage, self.orc_king, player_move)
        print(player_result)
        
        # Check if battle ended after player's move
        battle_result = self.check_battle_end()
        if battle_result:
            return battle_result
        
        # Orc King's turn (AI)
        orc_move = self.orc_king.get_random_move()
        orc_result = self.execute_move(self.orc_king, self.mage, orc_move)
        print(orc_result)
        print()
        
        # Check if battle ended after Orc King's move
        battle_result = self.check_battle_end()
        if battle_result:
            return battle_result
        
        # Prepare for next turn
        self.turn_count += 1
        input("Press Enter to continue...")
        print()
        
        return None
    
    def run(self):
        """Main game loop."""
        self.clear_screen()
        self.display_title()
        
        print("The ancient Mage faces the dreaded Orc King in mortal combat!")
        print("Choose your moves wisely to emerge victorious!")
        print()
        input("Press Enter to begin the battle...")
        print()
        
        # Main battle loop
        while True:
            battle_result = self.play_turn()
            if battle_result:
                self.display_battle_status()
                self.display_battle_end(battle_result)
                break
        
        # Ask if player wants to play again
        print()
        play_again = input("Would you like to play again? (y/n): ").lower().strip()
        if play_again.startswith('y'):
            # Reset the game state
            self.__init__()
            self.run()


def main():
    """Entry point for the game."""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nThanks for playing Mage vs. Orc King!")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please try running the game again.")


if __name__ == "__main__":
    main()