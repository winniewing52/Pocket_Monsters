from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from pokemon import Pokemon
import math
import random
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        """
        Initialized a battle object

        Time Complexity:
            Best Case: O(1), it only involves initializing the instance variables
            Worst Case: O(1), it only involves initializing the instance variables

        Parameters:
            self.trainer_1 = The first trainer in this battle.
            self.trainer_2 =  The second trainer in this battle.
            self.battle_mode = The battle mode to be used in this battle.
            self.criterion = The criterion used to determine the winner of the battle.

        Situation Occurs:
            Init method is called when creating a new Battle object
            It initializes the object with the provided trainers, battle mode and criterion.
        """
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def commence_battle(self) -> Trainer | None:
        """
        Commences the battle based on the selected battle mode.

        Time Complexity:
            Best Case: O(1), occurs when the battle mode is already set and the winner is determined in 
                       constant time.
            Worst Case: O(n), occurs when the battle mode is OPTIMISE and the optimise_battle method is called.

        Parameters:
            winner_team: Stores the winning trainer if there is a winner, otherwise None.

        Situations:
            If the battle mode is SET, the set_battle method is called to determine the winner.
            If the battle mode is ROTATE, the rotate_battle method is called to determine the winner.
            If the battle mode is OPTIMISE, the optimise_battle method is called with the specified criterion 
            to determine the winner.
            If the battle mode is not one of the predefined modes, an exception is raised.
        """
        winner_team = None

        if self.battle_mode == BattleMode.SET:
            winner_team = self.set_battle()
            
        elif self.battle_mode == BattleMode.ROTATE:
            winner_team = self.rotate_battle()

        elif self.battle_mode == BattleMode.OPTIMISE:
            winner_team = self.optimise_battle(self.criterion)
            
        else:
            raise Exception("Invalid battle mode. Please select a valid battle mode.")
            
        if winner_team == self.trainer_1:
            return self.trainer_1
        
        elif winner_team == self.trainer_2:
            return self.trainer_2
        
        else:
            return None

    def _create_teams(self) -> None:
        """
        Assembles teams for the battle.

        This method sets the criterion for both trainers' teams, picks a random team for each trainer,
        and assembles the teams based on the battle mode.

        Time Complexity:
            Best Case: O(1), occurs when the method is called and the trainers and criterion are already set, 
                        resulting in constant time operations.
            Worst Case: O(n), occurs when the method needs to pick a random team and assemble it, which involves 
                        iterating over the available Pokemon and performing operations based on the battle mode.

        Parameters:
            self.trainer_1: The first trainer object.
            self.trainer_2: The second trainer object.
            self.criterion: The criterion used for team selection.
            self.battle_mode: The battle mode used for team assembly.
        """
        self.trainer_1.get_team().criterion = self.criterion
        self.trainer_1.pick_team("Random")
        self.trainer_1.get_team().assemble_team(self.battle_mode)

        self.trainer_2.get_team().criterion = self.criterion
        self.trainer_2.pick_team("Random")
        self.trainer_2.get_team().assemble_team(self.battle_mode)

    # Note: These are here for your convenience
    # If you prefer you can ignore them
    def set_battle(self) -> PokeTeam | None:
        """
        Sets up and executes a battle between two trainers' teams.

        Time Complexity:
            Best Case: O(1), occurs when both teams are empty initially, the method returns None immediately.
            Worst Case: O(n), where n is the maximum number of Pokémon in either team. This occurs when the method 
                        iterates through all the Pokémon in both teams.

        Parameters:
            team_1: The team of the first trainer.
            team_2: The team of the second trainer.
            Pokemon_1: The Pokémon selected from team_1.
            Pokemon_2: The Pokémon selected from team_2.

        Situations:
            If both teams are empty initially, the method returns None.
            If team_1 is empty, the method returns the trainer_2.
            If team_2 is empty, the method returns the trainer_1.
        """
        team_1 = self.trainer_1.get_team().team
        team_2 = self.trainer_2.get_team().team

        while not team_1.is_empty() and not team_2.is_empty():
            Pokemon_1 = team_1.pop()
            Pokemon_2 = team_2.pop()

            self.trainer_1.register_pokemon(Pokemon_2)
            self.trainer_2.register_pokemon(Pokemon_1)

            self.battle(Pokemon_1, Pokemon_2)

            if Pokemon_1.is_alive():
                team_1.push(Pokemon_1)

            if Pokemon_2.is_alive():
                team_2.push(Pokemon_2)

            if not Pokemon_1.is_alive():
                self.trainer_1.get_team().team_count -= 1

            if not Pokemon_2.is_alive():
                self.trainer_2.get_team().team_count -= 1

        if team_1.is_empty() and team_2.is_empty():
            return None
        
        elif team_1.is_empty():
            return self.trainer_2
        
        else:
            return self.trainer_1
        
    def rotate_battle(self) -> PokeTeam | None:
        """
        Simulates a rotation battle between two trainers' teams of Pokemon.

        Time Complexity:
            Best Case: O(1),
            Worst Case: O(n), where n is the maximum number of Pokemon in either team.

        Parameters:
            team_1: The team of the Pokemon belonging to the trainer_1.
            team_2: The team of the Pokemon belonging to the trainer_2.

        Situation Occurs:
            If both of the teams are empty, the method returns None.
            If team_1 is empty, the method returns trainer_2.
            If team_2 is empty, the method returns trainer_1.
            If Pokemon_1 is alive, it goes back to team_1.
            If Pokemon_2 is alive, it goes back to team_2.
            If Pokemon_1 is not alive, the team_count of trainer_1 is decreased.
            If Pokemon_2 is not alive, the team_count of trainer_2 is decreased.
        """
        team_1 = self.trainer_1.get_team().team
        team_2 = self.trainer_2.get_team().team    

        while not team_1.is_empty() and not team_2.is_empty():
            Pokemon_1 = team_1.serve()
            Pokemon_2 = team_2.serve()

            self.trainer_1.register_pokemon(Pokemon_2)
            self.trainer_2.register_pokemon(Pokemon_1)

            self.battle(Pokemon_1, Pokemon_2)

            if Pokemon_1.is_alive():
                team_1.append(Pokemon_1)

            if Pokemon_2.is_alive():
                team_2.append(Pokemon_2)

            if not Pokemon_1.is_alive():
                self.trainer_1.get_team().team_count -= 1

            if not Pokemon_2.is_alive():
                self.trainer_2.get_team().team_count -= 1

        if team_1.is_empty() and team_2.is_empty():
            return None
        
        elif team_1.is_empty():
            return self.trainer_2
        
        else:
            return self.trainer_1    

    def optimise_battle(self, attribute: str) -> PokeTeam | None:
        """
        Optimizes the battle between two trainers' teams based on the given attribute.

        Time Complexity:
            Best Case: O(1), occurs when both teams are empty, the method returns none immediately.
            Worst Case: O(n), where n is the number of Pokémon in the teams, occurs when the method iterates through 
                        all the Pokémon in both teams.

        Args:
            attribute (str): The attribute to optimize the battle, e.g., "attack", "defense", "speed".

        Parameters:
            team_1 (PokeTeam): The team of the first trainer.
            team_2 (PokeTeam): The team of the second trainer.
            Pokemon_1 (PokeNode): The Pokémon from team_1 being battled.
            Pokemon_2 (PokeNode): The Pokémon from team_2 being battled.

        Situation Occurs:
            If both teams are empty, the method returns None.
            If team_1 is empty, the method returns the team of trainer_2.
            If team_2 is empty, the method returns the team of trainer_1.
        """
        team_1 = self.trainer_1.get_team()
        team_2 = self.trainer_2.get_team()

        while team_1.team_count > 0 and team_2.team_count > 0:
            Pokemon_1 = team_1.team.delete_at_index(0)
            Pokemon_2 = team_2.team.delete_at_index(0)

            self.trainer_1.register_pokemon(Pokemon_2.value)
            self.trainer_2.register_pokemon(Pokemon_1.value)

            self.battle(Pokemon_1.value, Pokemon_2.value)

            if Pokemon_1.value.is_alive():
                if Pokemon_1.key < 0:
                    team_1.push(Pokemon_1.value, self.criterion, - 1)

                else:
                    team_1.push(Pokemon_1.value, self.criterion)

            if Pokemon_2.value.is_alive():
                if Pokemon_2.key < 0:
                    team_2.push(Pokemon_2.value, self.criterion, - 1)

                else:
                    team_2.push(Pokemon_2.value, self.criterion)

            if not Pokemon_1.value.is_alive():
                self.trainer_1.get_team().team_count -= 1

            if not Pokemon_2.value.is_alive():
                self.trainer_2.get_team().team_count -= 1

        if team_1.is_empty() and team_2.is_empty():
            return None
        
        elif team_1.is_empty():
            return self.trainer_2
        
        else:
            return self.trainer_1 
    
    def battle(self, Pokemon_1: Pokemon, Pokemon_2: Pokemon):
        """
        Simulates a battle between two Pokemon.

        Time Complexity:
            Best Case: O(1), occurs when the speed of both Pokemon is equal, as it skips the speed comparison 
                       and directly attacks each other once.
            Worst Case: O(1), occurs when the speed of both Pokemon is different, as it performs two rounds of 
                        attacks and defenses.

        Args:
            Pokemon_1 (Pokemon): The first Pokemon.
            Pokemon_2 (Pokemon): The second Pokemon.

        Parameters:
            Pokemon_1_speed (int): The speed of Pokemon_1.
            Pokemon_2_speed (int): The speed of Pokemon_2.
            attack_point (float): The attack power of the attacking Pokemon.
            effective_damage (int): The effective damage caused by the attack.
            effective_damage_Pokemon_1 (int): The effective damage caused by Pokemon_1's attack.
            effective_damage_Pokemon_2 (int): The effective damage caused by Pokemon_2's attack.

        Situations:
            If Pokemon_1's speed is greater than Pokemon_2's speed, Pokemon_1 attacks Pokemon_2 first.
            If Pokemon_2's speed is greater than Pokemon_1's speed, Pokemon_2 attacks Pokemon_1 first.
            If both Pokemon have the same speed, they attack each other simultaneously.
            After each attack, the effective damage is calculated based on the attacker's Pokedex completion.
            The defending Pokemon's health is reduced by the effective damage.
            If a Pokemon's health reaches 0, the other Pokemon levels up.
            If both Pokemon's health is greater than 0, their health is reduced by 1.
            If a Pokemon's health reaches 0 after the health reduction, the other Pokemon levels up.
        """
        Pokemon_1_speed = Pokemon_1.get_speed()
        Pokemon_2_speed = Pokemon_2.get_speed()

        if Pokemon_1_speed > Pokemon_2_speed:
            attack_point = Pokemon_1.attack(Pokemon_2)
            effective_damage = math.ceil(attack_point * self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion())
            Pokemon_2.defend(effective_damage)

            if Pokemon_2.is_alive():
                attack_point = Pokemon_2.attack(Pokemon_1)
                effective_damage = math.ceil(attack_point * self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion())
                Pokemon_1.defend(effective_damage)

        elif Pokemon_1_speed < Pokemon_2_speed:
            attack_point = Pokemon_2.attack(Pokemon_1)
            effective_damage = math.ceil(attack_point * self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion())
            Pokemon_1.defend(effective_damage)

            if Pokemon_1.is_alive():
                attack_point = Pokemon_1.attack(Pokemon_2)
                effective_damage = math.ceil(attack_point * self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion())
                Pokemon_2.defend(effective_damage)

        else:
            attack_point = Pokemon_1.attack(Pokemon_2)
            attack_point = Pokemon_2.attack(Pokemon_1)

            effective_damage_Pokemon_1 = math.ceil(attack_point * self.trainer_1.get_pokedex_completion() / self.trainer_2.get_pokedex_completion())
            effective_damage_Pokemon_2 = math.ceil(attack_point * self.trainer_2.get_pokedex_completion() / self.trainer_1.get_pokedex_completion())

            Pokemon_2.defend(effective_damage_Pokemon_1)
            Pokemon_1.defend(effective_damage_Pokemon_2)

        if Pokemon_1.is_alive() and not Pokemon_2.is_alive():
            Pokemon_1.level_up()
        
        elif Pokemon_2.is_alive() and not Pokemon_1.is_alive():
            Pokemon_2.level_up()
        
        else:
            Pokemon_1.health -= 1
            Pokemon_2.health -= 1

            if not Pokemon_1.is_alive():
                Pokemon_2.level_up()
            
            elif not Pokemon_2.is_alive():
                Pokemon_1.level_up()

if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
