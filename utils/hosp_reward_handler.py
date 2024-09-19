from utils.reward_handler import RewardHandler


class HospRewardHandler(RewardHandler):
    def __init__(self):
        super().__init__()

    def _check_CPRboard_patient(self, obs):
        for literal in obs.literals:
            if (
                "on" == literal.predicate.name
                and "cpr_board" in literal.variables[0].name
                and "patient_bed_station" in literal.variables[1].name
            ):
                return True
        return False

    def pump_held(self, obs):
        for literal in obs.literals:
            if "has" == literal.predicate.name and "pump" in literal.variables[1].name:
                return True
        return False
        

    def pump_on_patient(self, obs):
        for literal in obs.literals:
            if (
                "atop" == literal.predicate.name
                and "pump" in literal.variables[0].name
                and "patient" in literal.variables[1].name
            ):
                return True
        return False

    def aed_held(self, obs):
        for literal in obs.literals:
            if "has" == literal.predicate.name and "aed" in literal.variables[1].name:
                return True
        return False
        

    def aed_on_pump(self, obs):
        for literal in obs.literals:
            if (
                "atop" == literal.predicate.name
                and "aed" in literal.variables[0].name
                and "pump" in literal.variables[1].name
            ):
                return True
        return False

    def medicine_held(self, obs):
        for literal in obs.literals:
            if "has" == literal.predicate.name and "medicine" in literal.variables[1].name:
                return True
        return False
    
    def medicine_on_aed(self, obs):
        for literal in obs.literals:
            if (
                "atop" == literal.predicate.name
                and "medicine" in literal.variables[0].name
                and "aed" in literal.variables[1].name
            ):
                return True
        return False

    def heuristic_reward(self, obs, state):
        """
        This function is a heuristic function that is used to generate a plan.

        Args:
            obs (PDDLGym State): The current state of the environment.

        Returns: The measure of "goodness" of the state.

        Goodness of state of determined by:
            1. Patient is properly being treated (ischestcompressed, isrescuebreathed, isshocked, istreated)
            2. CPR board being underneath the patient
            3. The equipment being in the correct order
            4. The progress the player is making towards using equipment properly (going to correct stations, picking up equipment, placing it down correctly)
        """

        # Example goal: [AND[iscut(lettuce1:item), atop(topbun1:item,lettuce1:item), iscooked(patty1:item), atop(lettuce1:item,patty1:item), atop(patty1:item,bottombun1:item)]]
        self.obs = obs
        self.state = state
        correct_order = ["cpr_board", "patient", "pump", "aed", "syringe"]
        score = 0
        chest_compressed = False
        rescue_breathed = False
        shocked = False
        medicine_given = False
        
        # Check if goals are met
        for clause in obs.goal.literals:
            for goal in clause.literals:
                for literal in obs.literals:
                    if goal == literal:
                        if goal.predicate.name == "ischestcompressed":
                            chest_compressed = True
                        elif goal.predicate.name == "isrescuebreathed":
                            rescue_breathed = True
                        elif goal.predicate.name == "isshocked":
                            shocked = True
                        elif goal.predicate.name == "istreated":
                            medicine_given = True

        # Check if the CPR board is under the patient
        if self._check_CPRboard_patient(obs):
            score += 30                    

        # Check if equipment is in the correct order
        correct_stacking = [
            self._check_CPRboard_patient(obs),
            self.pump_on_patient(obs),
            self.aed_on_pump(obs),
            self.medicine_on_aed(obs)
        ]
        for i, stacked in enumerate(correct_stacking):
            if stacked:
                score += 15 * (i + 1)
            else:
                break

        # Give rewards for each action progress
        for action in ["compresschest", "giverescuebreaths", "giveshock", "givemedicine"]:
            item_status = self.state.get("patient1", {})
            if item_status.get(action) is not None:
                max_count = {"compresschest": 3, "giverescuebreaths": 2, "giveshock": 1, "givemedicine": 1}[action]
                count = min(item_status[action], max_count)
                score += 10 * count

        # Give rewards for completed actions
        if chest_compressed:
            score += 20
        if rescue_breathed:
            score += 25
        if shocked:
            score += 30
        if medicine_given:
            score += 35

        # Give rewards for progress towards using equipment
        score += 5 if self.pump_held(obs) else 0
        score += 5 if self.aed_held(obs) else 0
        score += 5 if self.medicine_held(obs) else 0
        return score    
        
