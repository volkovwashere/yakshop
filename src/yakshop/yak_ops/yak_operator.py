from yakshop.utils.xml_reader import read_xml
from typing import List, Tuple, Union


class YakOperator(object):
    def __init__(self, yaks: List[dict] = None):
        self.herd = yaks
        self.start_wool_amount = len(yaks)
        self.wool_delivered = 0
        self.milk_delivered = 0

    @classmethod
    def init_herd(cls, path: str) -> "YakOperator":
        """
        This class method initializes the herd class instances of the YakOperator class.
        Args:
            path (str): String path to the xml

        Returns (YakOperator): Returns the class instances

        """
        return cls(read_xml(path_to_file=path))

    @staticmethod
    def _is_eligible_for_cut(age_in_days: float, dt: int) -> bool:
        """
        This static method checks whether the given yak is eligible for a cut or not. Does not check special cases
        if the yak is too young or dead.
        Args:
            age_in_days (float): Age of the yaks in days
            dt (int): Elapsed time

        Returns (bool): Returns True or False

        """
        # At most every 8+D*0.01 days you can again shave a LabYak (D = age in days)=
        # K A yak’s first shave can occur at the age of 1 year=
        # 100 days = 1 yak year
        return (
            dt % (8 + age_in_days * 0.01) == 0 if 100 < age_in_days <= 1000 else False
        )

    def calculate_stock(self, dt: int) -> dict:
        """
        This method calculates the available stock based on the first state after initialization. Does not take
        the total amount of delivered into account.
        Args:
            dt (int): Elapsed time

        Returns (dict): Returns the produced milk / wool over a given time period.

        """
        amount_of_milk = (
            self._calculate_milk_over_time(dt=dt, age_in_days=float(yak["age"]) * 100)
            for yak in self.herd
        )
        amount_of_wool = (
            self._calculate_wool_over_time(
                age_in_days=float(yak["age"]) * 100, dt=dt - 2
            )
            for yak in self.herd
        )

        amount_of_milk = round(sum(amount_of_milk), 2)
        amount_of_wool = int(sum(amount_of_wool) + self.start_wool_amount)
        return {"milk": amount_of_milk, "wool": amount_of_wool}

    def herd_state_after_t_days(self, dt: int) -> List[dict]:
        """
        This function calculates the herd state (name, age, last_cut) based on the fist initialization day 0.
        Args:
            dt (int): Elapsed time

        Returns (list): Returns a list of yaks with the current state (name, age, last_shaved.)

        """
        yak_ages = (
            self._calculate_age(age_in_days=float(yak["age"]) * 100, dt=dt)
            for yak in self.herd
        )
        last_shaved = (
            self._calculate_last_shaved(age_in_days=float(yak["age"]) * 100, dt=dt)
            for yak in self.herd
        )
        return [
            {
                "name": yak["name"],
                "age": yak_age,
                "age_last_shaved": last_shave_date / 100,
            }
            for yak, yak_age, last_shave_date in zip(self.herd, yak_ages, last_shaved)
        ]

    def _calculate_last_shaved(self, age_in_days: float, dt: int) -> float:
        """
        This function calculates when was a yak last shaved based on the age and the elapsed time.
        Args:
            age_in_days (float): Age in days
            dt (int): Elapsed time.

        Returns (float): Last shaved age in days.

        """
        eligible_time = self._calculate_eligible_time(age_in_days=age_in_days)
        wool_produced = self._calculate_wool_over_time(
            age_in_days=age_in_days, dt=dt - 2
        )
        # Shift constant. Shift the date if wool was produced else don't to get the right last_cut date.
        day_shift = 2 if wool_produced >= 1 else 0

        return day_shift + age_in_days + (wool_produced * eligible_time)

    def pack_order(
        self, milk_ordered: float, wool_ordered: int, dt: int
    ) -> Tuple[float, float]:
        """
        This function "packs" a given order. It basically calculates how much milk / wool is available on stock
        given an elapsed time and returns it. The function also updates a global state, the total delivered amount,
        that will be taken into account when calculating the total amount available.
        Args:
            milk_ordered (float): Amount of milk ordered.
            wool_ordered (float): Amount of wool skin ordered.
            dt (int): Elapsed time.

        Returns (tuple): Available milk, Available wool

        """
        on_stock = self.calculate_stock(dt=dt)
        milk_available = on_stock["milk"] - self.milk_delivered
        wool_available = on_stock["wool"] - self.wool_delivered

        milk_deliverable = milk_ordered if (milk_available - milk_ordered) >= 0 else 0
        wool_deliverable = wool_ordered if (wool_available - wool_ordered) >= 0 else 0

        self.milk_delivered += milk_deliverable
        self.wool_delivered += wool_deliverable

        return milk_deliverable, wool_deliverable

    @staticmethod
    def _calculate_eligible_time(age_in_days: float) -> float:
        """
        This static method returns the eligible time based on the age of a yak in days. The eligible time is the time
        in days when a yak is shaveable.
        Args:
            age_in_days (float): Age of a yak in days

        Returns (float): Eligible time

        """
        return 8 + age_in_days * 0.01

    @staticmethod
    def _calculate_milk(age_in_days: float) -> float:
        """
        This static method returns the produce milk based on the age of yak in days.
        Args:
            age_in_days (float): Age of a yak in days.

        Returns (float): Amount of milk that a yak can produce.

        """
        # Each day a LabYak produces 50-D*0.03 liters of milk (D = age in days)
        return 50 - age_in_days * 0.03

    def _calculate_wool_over_time(
        self, age_in_days: float, dt: int
    ) -> Union[float, int]:
        """
        This function calculates the wool skin produced over time for a yak based on elapsed time and age in days.
        The function takes into account if a yak is too young or dead.
        Args:
            age_in_days (float): Age of a yak in days
            dt (int): Elapsed time in days.

        Returns (float or int): Return a float or int.

        """
        is_dead, is_young = age_in_days + dt > 1000, age_in_days + dt < 100

        eligible_time = self._calculate_eligible_time(age_in_days=age_in_days)
        n_in = (
            dt // eligible_time
            if not is_dead
            else (1000 - age_in_days) // eligible_time
        )
        is_eligible = self._is_eligible_for_cut(age_in_days=age_in_days, dt=dt)

        if is_eligible:
            return dt / eligible_time
        elif is_young:
            return 0
        elif not is_eligible and n_in >= 1:
            return n_in
        else:
            return 0

    def _calculate_milk_over_time(self, dt: int, age_in_days: float) -> float:
        """
        This function calculates the milk produced over time.
        Args:
            dt (int): Elapsed time.
            age_in_days (float): Age of a yak in days.

        Returns (float): total produced milk over time.

        """
        # set a limit to dt
        dt = 1000 - age_in_days if age_in_days + dt > 1000 else dt
        milk_produced = 0

        for i in range(int(dt)):
            milk_produced += self._calculate_milk(age_in_days)
            age_in_days += 1
        return milk_produced

    @staticmethod
    def _calculate_age(age_in_days: float, dt: int) -> float:
        """
        This function calculates the age of a yak over time.
        Args:
            age_in_days (float): Age of a yak in days.
            dt (int): Elapsed time

        Returns (float): Age of a yak in years.

        """
        return (age_in_days + dt) / 100
