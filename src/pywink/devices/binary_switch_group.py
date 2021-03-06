from pywink.devices.base import WinkDevice


class WinkBinarySwitchGroup(WinkDevice):
    """
    Represents a Wink binary switch group.
    """

    def state(self):
        """
        Groups states is determined based on a combination of all devices states
        """
        return bool(self.state_true_count() != 0)

    def reading_aggregation(self):
        return self.json_state.get("reading_aggregation")

    def state_true_count(self):
        return self.reading_aggregation().get("powered").get("true_count")

    def available(self):
        count = self.reading_aggregation().get("connection").get("true_count")
        if count > 0:
            return True
        return False

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        desired_state = {"desired_state": {"powered": state}}
        response = self.api_interface.set_device_state(self, desired_state)
        self._update_state_from_response(response)
