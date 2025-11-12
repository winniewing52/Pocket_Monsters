from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem

class PokeTeam:
    """
    This class represents a team of Pokemon.
    """
    TEAM_LIMIT = 6
    POKE_LIST = get_all_pokemon_types()
    CRITERION_LIST = ["health", "defence", "battle_power", "speed", "level"]

    def __init__(self):
        """
        Initializes a new PokeTeam object.

        Time Complexity:
            Best Case: O(1), it only involves initializing the instance variables
            Worst Case: O(1), it only involves initializing the instance variables

        Parameters:
            team (ArrayR): an array of Pokemon objects representing the team.
            team_count (int): the number of Pokemon in the team.
            total_team (ArrayR): an array of Pokemon objects representing the original team for regenerating
            criterion (str): the criterion for optimising the team
        """
        self.team = ArrayR(self.TEAM_LIMIT)
        self.team_count = 0
        self.total_team = ArrayR(self.TEAM_LIMIT)
        self.criterion = " "

    def choose_manually(self):
        """
        Allows the user to manually choose Pokemon for their team.

        This method prompts the user to enter the names of the Pokemon they want to add to their team.
        User can enter 'exit' to finish choosing the Pokemon.

        Time Complexity:
            Best Case: O(1), occurs when user enters 'exit' immediately without choosing any Pokemon.
            Worst Case: O(n), occurs when the user chooses all the Pokemon for the team.
        
        Parameters:
            all_pokemon: A list of all available Pokemon types.
            i: A loop variable used to iterate through  the team limit.
            user_response: 
            pokemon_chosen:

        Situation Occurs:
            When user enters 'exit', the loop will terminate and the method finishes.
            When the user enters an invalid Pokemon name, the user is prompt again to enter a valid Pokemon name.
        """
        all_pokemon = get_all_pokemon_types()

        for i in range(self.TEAM_LIMIT):
            pokemon_chosen = False

            while not pokemon_chosen:
                user_response = input("Choose which Pokemon you want (or enter 'exit' to finish): ")

                if user_response.lower() == "exit":
                    break

                self.team[i] = user_response
                self.total_team[i] = self.team[i]
                self.team_count += 1
                pokemon_chosen = True
            
            if not pokemon_chosen:
                print("Invalid Pokemon name. Please enter a valid Pokemon name.")

    def choose_randomly(self) -> None:
        """
        Choose a team of Pokemon randomly.
        """
        all_pokemon = get_all_pokemon_types()
        self.team_count = 0

        for i in range(self.TEAM_LIMIT):
            rand_int = random.randint(0, len(all_pokemon)-1)
            self.team[i] = all_pokemon[rand_int]()
            self.team[i].original_hp = self.team[i].get_health()
            self.total_team[i] = self.team[i]
            self.team_count += 1

    def regenerate_team(self, battle_mode: BattleMode, criterion: str = None) -> None:
        """
        Regenerate the team based on the specified battle mode and criterion.

        Time Complexity:
            Best Case: O(n), where n is the size of the team. This occurs when the battle mode is set to BattleMode.SET or BattleMode.ROTATE, and the
                       criterion is not in self.CRITERION_LIST.
            Worst Case: O(n^2), where n is the size of the team. This occurs when the battle mode is set to BattleMode.OPTIMISE, and the criterion is
                        in criterion is in self.CRITERION_LIST.
        
        Parameters:
            battle_mode(BattleMode): The battle mode to regenerate the team.
            criterion(str): The criterion to optimize the team.
            new_pokemon_team: A new instance of a data structure to store the regenerate team.                
        """
        if battle_mode == BattleMode.SET:
            new_pokemon_team = ArrayStack(max_capacity=self.TEAM_LIMIT)

            for i in range(self.TEAM_LIMIT):
                self.total_team[i].health = self.total_team[i].original_hp
                new_pokemon_team.push(self.total_team[i])

            self.team = new_pokemon_team
        
        elif battle_mode == BattleMode.ROTATE:
            new_pokemon_team = CircularQueue(max_capacity=self.TEAM_LIMIT)

            for i in range(self.TEAM_LIMIT):
                self.total_team[i].health = self.total_team[i].original_hp
                new_pokemon_team.append(self.total_team[i])
            
            self.team = new_pokemon_team

        elif battle_mode == BattleMode.OPTIMISE:
            self.team = ArrayR(length = self.TEAM_LIMIT)

            for i in range(self.TEAM_LIMIT):
                self.total_team[i].health = self.total_team[i].original_hp
                self.team[i] = self.total_team[i]

            if criterion in self.CRITERION_LIST:
                self.assign_team(criterion)

            else:
                print("Invalid criterion. You can only select from 'health', 'defence', 'battle_power', 'speed', 'level'.")

    def assign_team(self, criterion: str = None) -> None:
        """
        Assigns a new team of Pokemon based on the given criterion,

        Time Complexity:
            Best Case: O(n log n), occurs when the criterion is not provided or is not one of the valid options.
            Worst Case: O(n log n), occurs when the criterion is provided and is one of the valid options.

        Parameters:
            new_pokemon_team (ArraySortedList): An instance of the ArraySortedList class used to store the new sorted team.
            criterion(str): The criterion to sort the Pokemon by valid options.
        """
        new_pokemon_team = ArraySortedList(self.TEAM_LIMIT)

        if criterion == "health":
            for i in range(len(self.team)):
                new_pokemon = ListItem(self[i], self[i].get_health())
                new_pokemon_team.add(new_pokemon)

        elif criterion == "defence":
            for i in range(len(self.team)):
                new_pokemon = ListItem(self[i], self[i].get_defence())
                new_pokemon_team.add(new_pokemon)

        elif criterion == "battle_power":
            for i in range(len(self.team)):
                new_pokemon = ListItem(self[i], self[i].get_battle_power())
                new_pokemon_team.add(new_pokemon)

        elif criterion == "speed":
            for i in range(len(self.team)):
                new_pokemon = ListItem(self[i], self[i].get_speed())
                new_pokemon_team.add(new_pokemon)

        elif criterion == "level":
            for i in range(len(self.team)):
                new_pokemon = ListItem(self[i], self[i].get_level())
                new_pokemon_team.add(new_pokemon)

        else:
            print("Invalid criterion. You can only select from 'health', 'defence', 'battle_power', 'speed', 'level'.")

        self.team = new_pokemon_team

    def assemble_team(self, battle_mode: BattleMode) -> None:
        """
        Assembles the team of Pokemon based on the specified the battle mode.

        Time Complexity:
            Best Case: O(n), where n is the number of Pokemon in the team. This occurs when the battle mode is set to BattleMode.SET or 
                       BattleMode.ROTATE.
            Worst Case: O(n^2), occurs when the battle mode is set to BattleMode.OPTIMISE.

        Parameters:
            battle_mode(BattleMode): The battle mode to assemble the team.
        """
        self.battle_mode = battle_mode

        if self.battle_mode == BattleMode.SET:
            new_pokemon_team = ArrayStack(max_capacity= self.TEAM_LIMIT)

            for i in range(len(self.team)):
                new_pokemon_team.push(self.team[i])

            self.team = new_pokemon_team

        elif self.battle_mode == BattleMode.ROTATE:
            new_pokemon_team = CircularQueue(max_capacity= self.TEAM_LIMIT)

            for i in range(len(self.team)):
                new_pokemon_team.append(self.team[i])
            
            self.team = new_pokemon_team

        elif self.battle_mode == BattleMode.OPTIMISE:
            self.assign_team(self.criterion)

        else:
            raise ValueError("Invalid battle mode")

    def special(self, battle_mode: BattleMode) -> None:
        """
        Performs a special operation on the PokeTeam based on the given battle mode.

        Time Complexity:
            Best Case: O(n), where n is the length of the team. This occurs when the battle mode is set to BattleMode.SET and the team length is even.
            Worst Case: O(n^2), where n is the length of the team. This occurs when the battle mode is set to BattleMode.ROTATE and the team length
                        is odd.
        
        Parameters:
            battle_mode(BattleMode): The battle mode to determine the special operation.
            total_length(int): The length of the team.
            q(CircularQueue): A circular queue used for temporary storage.
            s(ArrayStack): An array stack used for temporary storage.
            temp(CircularQueue or ArraySortedList): A temporary data structure used for sorting.

        Situation Occurs:
            SET: Rearranges the team by splitting it in half and reverse the order of the first half.
            ROTATE: Rearranges the team by rotating the elements in a circular manner.
            OPTIMISE: Sorts the team in ascending and descending order.
        """
        if battle_mode == BattleMode.SET:
            total_length = len(self.team)

            q = CircularQueue(self.TEAM_LIMIT)

            for i in range(total_length//2):
                q.append(self.team.pop())

            for i in range(total_length//2):
                self.team.push(q.serve())
        
        elif battle_mode == BattleMode.ROTATE:
            total_length = len(self.team)

            s = ArrayStack(self.TEAM_LIMIT)
            temp = CircularQueue(self.TEAM_LIMIT)

            for i in range(total_length//2):
                temp.append(self.team.serve())

            total_length = len(self.team)

            for i in range(total_length):
                s.push(self.team.serve())
            
            for i in range(total_length):
                temp.append(s.pop())
            
            self.team = temp
        
        elif battle_mode == BattleMode.OPTIMISE:
            temp =ArraySortedList(self.TEAM_LIMIT)

            for i in range(len(self.team)):
                temp.add(ListItem(self.team[i].value, -self.team[i].key))

            self.team = temp

    def __getitem__(self, index: int):
        """
        Retrives the item at the specified index in the team.

        Time Complexity:
            Best Case: O(1), occurs when the underlying data structure is an ArraySortedList.
            Worst Case: O(n), occurs when the underlying data structure is an ArrayStack or CircularQueue.

        Parameters:
            index (int): The index of the item to retrieve.

        Returns:
            The item at the specified index in the team.
        """
        if type(self.team) == ArrayStack:
            pokemon_storage = ArrayStack(max_capacity = self.TEAM_LIMIT)

            for i in range(index + 1):
                current_pokemon = self.team.pop()
                pokemon_storage.push(current_pokemon)
            
            pokemon_at_index = pokemon_storage.peek()

            for i in range(index + 1):
                current_pokemon = pokemon_storage.pop()
                self.team.push(current_pokemon)
            
            return pokemon_at_index
    
        elif type(self.team) == CircularQueue:
            pokemon_storage = ArrayR(length = self.TEAM_LIMIT)

            for i in range(len(self.team)):
                current_pokemon = self.team.serve()
                pokemon_storage[i] = current_pokemon

            pokemon_at_index = pokemon_storage[index]
            self.team = pokemon_storage
            
            self.assemble_team(BattleMode.ROTATE)

            return pokemon_at_index
        
        elif type(self.team) == ArraySortedList:
            return self.team[index].value
    
        else:
            return self.team[index]

    def __len__(self):
        """
        Returns the number of Pokemon in the team.

        Time Complexity:
            Best Case: O(1), occurs when the PokeTeam is empty.
            Worst Case: O(n), occurs when the PokeTeam has n elements.

        Returns:
            int: The number of Pokemon in the team.
        """
        return self.team_count

    def __str__(self):
        """
        Returns the string representation of the PokeTeam object.

        Time Complexity:
            Best Case: O(n), where n is the number of Pokemon in the team. This occurs when the team is empty, resulting in a single iteration over
                       an empty range.
            Worst Case: O(n), where n is the number of Pokemon in the team. This occurs when the team has at least one Pokemon, resulting in an
                        iteration over the range of team_count

        Returns:
            str: PokeTeam object with each Pokemon.
        """
        return '\n'.join(str(self[i]) for i in range(self.team_count))
                         
    def is_empty(self):
        """
        Checks if the team is empty.

        Time Complexity:
            Best Case: O(1)
            Worst Case: O(1)

        Returns:
            bool: True if the team is empty, False otherwise.
        """
        return self.team_count == 0

    def push(self, pokemon, criterion = " ", isNegative = 1):
        """
        Time Complexity:
            Best Case: O(1), occurs when the battle mode is set to BattleMode.SET or BattleMode.ROTATE, as the Pokemon is simply added to the team
                       without any additional operations.
            Worst Case: O(1), occurs when the battle mode is set to BattleMode.OPTIMISE, and the criterion is one of the valid options.

        Args:
            pokemon(Pokemon): The Pokemon object to be added to the team.
            criterion: The criterion to determine the order of the Pokemon in the team.
            isNegative: A multiplier to determine the order of the Pokemon in the team.
        """
        if self.battle_mode == BattleMode.SET:
           self.team.push(pokemon)
        
        elif self.battle_mode == BattleMode.ROTATE:
           self.team.append(pokemon)

        elif self.battle_mode == BattleMode.OPTIMISE:
            if criterion == "health":
                pokemon = ListItem(pokemon, isNegative * pokemon.get_health())
            
            elif criterion == "defence":
                pokemon = ListItem(pokemon, isNegative * pokemon.get_defence())
            
            elif criterion == "battle_power":
                pokemon = ListItem(pokemon, isNegative * pokemon.get_battle_power())
            
            elif criterion == "speed":
                pokemon = ListItem(pokemon, isNegative * pokemon.get_speed())

            elif criterion == "level":
                pokemon = ListItem(pokemon, isNegative * pokemon.get_level())

            self.team.add(pokemon)

class Trainer:

    def __init__(self, name) -> None:
        """
        Initializes a new instance of the PokeTeam class.

        Time Complexity:
            Best Case: O(1)
            Worst Case: O(1)

        Parameters:
            name(str): The name of the PokeTeam.
            poketeam (PokeTeam): An instance of the PokeTeam class.
            pokedex (BSet): An instance of the BSetb class.
        """
        self.name = name
        self.poketeam = PokeTeam()
        self.pokedex = BSet()

    def pick_team(self, method: str) -> None:
        """
        Picks a team of Pokemon based on the specified method.

        Time Complexity:
            Best Case: O(n), where n is the number of Pokemon in the team. This occurs when the method is 'Random' and the team is already chosen
                       randomly. 
            Worst Case: O(n^2), where n is the number of Pokemon in the team. This occurs when then method is 'Manual' and the team is chosen
                        manually. 
        
        Parameters:
            method (str): The method is used to pick the team. The valid options are 'Random' and 'Manual'.
            i (int): Loop the variable used to iterate over the team
        """
        if method == 'Random':
            self.poketeam.choose_randomly()
        
        elif method == 'Manual':
            self.poketeam.choose_manually()

        else:
            raise ValueError("Invalid method. Please select either Random or Manual")
        
        for i in range(len(self.poketeam)):
            self.register_pokemon(self.poketeam[i])
            self.poketeam[i].original_hp = self.poketeam[i].get_health()

    def get_team(self) -> PokeTeam:
        """
        Returns the PokeTeam object.

        Time Complexity:
            Best Case: O(1)
            Worst Case: O(1)

        Returns:
            PokeTeam: The PokeTeam object.
        """
        return self.poketeam

    def get_name(self) -> str:
        """
        Returns the name of the object

        Time Complexity:
            Best Case: O(1), occurs when
            Worst Case: O(1), occurs when

        Returns:
            str: The name of the object.
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Register a Pokemon  to the Pokedex

        Time Complexity:
            Best Case: O(1), occurs when the Pokedex is empty, and the Pokemon is added directly to the Pokedex without any additional operations.
            Worst Case: O(n), where n is the number of Pokemon in the Pokedex.

        Parameters:
            pokemon (Pokemon): The Pokemon object is registered.
        """
        self.pokedex.add(pokemon.poketype.value + 1)

    def get_pokedex_completion(self) -> float:
        """
        Calculates the completion percentage of the Pokedex.

        Time Complexity:
            Best Case: O(1), occurs when the Pokedex is empty.
            Worst Case: O(n), occurs when the Pokedex is fully populated with Pokemon

        Returns:
            float: The completion percentage of the Pokedex, rounded to 2 decimal places. 
        """
        total_pokemon_type = len(PokeType)
        return round(len(self.pokedex) / total_pokemon_type, 2)

    def __str__(self) -> str:
        """
        Returns a string representation of the Trainer object.

        Time Complexity:
            Best Case: O(1), occurs when the Trainer object has no attributes to access or calculate.
            Worst Case: O(n), occurs when the Trainer object has to access or calculate multiple attributes.
            
        Returns:
            str: The trainer's name and the pokedex completion percentage.    
        """
        completion = self.get_pokedex_completion()
        return f"Trainer {self.name} Pokedex Completion: {int(completion * 100)}%"

if __name__ == '__main__':
    t = Trainer('Ash')
    print(t)
    t.pick_team("Random")
    print(t)
    print(t.get_team())
