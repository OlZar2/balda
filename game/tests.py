import unittest
from balda_model import GameModel

class TestGameModel(unittest.TestCase):

    def setUp(self):
        self.game = GameModel()

    def test_initial_board_setup(self):
        expected_row = ["Б", "А", "Л", "Д", "А"]
        self.assertEqual(self.game.board[2], expected_row)
        for y in range(5):
            if y != 2:
                self.assertTrue(all(cell == "" for cell in self.game.board[y]))

    def test_add_letter_to_board(self):
        self.game.add_letter_to_board(3, 3, "С")
        self.assertEqual(self.game.board[3][3], "С")
        with self.assertRaises(ValueError):
            self.game.add_letter_to_board(4, 4, "Т")

    def test_clear_added_letter(self):
        self.game.add_letter_to_board(3, 3, "С")
        self.game.clear_added_letter()
        self.assertEqual(self.game.board[3][3], "")
        self.assertEqual(self.game.added_letter_pos, [None, None])

    def test_add_word(self):
        self.game.add_letter_to_board(2, 3, "С")
        self.game.add_letter_to_word(2, 2)
        self.game.add_letter_to_word(2, 3)
        self.game.add_word()
        self.assertIn("ЛС", self.game.word_list)
        self.assertEqual(self.game.scores[0], 2)  # Слово из 2 букв

    def test_switch_player(self):
        self.assertEqual(self.game.current_player, 0)
        self.game.switch_player(True)
        self.assertEqual(self.game.current_player, 1)
        self.assertEqual(self.game.pass_count, 0)  # Сброс пропуска

    def test_pass_turn_and_game_over(self):
        self.game.pass_turn()
        self.assertEqual(self.game.pass_count, 1)
        with self.assertRaises(ValueError):
            self.game.pass_turn()

if __name__ == "__main__":
    unittest.main()
