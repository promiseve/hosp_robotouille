from utils.reward_handler import RewardHandler

class HospRewardHandler(RewardHandler):
    def __init__(self, config):
        super().__init__()
        self.config = config  # Keep config for reference if needed
        # self.pickup_order = ["cpr_board","pump","aed","syringe"]
        # self.picked_items = []


    def _check_item_on_station(self, obs, item, station):
        """Check if an item is on a specific station."""
        for literal in obs.literals:
            if (
                "on" == literal.predicate.name
                and item in literal.variables[0].name
                and station in literal.variables[1].name
            ):
                return True
        return False

    def _check_item_on_item(self, obs, top_item, bottom_item):
        """Check if one item is on top of another."""
        for literal in obs.literals:
            if (
                "on" == literal.predicate.name
                and top_item in literal.variables[0].name
                and bottom_item in literal.variables[1].name
            ):
                return True
        return False

    def _check_item_held(self, obs, item):
        """Check if an item is being held."""
        for literal in obs.literals:
            if "has" == literal.predicate.name and item in literal.variables[1].name:
                return True
        return False

    def _check_predicate(self, obs, predicate, item):
        """Check if a specific predicate is true for an item."""
        for literal in obs.literals:
            if predicate == literal.predicate.name and item in literal.variables[0].name:
                return True
        return False

    # def _update_pickup_order(self, item):
    #     """Update the list of picked up items."""
    #     if item in self.pickup_order and item not in self.picked_items:
    #         self.picked_items.append(item)

    # def _check_pickup_order(self,):
    #     """Check if the picked up items are in the correct order."""
    #     return self.picked_items == self.pickup_order[:len(self.picked_items)]
        

    def _check_action_progress(self, state, action, item="patient1"):
        """
        Check the progress of a specific action for a given item.
        
        Args:
        state (dict): The current state of the environment
        action (str): The action we're checking progress for
        item (str): The item the action is being performed on (default is "patient1")
        
        Returns:
        int: The current progress of the action, or 0 if no progress
        """
        item_status = state.get(item, {})
        return item_status.get(action, 0)

    def _calculate_action_reward(self, progress, max_progress):
        """
        Calculate reward based on action progress.
        
        Args:
        progress (int): Current progress of the action
        max_progress (int): Maximum progress for the action
        
        Returns:
        int: Calculated reward
        """
        if progress == 0:
            return 0
        elif progress == max_progress:
            return 20  # Maximum reward for completing the action
        else:
            # Graduated reward: more reward for later actions
            return 5 * progress

    def heuristic_reward(self, obs, state):
        """
        Calculate the heuristic reward based on the current observation and state.
        
        Args:
        obs: The current observation
        state: The current state of the environment
        
        Returns:
        float: The calculated reward
        """
        self.obs = obs
        self.state = state
        score = 0

        # Check if the goal is met (patient is treated)
        if self._check_predicate(obs, "istreated", "patient1"):
            return 170  # Maximum score for completing the goal
                # Update picked items based on current state

        # for item in self.pickup_order:
        #     if self._check_item_held(obs, item):
        #         self._update_pickup_order(item)

        # if not self._check_pickup_order():
        #     print(f"Incorrect pickup order: {self.picked_items} vs expected {self.pickup_order}")
        #     score -= 10  # Penalty for incorrect order
            #         print("literal.variables[0].name" : literal.variables[0].name)
            # print("literal.variables[].name" : literal.variables[1].name)

        # 1. CPR board placement
        if self._check_item_on_station(obs, "cpr_board", "patient_bed_station"):
            score += 10  # Reward for correct placement
        if self._check_item_held(obs, "cpr_board"):
            score += 5   # Smaller reward for holding the CPR board

        # 2. Chest compressions
        chest_compression_progress = self._check_action_progress(state, "compresschest")
        score += self._calculate_action_reward(chest_compression_progress, 3)
        if self._check_predicate(obs, "ischestcompressed", "patient1"):
            score += 15  # Additional reward for completing compressions

        # 3. Pump placement and rescue breaths
        if self._check_item_on_item(obs, "pump1", "patient1"):
            score += 10  # Reward for correct pump placement
        elif self._check_item_held(obs, "pump1"):
            score += 5   # Smaller reward for holding the pump

        rescue_breath_progress = self._check_action_progress(state, "giverescuebreaths")
        score += self._calculate_action_reward(rescue_breath_progress, 2)
        if self._check_predicate(obs, "isrescuebreathed", "patient1"):
            score += 15  # Additional reward for completing rescue breaths

        # 4. AED placement and shock
        if self._check_item_on_item(obs, "aed1", "pump1"):
            score += 10  # Reward for correct AED placement
        elif self._check_item_held(obs, "aed1"):
            score += 5   # Smaller reward for holding the AED

        shock_progress = self._check_action_progress(state, "giveshock")
        score += self._calculate_action_reward(shock_progress, 1)
        if self._check_predicate(obs, "isshocked", "patient1"):
            score += 15  # Additional reward for completing shock

        # 5. Medicine administration
        if self._check_item_on_item(obs, "syringe1", "aed1"):
            score += 10  # Reward for correct syringe placement
        elif self._check_item_held(obs, "syringe1"):
            score += 5   # Smaller reward for holding the syringe

        medicine_progress = self._check_action_progress(state, "givemedicine")
        score += self._calculate_action_reward(medicine_progress, 1)

        return score

# Note: This updated reward structure uses self.state to track action progress
# and provides graduated rewards for repeated actions, with higher rewards
# for completing actions up to their maximum allowed repetitions.