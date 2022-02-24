from typing import Optional


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        space = '' if self.calories > 0 else ' '
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность:{self.duration: .3f} ч.; '
                f'Дистанция:{self.distance: .3f} км; '
                f'Ср. скорость:{self.speed: .3f} км/ч; '
                f'Потрачено ккал:{space}{self.calories: .3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = (self.action * self.LEN_STEP) / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        t_in_m: int = 60
        calories = ((self.coeff_calorie_1 *
                    self.get_mean_speed() - self.coeff_calorie_2) *
                    self.weight / self.M_IN_KM *
                    self.duration * t_in_m)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 2
    coeff_calorie_5 = 0.029
    T_IN_M = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        part_b = (self.get_mean_speed() ** self.coeff_calorie_4 // self.height)
        part_f = self.coeff_calorie_3 * self.weight
        part_c = (part_f + part_b * self.coeff_calorie_5 * self.weight)
        calories = part_c * self.duration * self.T_IN_M
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        part_d = (self.length_pool * self.count_pool)
        speed = part_d / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        coeff_calorie_6 = 1.1
        coeff_calorie_7 = 2
        part_e = (self.get_mean_speed() + coeff_calorie_6)
        calories = part_e * coeff_calorie_7 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    code = {'RUN': Running,
            'SWM': Swimming,
            'WLK': SportsWalking}
    if workout_type == 'SWM':
        return code[workout_type](*data)
    elif workout_type == 'RUN':
        return code[workout_type](*data)
    elif workout_type == 'WLK':
        return code[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
