from yakshop.utils.xml_reader import read_xml
from typing import List, Tuple


class YakOperator(object):
    def __init__(self, yaks: List[dict] = None):
        self.herd = yaks
        self.start_wool_amount = len(yaks)
        self.wool_delivered = 0
        self.milk_delivered = 0

    @classmethod
    def init_herd(cls, path: str):
        return cls(read_xml(path_to_file=path))

    @staticmethod
    def _is_eligible_for_cut(age_in_days: float, dt: int) -> bool:
        # At most every 8+D*0.01 days you can again shave a LabYak (D = age in days)=
        # K A yak’s first shave can occur at the age of 1 year=
        # 100 days = 1 yak year
        return (
            dt % (8 + age_in_days * 0.01) == 0 if 100 < age_in_days <= 1000 else False
        )

    def calculate_stock(self, dt: int):
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
        eligible_time = self._calculate_eligible_time(age_in_days=age_in_days)
        wool_produced = self._calculate_wool_over_time(
            age_in_days=age_in_days, dt=dt - 2
        )
        day_shift = 2 if wool_produced >= 1 else 0

        return day_shift + age_in_days + (wool_produced * eligible_time)

    def pack_order(
        self, milk_ordered: float, wool_ordered: int, dt: int
    ) -> Tuple[float, float]:
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
        return 8 + age_in_days * 0.01

    @staticmethod
    def _calculate_milk(age_in_days: float) -> float:
        # Each day a LabYak produces 50-D*0.03 liters of milk (D = age in days)
        return 50 - age_in_days * 0.03

    def _calculate_wool_over_time(self, age_in_days: float, dt: int):
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
        # set a limit to dt
        dt = 1000 - age_in_days if age_in_days + dt > 1000 else dt
        milk_produced = 0

        for i in range(int(dt)):
            milk_produced += self._calculate_milk(age_in_days)
            age_in_days += 1
        return milk_produced

    @staticmethod
    def _calculate_age(age_in_days: float, dt: int) -> float:
        return (age_in_days + dt) / 100
