import os
import pygame
import numpy as np


class RobotouilleCanvas:
    """
    This class is responsible for drawing the game state on a pygame surface. Some of
    the rendered information isn't necessarily provided by the game state (e.g. the
    location of the stations) so it is necessary to provide a layout upon initialization.
    """

    # The directory containing the assets
    ASSETS_DIRECTORY = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets"
    )

    # The offset to draw food and stations relative to the center of the grid square
    STATION_FOOD_OFFSET = 0.25

    def __init__(self, layout, players, window_size=np.array([512, 512])):
        """
        Initializes the canvas.

        Args:
            layout (List[List[Optional[str]]]): 2D array of station names (or None)
            window_size (np.array): (width, height) of the window
        """
        print("Initializing RobotouilleCanvas...")
        # The layout of the game
        self.layout = layout
        print(f"layout: {self.layout}")
        # The player's position and direction
        players_pos = [
            (players[i]["x"], len(layout) - players[i]["y"] - 1)
            for i in range(len(players))
        ]
        print(f"players_pos: {players_pos}")

        self.players_pose = [
            {
                "name": players[i]["name"],
                "position": players_pos[i],
                "direction": tuple(players[i]["direction"]),
            }
            for i in range(len(players_pos))
        ]
        print(f"players_pose: {self.players_pose}")

        grid_dimensions = np.array([len(layout[0]), len(layout)])
        print(f"grid_dimensions: {grid_dimensions}")
        # The scaling factor for a grid square
        self.pix_square_size = window_size / grid_dimensions
        print(f"pix_square_size: {self.pix_square_size}")
        # A dictionary which maps image names to loaded images
        self.asset_directory = {}
        print(f"asset_directory: {self.asset_directory}")

    def _get_station_position(self, station_name):
        """
        Gets the position of a station.

        Args:
            station_name (str): Name of the station

        Returns:
            position (np.array): (x, y) position of the station
        """
        print(f"Getting position for station: {station_name}")
        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                if col == station_name:
                    position = np.array([j, i], dtype=float)
                    print(f"Found position: {position}")
                    return position

    def _draw_image(self, surface, image_name, position, scale):
        """
        Draws an image on the canvas.

        Args:
            surface (pygame.Surface): Surface to draw on
            image_name (str): Name of the image
            position (np.array): (x, y) position of the image
            scale (np.array): (width, height) to scale the image by
        """
        print(f"Drawing image: {image_name} at position: {position} with scale: {scale}")
        if image_name not in self.asset_directory:
            self.asset_directory[image_name] = pygame.image.load(
                os.path.join(RobotouilleCanvas.ASSETS_DIRECTORY, image_name)
            )
        image = self.asset_directory[image_name]
        image = pygame.transform.smoothscale(image, scale)
        surface.blit(image, position)
    def _draw_food_image(self, surface, food_name, obs, position):
        """
        Helper to draw a food image on the canvas.

        Args:
            surface (pygame.Surface): Surface to draw on
            food_name (str): Name of the food
            obs (List[Literal]): Game state predicates
            position (np.array): (x, y) position of the food (with pix_square_size factor accounted for)
        """
        print(f"Drawing food image: {food_name} at position: {position}")
        food_image_name = food_name
        # Check if cut or cooked or fried
        for literal in obs:
            if literal.predicate == "iscut" and literal.variables[0] == food_image_name:
                food_image_name = "cut" + food_image_name
            if (
                literal.predicate == "iscooked"
                and literal.variables[0] == food_image_name
            ):
                food_image_name = "cooked" + food_image_name
            if literal.predicate == "isfried":
                if literal.variables[0] == food_image_name:
                    food_image_name = "fried" + food_image_name
                elif literal.variables[0] == food_image_name[3:]:
                    food_image_name = "fried" + food_image_name[3:]
            if literal.predicate == "ischestcompressed":
                print(f"Found chestcompressed: {literal.variables[0]}")
                if literal.variables[0] == food_image_name:
                    food_image_name = "chestcompressed" + food_image_name
                elif literal.variables[0] == food_image_name[3:]:
                    food_image_name = "chestcompressed" + food_image_name[3:]
            if literal.predicate == "isrescuebreathed":
                if literal.variables[0] == food_image_name:
                    print(f"Found rescuebreathed: {literal.variables[0]}")
                    food_image_name = "rescuebreathed" + food_image_name
                elif literal.variables[0] == food_image_name[3:]:
                    food_image_name = "rescuebreathed" + food_image_name[3:]
        # Remove and store ID
        food_id = ""
        while food_image_name[-1].isdigit():
            food_id += food_image_name[-1]
            food_image_name = food_image_name[:-1]
        print(f"Final food image name: {food_image_name}")

        # Special case for patient
        if food_image_name == "patient":
            self._draw_image(
                surface,
                f"{food_image_name}.png",
                position,
                self.pix_square_size
            )
        else:
            self._draw_image(
                surface,
                f"{food_image_name}.png",
                position + self.pix_square_size * 0.125,
                self.pix_square_size * 0.75,
            )

    def _draw_floor(self, surface):
        """
        Draw the floor on the canvas.

        Note the game state is not necessary to draw the floor as this rendering information
        is provided by the layout.

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        print("Drawing floor...")
        clamped_pix_square_size = np.ceil(self.pix_square_size)  # Necessary to avoid 1 pixel gaps from decimals
        for row in range(len(self.layout)):
            for col in range(len(self.layout[0])):
                self._draw_image(
                    surface,
                    "floorhospital.png",
                    np.array([col, row]) * clamped_pix_square_size,
                    clamped_pix_square_size,
                )

    def _draw_stations(self, surface):
        """
        Draws the stations on the canvas.

        Note the game state is not necessary to draw the floor as this rendering information
        is provided by the layout.

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        print("Drawing stations...")
        for i, row in enumerate(self.layout):
            for j, col in enumerate(row):
                if col is not None:
                    while col[-1].isdigit():
                        col = col[:-1]
                    self._draw_image(
                        surface,
                        f"{col}.png",
                        np.array([j, i]) * self.pix_square_size,
                        self.pix_square_size,
                    )

    def _get_player_index(self, literal):
        player_index = int(literal.variables[0].name[5:]) - 1
        print(f"Player index: {player_index}")
        return player_index

    def _get_station_locations(self, layout):
        """
        Gets the locations of all stations in the layout.

        Args:
            layout (List[List[Optional[str]]]): 2D array of station names (or None)

        Returns:
            station_locations (List[tuple]): List of (x, y) positions of stations
        """
        station_locations = []
        for i, row in enumerate(layout):
            for j, col in enumerate(row):
                if col is not None:
                    station_locations.append((j, i))
        print(f"Station locations: {station_locations}")
        return station_locations

    def _get_player_positions(self, player_index):
        player_positions = []
        for i in range(len(self.players_pose)):
            if i != player_index:
                player_positions.append(self.players_pose[i]["position"])
        print(f"Player positions excluding player {player_index}: {player_positions}")
        return player_positions

    def _move_player_to_station(
        self, player_index, player_position, station_position, layout, test=False
    ):
        """
        Moves the player from their current position to a position adjacent to a station using BFS.

        BFS is used to determine the final state. As an additional constraint, the player cannot
        move through a station or out of bounds.

        Args:
            player_position (tuple): (x, y) position of the player
            station_position (tuple): (x, y) position of the station
            layout (List[List[Optional[str]]]): 2D array of station names (or None)

        Returns:
            new_player_position (tuple): (x, y) position of the player after moving
            new_player_direction (tuple): unit vector of the player's direction after moving

        Raises:
            ValueError: If the player cannot reach the station
        """
        print(f"Moving player {player_index} from {player_position} to {station_position}")
        width, height = len(layout[0]), len(layout)
        print(f"Layout dimensions: width={width}, height={height}")
        obstacle_locations = self._get_station_locations(layout)
        player_positions = self._get_player_positions(player_index)
        curr_prev = (player_position, player_position)  # current position, previous position
        queue = [curr_prev]
        visited = set()

        while queue:
            curr_prev = queue.pop(0)
            curr_position = curr_prev[0]
            prev_position = curr_prev[1]
            if curr_position == station_position:
                # Reached target station
                new_position = prev_position, (curr_position[0] - prev_position[0], prev_position[1] - curr_position[1])
                print(f"New position: {new_position}")
                return new_position
            if (
                curr_position[0] < 0
                or curr_position[0] >= width
                or curr_position[1] < 0
                or curr_position[1] >= height
            ):
                # Out of bounds
                continue

            if (curr_position in obstacle_locations) or (curr_position in player_positions):
                # Cannot move through station
                continue
            if curr_position in visited:
                # Already visited
                continue
            visited.add(curr_position)
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_position = (curr_position[0] + direction[0], curr_position[1] + direction[1])
                if next_position != prev_position:
                    queue.append((next_position, curr_position))

        assert False, "Player could not be moved to station"

    def _check_selected(self, obs, player_index):
        for literal in obs:
            if literal.predicate == "selected":
                selected_player_index = self._get_player_index(literal)
                print(f"Player {player_index} selected: {selected_player_index == player_index}")
                return selected_player_index == player_index
        return False

    def _get_player_image_name(self, direction, selected):
        """
        Returns the image name of the player given their direction.

        Args:
            direction (tuple): Unit vector of the player's direction

        Returns:
            image_name (str): Image name of the player

        Raises:
            AssertionError: If the direction is invalid
        """

        selected_string = "_selected" if selected else ""

        if direction == (0, 1):
            return "robot_back" + selected_string + ".png"
        elif direction == (0, -1):
            return "robot_front" + selected_string + ".png"
        elif direction == (1, 0):
            return "robot_right" + selected_string + ".png"
        elif direction == (-1, 0):
            return "robot_left" + selected_string + ".png"
        print(f"Invalid direction: {direction}")
        assert False, "Invalid player direction"

    def test_new_positions(self, obs):
        for literal in obs.literals:
            if literal.predicate == "loc":
                player_station = literal.variables[1].name
                station_pos = self._get_station_position(player_station)
                player_index = self._get_player_index(literal)
                player_pos = self.players_pose[player_index]["position"]
                player_pos, player_direction = self._move_player_to_station(
                    player_index, player_pos, tuple(station_pos), self.layout, test=True
                )
                print(f"Tested new position for player {player_index}: {player_pos}, direction: {player_direction}")

    def _draw_player(self, surface, obs):
        """
        Draws the player on the canvas with detailed debugging.
        """
        print("\n--- Start of _draw_player ---")
        for literal in obs:
            if literal.predicate.name == "loc":
                player_station = literal.variables[1].name
                station_pos = self._get_station_position(player_station)
                player_index = self._get_player_index(literal)
                initial_pos = self.players_pose[player_index]["position"]
                
                print(f"Player {player_index}:")
                print(f"  Initial position: {initial_pos}")
                print(f"  Station: {player_station}")
                print(f"  Station position: {station_pos}")
                
                player_pos, player_direction = self._move_player_to_station(
                    player_index, initial_pos, tuple(station_pos), self.layout
                )
                
                print(f"  After move_player_to_station: {player_pos}")
                
                # Check if the player is on a CPR stool
                if player_station == "cpr_stool":
                    # The value 0.2 represents 20% of a grid cell's height
                    # This moves the player up by 20% of a cell, making them appear on top of the obje
                    # Adjust the vertical position upwards
                    player_pos = (player_pos[0], player_pos[1] - 0.2)  # Increased offset
                    print(f"  On CPR stool, adjusted position: {player_pos}")
                
                self.players_pose[player_index]["position"] = player_pos
                self.players_pose[player_index]["direction"] = player_direction
                selected = self._check_selected(obs, player_index)
                robot_image_name = self._get_player_image_name(player_direction, selected)
                
                # Calculate the drawing position in pixels
                # player_pos[0] * self.pix_square_size[0]: Convert x-coordinate from grid to pixels
                # (player_pos[1] - 0.2) * self.pix_square_size[1]: Convert y-coordinate from grid to pixels,
                # subtracting 0.2 (20% of a cell) to move the player up slightly
                # This ensures the player is drawn above the object they're standing on
                draw_pos = (player_pos[0] * self.pix_square_size[0], 
                            (player_pos[1]- 0.2) * self.pix_square_size[1])
                
                print(f"  Final draw position (pixels): {draw_pos}")
                print(f"  Image: {robot_image_name}")
                
                self._draw_image(
                    surface,
                    robot_image_name,
                    draw_pos,
                    self.pix_square_size,
                )
        
        print("--- End of _draw_player ---\n")
    def _draw_food(self, surface, obs):
        """
        This helper draws food on the canvas.

        Since food can be stacked, the stack information must first be determined with the on and atop predicates.
        Any food with an on predicate is the bottom of a stack and is drawn first. The foods with atop predicates
        are then drawn in the correct order afterward.

        Args:
            surface (pygame.Surface): Surface to draw on
            obs (List[Literal]): Game state predicates
        """
        stack_list = []  # In the form (x, y) such that x is stacked on y
        stack_number = {}  # Stores the food item and current stack number
        for literal in obs:
            if literal.predicate == "on":
                food = literal.variables[0].name
                stack_number[food] = 1
                food_station = literal.variables[1].name
                pos = self._get_station_position(food_station)
                if "patient" not in food:
                    pos[1] -= RobotouilleCanvas.STATION_FOOD_OFFSET  # place the food slightly above the station
                print(f"Drawing food: {food} at {pos}")
                self._draw_food_image(surface, food, obs, pos * self.pix_square_size)
            if literal.predicate == "atop":
                stack = (literal.variables[0].name, literal.variables[1].name)
                stack_list.append(stack)

        # Add stacked items
        while len(stack_list) > 0:
            i = 0
            while i < len(stack_list):
                food_above, food_below = stack_list[i]
                if food_below in stack_number:
                    stack_list.remove(stack_list[i])
                    stack_number[food_above] = stack_number[food_below] + 1
                    # Get location of station
                    for literal in obs:
                        if (
                            literal.predicate == "at"
                            and literal.variables[0].name == food_below
                        ):
                            station_pos = self._get_station_position(
                                literal.variables[1].name
                            )
                            break
                    cheese_offset = (
                        -0.05 if "cheese" in food_above or "onion" in food_above else 0
                    )
                    station_pos[1] -= (
                        self.STATION_FOOD_OFFSET
                        + 0.1 * (stack_number[food_above] - 1)
                        + cheese_offset
                    )
                    print(f"Drawing stacked food: {food_above} at {station_pos}")
                    self._draw_food_image(
                        surface, food_above, obs, station_pos * self.pix_square_size
                    )
                else:
                    i += 1

    def _debug_print_layout(self):
        print("\n--- Layout Debug ---")
        for y in range(len(self.layout)):
            row = []
            for x in range(len(self.layout[0])):
                cell = self.layout[y][x]
                if cell is None:
                    row.append(".")
                else:
                    row.append(cell[:2])  # First two characters of station name
            print(" ".join(row))
        
        print("\nPlayer Positions:")
        for i, player in enumerate(self.players_pose):
            print(f"Player {i}: {player['position']}")
        print("--- End Layout Debug ---\n")

    def draw_to_surface(self, surface, obs):
        """
        Draws the game state to the surface.

        Args:
            surface (pygame.Surface): Surface to draw on
            obs (List[Literal]): Game state predicates
        """
        print("Drawing to surface...")
        self._debug_print_layout()
        self._draw_floor(surface)
        self._draw_stations(surface)
        self._draw_player(surface, obs)
        self._draw_food(surface, obs)



    # def _draw_medical_equipment(self, surface, obs):
    #     """
    #     Draws the medical equipment on the canvas.

    #     Args:
    #         surface (pygame.Surface): Surface to draw on
    #         obs (List[Literal]): Game state predicates
    #     """
    #     # for literal in obs:
    #     #     print("literal",literal)
    #     #     breakpoint()
    #     # print("obs", obs)
    #     for literal in obs:
    #         if literal.predicate == "atop":
    #             item_name = literal.variables[0].name
    #             station_name = literal.variables[1].name
    #             station_pos = self._get_station_position(station_name)
                
    #             if item_name == "aed":
    #                 self._draw_image(
    #                     surface,
    #                     "aed.png",
    #                     station_pos * self.pix_square_size,
    #                     self.pix_square_size * 0.5,
    #                 )
    #             elif item_name == "cpr_kit":
    #                 self._draw_image(
    #                     surface,
    #                     "cpr_kit.png",
    #                     station_pos * self.pix_square_size,
    #                     self.pix_square_size * 0.5,
    #                 )
    #             elif item_name == "ventilator":
    #                 self._draw_image(
    #                     surface,
    #                     "ventilator.png",
    #                     station_pos * self.pix_square_size,
    #                     self.pix_square_size * 0.5,
    #                 )
    #             elif item_name == "medicine":
    #                 self._draw_image(
    #                     surface,
    #                     "medicine.png",
    #                     station_pos * self.pix_square_size,
    #                     self.pix_square_size * 0.5,
    #                 )