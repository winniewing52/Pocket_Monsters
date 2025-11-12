from poke_team import Trainer, PokeTeam
from battle import Battle
from battle_mode import BattleMode
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple
import random

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3

    def __init__(self) -> None:
        """
        Initializes a new instance of the Tower class.
        """
        self.my_trainer = None
        self.enemy_trainers = None
        self.enemy_lives = None
        self.lives_taken = 0

    def set_my_trainer(self, trainer: Trainer) -> None:
        """
        Sets the trainer for the tower.

        Time Complexity:
            Best Case: O(1), occurs when the trainer object is already set and there are no additional operations required.
            Worst Case: O(1), occurs when the trainer object is already set and there are no additional operations required.

        Parameters:
            self.my_trainer: The trainer object to be set.
            self.my_trainer_lives: The number of lives assigned to the player's trainer.

        Args:
            trainer(Trainer): The trainer object to be set.
        """
        self.my_trainer = trainer
        self.my_trainer_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_enemy_trainers(self, num_teams: int) -> None:
        """
        Generate enemy trainers and initialize their teams and lives.

        Time Complexity Analysis:
            Best Case: O(num_teams), occurs when the number of enemy teams to generate is small. This method only 
                       needs to iterate through the range of num_teams once to create the trainers, and the time 
                       complexity is linear with respect to the number of teams.

            Worst Case: O(num_teams), occurs when the number of enemy teams to generate is large. This method needs to 
                        iterate through the range of num_teams to create the trainers, and the time complexity is 
                        linear with respect to the number of teams.

        Parameters:
            self.enemy_trainers: A circular queue of enemy trainers.
            self.enemy_lives: A circular queue of enemy lives.

        Args:
            num_teams (int): The number of enemy teams to generate.
        """
        self.enemy_trainers = CircularQueue(num_teams)
        self.enemy_lives = CircularQueue(num_teams)

        for _ in range(num_teams):
            trainer = Trainer("Enemy")
            trainer.pick_team("Random")
            trainer.get_team().assemble_team(BattleMode.ROTATE)
            self.enemy_trainers.append(trainer)
            self.enemy_lives.append(random.randint(self.MIN_LIVES, self.MAX_LIVES))

    def battles_remaining(self) -> bool:
        """
        Check if there are battles remaining in tower.

        Time Complexity Analysis:
            Best Case: O(1), occurs when both conditions are false, which means there are no battles remaining. This method simply returns False 
                       without any additional operations.

            Worst Case: O(1), occurs when at least one of the conditions is true, indicating that there are battles remaining. The method checks the 
                        values of self.my_trainer_lives and self.enemy_trainers and returns True if the conditions are met.

        Parameters:
            self.my_trainer_lives: The number of lives of the trainer.
            self.enemy_trainers: A circular queue of enemy trainers.

        Returns:
            bool: True if there are more battles to be had, False otherwise.
        """
        return self.my_trainer_lives > 0 and not self.enemy_trainers.is_empty() 

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Initiates the next battle between the player's trainer and enemy trainer.

        Time Complexity:
            Best Case: O(1), this occurs when there are no Pokemon in the player's and enemy's teams.
            Worst Case: O(n), where n is the number of Pokemon in the player's and enemy's teams.

        Parameters:
            enemy_trainer: 
            enemy_lives: The remaining lives of the enemy trainer obtained from the enemy_lives queue.
            battle: The battle object used to initiate the battle.
            battle_result: The result of the battle.
        """
        enemy_trainer = self.enemy_trainers.serve()
        enemy_lives = self.enemy_lives.serve()

        self.my_trainer.get_team().regenerate_team(BattleMode.ROTATE)
        enemy_trainer.get_team().regenerate_team(BattleMode.ROTATE)

        battle = Battle(self.my_trainer, enemy_trainer, BattleMode.ROTATE)
        battle_result = battle.commence_battle()

        if battle_result == self.my_trainer:
            enemy_lives -= 1
            self.lives_taken += 1

        elif battle_result == enemy_trainer:
            self.my_trainer_lives -= 1

        else:
            self.my_trainer_lives -= 1
            enemy_lives -= 1

        if enemy_lives > 0:
            self.enemy_trainers.append(enemy_trainer)
            self.enemy_lives.append(enemy_lives)

        return battle_result, self.my_trainer, enemy_trainer, self.my_trainer_lives, enemy_lives

    def enemies_defeated(self) -> int:
        """
        Returns the number of enemies defeated by tower.

        Time Complexity:
            Best Case: O(1), occurs when the number of enemies defeated is accessed directly from the lives_taken attribute.
            Worst Case: O(1), occurs when the number of enemies defeated is accessed directly from the lives_taken attribute.

        Parameters:
            self.lives_taken(int): The number of lives taken by the tower

        Returns:
            int: The number of enemies defeated
        """
        return self.lives_taken
