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
        pass

    def pump_on_patient(self, obs):
        pass

    def aed_held(self, obs):
        pass

    def aed_on_cpr(self, obs):
        pass

    def medicine_held(self, obs):
        pass

    def medicine_on_aed(self, obs):
        pass

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
        correct_order = ["cpr_board", "patient", "pump", "aed", "medicine"]
        chest_compressed = False
        rescue_breathed = False
        shocked = False
        medicine_given = False

        # See if goals (stacking, cooking, cutting) are met
        score = 0
        for clause in obs.goal.literals:
            for goal in clause.literals:
                for literal in obs.literals:
                    if goal == literal:
                        if goal.predicate == "iscooked":
                            cooked = True
                        if goal.predicate == "iscut":
                            cut = True

        # Check if the stacking is correct (Correct order + cooked burger + cut lettuce)
        for i in range(len(correct_stacking)):
            if not correct_stacking[2 - i]:
                break
            if i == 0 and not cooked:
                break
            elif i == 1 and (not cut or not cooked):
                break
            elif i == 2 and not cut:
                break
            score += 30

        # Give reward for cut. If not, give reward for uncut lettuce on board and uncut lettuce held
        if cut:
            score += 45
        else:
            score += 15 if self._check_lettuce_board(obs) else 0
            score += 5 if self._check_lettuce_held(obs) else 0

        # Give reward for each cut in the lettuce
        item_status = self.state.get("lettuce1")
        if item_status is not None and item_status.get("cut") is not None:
            score += 10 * item_status["cut"] if item_status["cut"] < 3 else 0

        return score
