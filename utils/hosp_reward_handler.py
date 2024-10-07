from utils.reward_handler import RewardHandler

class HospRewardHandler(RewardHandler):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.correct_order = ["cpr_board", "patient", "pump", "aed", "syringe"]
        self.max_possible_reward = 300

    def _find_stacking_index(self, item1, item2):
        for i in range(len(self.correct_order) - 1):
            if (self.correct_order[i] in item1 and self.correct_order[i+1] in item2):
                return i
        return -1

    def _check_item_on_station(self, obs, item, station):
        for literal in obs.literals:
            if ("on" == literal.predicate.name
                and item in literal.variables[0].name
                and station in literal.variables[1].name):
                return True
        return False

    def _check_item_on_item(self, obs, top_item, bottom_item):
        for literal in obs.literals:
            if ("atop" == literal.predicate.name
                and top_item in literal.variables[0].name
                and bottom_item in literal.variables[1].name):
                return True
        return False

    def _check_item_held(self, obs, item):
        for literal in obs.literals:
            if "has" == literal.predicate.name and item in literal.variables[1].name:
                return True
        return False

    def _check_predicate(self, obs, predicate, item):
        for literal in obs.literals:
            if predicate == literal.predicate.name and item in literal.variables[0].name:
                return True
        return False

    def _check_action_progress(self, state, action, item="patient1"):
        item_status = state.get(item, {})
        return item_status.get(action, 0)

    def _calculate_action_reward(self, progress, max_progress):
        # Return based on the progress of the task. The minimum reward is 0 and the maximum reward is 20 if the task is completed.
        return min(20 * progress/max_progress, 20)

    def heuristic_reward(self, obs, state):
        self.obs = obs
        self.state = state
        score = 0

        if self._check_predicate(obs, "istreated", "patient1"):
            return 300

        correct_stacking = [False] * (len(self.correct_order) - 1)
        
        # Check correct stacking order
        for literal in obs.literals:
            if literal.predicate.name == "atop":
                index = self._find_stacking_index(literal.variables[1].name, literal.variables[0].name)
                if index != -1:
                    correct_stacking[index] = True

        # Give rewards for correct stacking
        for i, stacked in enumerate(correct_stacking):
            if stacked:
                score += 10 * (i + 1)
            else:
                break

        # CPR board placement
        if self._check_item_on_station(obs, "cpr_board", "patient_bed_station"):
            score += 10
        elif self._check_item_held(obs, "cpr_board"):
            score += 5

        # Chest compressions
        chest_compression_progress = self._check_action_progress(state, "compresschest")
        score += self._calculate_action_reward(chest_compression_progress, self.config["num_compressions"])
        if self._check_predicate(obs, "ischestcompressed", "patient1"):
            score += 15

        # Pump placement and rescue breaths
        if self._check_item_on_item(obs, "pump", "patient"):
            score += 10
        elif self._check_item_held(obs, "pump"):
            score += 5

        rescue_breath_progress = self._check_action_progress(state, "giverescuebreaths")
        score += self._calculate_action_reward(rescue_breath_progress, self.config["num_breaths"])
        if self._check_predicate(obs, "isrescuebreathed", "patient1"):
            score += 15

        # AED placement and shock
        if self._check_item_on_item(obs, "aed", "pump"):
            score += 10
        elif self._check_item_held(obs, "aed"):
            score += 5

        shock_progress = self._check_action_progress(state, "giveshock")
        score += self._calculate_action_reward(shock_progress, self.config["num_shocks"])
        if self._check_predicate(obs, "isshocked", "patient1"):
            score += 15

        # Medicine administration
        if self._check_item_on_item(obs, "syringe", "aed"):
            score += 10
        elif self._check_item_held(obs, "syringe"):
            score += 5

        medicine_progress = self._check_action_progress(state, "givemedicine")
        score += self._calculate_action_reward(medicine_progress, self.config["num_medicine_doses"])

        return score