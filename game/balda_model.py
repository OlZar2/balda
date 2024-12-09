class GameModel:
    def __init__(self):
        self.board = [["" for _ in range(5)] for _ in range(5)]
        self.word_list = set()
        self.scores = [0, 0]
        self.current_player = 0
        self.pass_count = 0
        self.added_letter_pos = [None, None]
        self.current_letter_pos = [None, None]
        self.current_word = ""
        self.init_board()

    def init_board(self):
        initial_word = "БАЛДА"
        for i, char in enumerate(initial_word):
            self.board[2][i] = char

    def add_letter_to_board(self, x, y, letter):
        if self.added_letter_pos[0] != None:
            raise ValueError("Вы уже ввели букву")
        self.board[y][x] = letter
        self.added_letter_pos = [y, x]
    
    def clear_added_letter(self):
        if(self.added_letter_pos[0] != None):
            self.board[self.added_letter_pos[0]][self.added_letter_pos[1]] = ""
            self.added_letter_pos[0] = self.added_letter_pos[1] = None
    
    def is_valid_letter(self, x, y):
        if self.current_letter_pos[0] == None:
            return True
        if((self.current_letter_pos[0] + 1 >= y >= self.current_letter_pos[0] - 1)
            and (self.current_letter_pos[1] + 1 >= x >= self.current_letter_pos[1] - 1)):
            return True
        return False

    def add_letter_to_word(self, x, y):
        if(self.added_letter_pos[0] == None):
            raise ValueError("Сначала введите букву")
        if(self.is_valid_letter(x, y) == False):
            raise ValueError("Выберите букву рядом с текущей")
        self.current_word += self.board[y][x]
        self.current_letter_pos = [y, x]

    def add_word(self):
        if self.current_word in self.word_list:
            raise ValueError("Слово уже использовано")

        self.word_list.add(self.current_word)
        self.scores[self.current_player] += len(self.current_word)
        self.current_word = ""
        self.current_letter_pos = self.added_letter_pos = [None, None]
        self.switch_player(True)

    def clear_current_actions(self):
        self.current_letter_pos = [None, None]
        self.clear_added_letter()
        self.current_word = ""

    def switch_player(self, reset):
        self.current_player = 1 - self.current_player
        if reset:
            self.pass_count = 0

    def pass_turn(self):
        self.pass_count += 1
        if self.pass_count >= 2:
            if(self.scores[0] > self.scores[1]):
                raise ValueError("Игра окончена: Победил игрок 1")
            if(self.scores[0] < self.scores[1]):
                raise ValueError("Игра окончена: Победил игрок 2")
            else:
                raise ValueError("Игра окончена: Ничья")
        self.switch_player(False)

    def is_game_over(self):
        for row in self.board:
            if "" in row:
                return False
        return True
