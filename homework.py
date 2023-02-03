from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; Ср. скорость: '
        '{speed:.3f} км/ч; Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**self.__dict__)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Размер 1 шага\гребка
    M_IN_KM = 1000  # константа для перевода м в км
    MIN_IN_HOUR = 60  # Кол-во минут в 1 часе
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # коэф. ср. скорости сжигания калорий
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # сдвиг средней скорости сжигания калорий

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def training_time_in_minutes(self) -> int:
        """Получить время тренировки в минутах."""
        return self.duration * self.MIN_IN_HOUR

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.
        метод неопределен, потому что у каждого класса он свой"""
        raise NotImplementedError('Реализация метода отсутсвует!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # Константа наследуется, но тесты.
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # Тоже самое

    def get_spent_calories(self) -> float:
        """Переопределённый метод расчёта калорий для бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / super().M_IN_KM
                * super().training_time_in_minutes())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    KMH_TO_MPS = 0.278
    CM_TO_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def height_in_m(self):
        """Рост в метрах"""
        return self.height / self.CM_TO_M

    def get_spent_calories(self) -> float:
        """Переопределенный метод подсчёта калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight + ((super().get_mean_speed()
                 * self.KMH_TO_MPS) ** 2 / self.height_in_m())
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight)
                * super().training_time_in_minutes())


class Swimming(Training):
    """Тренировка: плавание."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1  # ср. расход калорий
    CALORIES_MEAN_SPEED_SHIFT = 2  # коэф. сдвига ср. числа калорий
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """"Переопределенный метод расчёта средней скорости для плавания."""
        return (self.length_pool * self.count_pool
                / super().M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """"Переопределенный метод расчёта затраченных калорий для плавания"""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dct = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    if workout_type in training_dct.keys():
        return training_dct.get(workout_type)(*data)
    raise ValueError('Неверный код тренировки, '
                     f'допустимые значения: {list(training_dct.keys())}.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
