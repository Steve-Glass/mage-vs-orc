#!/usr/bin/env python3
"""
Basic tests for Mage vs. Orc King game functionality.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the game module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mage_vs_orc


class TestMove:
    """Test the Move class functionality."""
    
    def test_move_creation(self):
        """Test that moves can be created with basic properties."""
        move = mage_vs_orc.Move("Fireball", 25, "A blazing sphere of fire")
        assert move.name == "Fireball"
        assert move.damage == 25
        assert move.description == "A blazing sphere of fire"
        assert move.special_effect is None
    
    def test_move_with_special_effect(self):
        """Test that moves can be created with special effects."""
        move = mage_vs_orc.Move("Heal", 0, "Restores HP", special_effect="heal_20")
        assert move.name == "Heal"
        assert move.damage == 0
        assert move.special_effect == "heal_20"
    
    def test_move_string_representation(self):
        """Test the string representation of moves."""
        move = mage_vs_orc.Move("Lightning Bolt", 30, "Crackling electricity")
        expected = "Lightning Bolt (30 damage): Crackling electricity"
        assert str(move) == expected


class TestCharacter:
    """Test the Character base class functionality."""
    
    def test_character_creation(self):
        """Test that characters can be created with basic stats."""
        moves = [mage_vs_orc.Move("Attack", 10, "Basic attack")]
        character = mage_vs_orc.Character("Test Character", 100, moves)
        assert character.name == "Test Character"
        assert character.max_hp == 100
        assert character.current_hp == 100
        assert len(character.move_set) == 1
    
    def test_character_is_alive(self):
        """Test the is_alive method."""
        moves = [mage_vs_orc.Move("Attack", 10, "Basic attack")]
        character = mage_vs_orc.Character("Test Character", 100, moves)
        assert character.is_alive() is True
        
        character.current_hp = 0
        assert character.is_alive() is False
    
    def test_character_take_damage(self):
        """Test the take_damage method."""
        moves = [mage_vs_orc.Move("Attack", 10, "Basic attack")]
        character = mage_vs_orc.Character("Test Character", 100, moves)
        
        character.take_damage(25)
        assert character.current_hp == 75
        
        # Test that HP doesn't go below 0
        character.take_damage(100)
        assert character.current_hp == 0
    
    def test_character_heal(self):
        """Test the heal method."""
        moves = [mage_vs_orc.Move("Attack", 10, "Basic attack")]
        character = mage_vs_orc.Character("Test Character", 100, moves)
        
        character.current_hp = 50
        character.heal(25)
        assert character.current_hp == 75
        
        # Test that HP doesn't exceed maximum
        character.heal(50)
        assert character.current_hp == 100
    
    def test_character_get_random_move(self):
        """Test the get_random_move method."""
        moves = [
            mage_vs_orc.Move("Attack1", 10, "First attack"),
            mage_vs_orc.Move("Attack2", 15, "Second attack")
        ]
        character = mage_vs_orc.Character("Test Character", 100, moves)
        
        # Get a random move and verify it's from the move set
        random_move = character.get_random_move()
        assert random_move in moves


class TestMage:
    """Test the Mage character class."""
    
    def test_mage_creation(self):
        """Test that the Mage is created with correct stats and moves."""
        mage = mage_vs_orc.Mage()
        assert mage.name == "Mage"
        assert mage.max_hp == 100
        assert mage.current_hp == 100
        assert len(mage.move_set) == 4
        
        # Check that specific moves exist
        move_names = [move.name for move in mage.move_set]
        expected_moves = ["Fireball", "Lightning Bolt", "Heal", "Magic Missile"]
        for expected_move in expected_moves:
            assert expected_move in move_names


class TestOrcKing:
    """Test the OrcKing character class."""
    
    def test_orc_king_creation(self):
        """Test that the Orc King is created with correct stats and moves."""
        orc_king = mage_vs_orc.OrcKing()
        assert orc_king.name == "Orc King"
        assert orc_king.max_hp == 120
        assert orc_king.current_hp == 120
        assert len(orc_king.move_set) == 4
        
        # Check that specific moves exist
        move_names = [move.name for move in orc_king.move_set]
        expected_moves = ["Axe Swing", "Battle Roar", "Charge", "Slam"]
        for expected_move in expected_moves:
            assert expected_move in move_names


class TestGame:
    """Test the Game class functionality."""
    
    def test_game_creation(self):
        """Test that the game initializes with proper characters."""
        game = mage_vs_orc.Game()
        assert game.mage is not None
        assert game.orc_king is not None
        assert game.turn_count == 1
        assert isinstance(game.mage, mage_vs_orc.Mage)
        assert isinstance(game.orc_king, mage_vs_orc.OrcKing)
    
    def test_execute_move_regular_damage(self):
        """Test executing a regular damage move."""
        game = mage_vs_orc.Game()
        initial_hp = game.orc_king.current_hp
        
        # Use the Mage's Fireball move
        fireball = game.mage.move_set[0]  # Fireball is the first move
        result = game.execute_move(game.mage, game.orc_king, fireball)
        
        assert game.orc_king.current_hp == initial_hp - fireball.damage
        assert "Mage uses Fireball!" in result
        assert "Orc King takes" in result
    
    def test_execute_move_heal(self):
        """Test executing a heal move."""
        game = mage_vs_orc.Game()
        
        # Damage the mage first
        game.mage.take_damage(30)
        initial_hp = game.mage.current_hp
        
        # Find the heal move
        heal_move = None
        for move in game.mage.move_set:
            if move.special_effect == "heal_20":
                heal_move = move
                break
        
        assert heal_move is not None
        result = game.execute_move(game.mage, game.orc_king, heal_move)
        
        assert game.mage.current_hp == initial_hp + 20
        assert "Mage uses Heal!" in result
        assert "recovers 20 HP!" in result
    
    def test_check_battle_end(self):
        """Test the battle end check functionality."""
        game = mage_vs_orc.Game()
        
        # Initially, no one should have won
        result = game.check_battle_end()
        assert result is None
        
        # If mage dies, orc king should win
        game.mage.current_hp = 0
        result = game.check_battle_end()
        assert result == "defeat"
        
        # Reset and test orc king death
        game.mage.current_hp = 100
        game.orc_king.current_hp = 0
        result = game.check_battle_end()
        assert result == "victory"


if __name__ == "__main__":
    pytest.main([__file__])