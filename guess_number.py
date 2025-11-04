from datetime import datetime as dt
from random import randint

from access_control import access_control
from constants import ADMIN_USERNAME, UNKNOWN_COMMAND


class GuessNumberGame:
    def __init__(self):
        self.start_time = dt.now()
        self.player_name = ""
        self.total_games = 0
        self.total_attempts = 0
        self.best_score = float('inf')  # Минимальное количество попыток
        self.current_game_attempts = 0

    def set_player_name(self, name: str) -> None:
        """Установка имени игрока с приветствием"""
        self.player_name = name.strip()
        if self.player_name == ADMIN_USERNAME:
            print(
                '\nДобро пожаловать, создатель! '
                'Во время игры вам доступны команды "stat", "answer"'
            )
        else:
            print(f'\n{self.player_name}, добро пожаловать в игру!')

    def get_player_name(self) -> str:
        """Получение имени игрока"""
        return self.player_name

    @access_control
    def get_statistics(self) -> None:
        """Получение статистики игры (только для админа)"""
        game_time = dt.now() - self.start_time
        avg_attempts = self.total_attempts / self.total_games if self.total_games > 0 else 0

        print(f'\n=== СТАТИСТИКА ИГРЫ ===')
        print(f'Игрок: {self.player_name}')
        print(f'Всего сыграно игр: {self.total_games}')
        print(f'Общее время игры: {game_time}')
        print(f'Всего попыток: {self.total_attempts}')
        print(f'Среднее количество попыток: {avg_attempts:.1f}')
        if self.best_score != float('inf'):
            print(f'Лучший результат: {self.best_score} попыток')
        print(f'Текущая игра: попытка №{self.current_game_attempts}')

    @access_control
    def get_right_answer(self, number: int) -> None:
        """Показать правильный ответ (только для админа)"""
        print(f'Правильный ответ: {number}')

    def check_number(self, guess: int, number: int) -> bool:
        """Проверка угаданного числа"""
        self.current_game_attempts += 1

        if guess == number:
            print(f'Отличная интуиция, {self.player_name}! Вы угадали число :)')
            print(f'Количество попыток: {self.current_game_attempts}')
            
            # Обновляем статистику
            self.total_attempts += self.current_game_attempts
            if self.current_game_attempts < self.best_score:
                self.best_score = self.current_game_attempts
                print(f'Новый рекорд!')
            
            return True

        if guess < number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False

    def play_round(self) -> None:
        """Один раунд игры"""
        number = randint(1, 100)
        self.current_game_attempts = 0

        print(
            '\nУгадайте число от 1 до 100.\n'
            'Для выхода из текущей игры введите команду "stop"'
        )

        while True:
            user_input = input('Введите число или команду: ').strip().lower()

            match user_input:
                case 'stop':
                    break
                case 'stat':
                    self.get_statistics()
                case 'answer':
                    self.get_right_answer(number)
                case _:
                    try:
                        guess = int(user_input)                
                    except ValueError:
                        print(UNKNOWN_COMMAND)
                        continue

                    if self.check_number(guess, number):
                        break

    def get_username(self) -> None:
        """Запрос имени пользователя"""
        username = input('Представьтесь, пожалуйста, как Вас зовут?\n')
        self.set_player_name(username)

    def start(self) -> None:
        """Запуск основной игровой сессии"""
        self.get_username()

        while True:
            self.total_games += 1
            self.play_round()

            play_again = input(f'\nХотите сыграть ещё? (yes/no) ')
            if play_again.strip().lower() not in ('y', 'yes'):
                break

        # Показываем финальную статистику при выходе
        if self.total_games > 0:
            print(f'\n=== ФИНАЛЬНАЯ СТАТИСТИКА ===')
            print(f'Сыграно игр: {self.total_games}')
            print(f'Лучший результат: {self.best_score if self.best_score != float("inf") else "N/A"} попыток')
            print(f'Всего попыток: {self.total_attempts}')
            print('Спасибо за игру!')
