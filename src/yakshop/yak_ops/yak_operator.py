from yakshop.utils.xml_reader import read_xml
from typing import List


class YakOperator(object):
    def __init__(self, yaks: List[dict] = None):
        self.herd = yaks
        self.start_wool_amount = len(yaks)

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
        yak_ages = (
            self._calculate_age(age_in_days=float(yak["age"]) * 100, dt=dt)
            for yak in self.herd
        )
        amount_of_milk = round(sum(amount_of_milk), 2)
        amount_of_wool = int(sum(amount_of_wool) + self.start_wool_amount)

        print(
            f"In stock \n{amount_of_milk} liters of milk \n{amount_of_wool} skins of wool"
        )
        for yak, yak_age in zip(self.herd, yak_ages):
            print(f"{yak['name']} {yak_age} years old")

    @staticmethod
    def _calculate_milk(age_in_days: float) -> float:
        # Each day a LabYak produces 50-D*0.03 liters of milk (D = age in days)
        return 50 - age_in_days * 0.03

    def _calculate_wool_over_time(self, age_in_days: float, dt: int):
        eligible_time = 8 + age_in_days * 0.01
        n_in = dt // eligible_time
        is_eligible = self._is_eligible_for_cut(age_in_days=age_in_days, dt=dt)

        if is_eligible:
            return dt / eligible_time
        elif not is_eligible and n_in >= 1:
            return n_in
        else:
            return 0

    def _calculate_milk_over_time(self, dt: int, age_in_days: float) -> float:
        if dt <= 1:
            return self._calculate_milk(age_in_days=age_in_days)
        else:
            return self._calculate_milk(
                age_in_days=age_in_days
            ) + self._calculate_milk_over_time(dt=dt - 1, age_in_days=age_in_days + 1)

    @staticmethod
    def _calculate_age(age_in_days: float, dt: int) -> float:
        return (age_in_days + dt) / 100