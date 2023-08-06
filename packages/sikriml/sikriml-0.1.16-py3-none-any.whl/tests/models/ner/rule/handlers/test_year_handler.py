import unittest

from sikriml.models.ner import ScoreEntity, ScoreLabel
from sikriml.models.ner.rule.handlers import NumberHandler, YearHandler

handler = YearHandler()


class UrlHandlerTest(unittest.TestCase):
    def test_year_handler_correct_result(self):
        # Arrange
        year = "1990"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 16, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_apostrophe(self):
        # Arrange
        year = "1990's"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 18, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_one_char(self):
        # Arrange
        year = "1990s"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 17, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_with_two_chars(self):
        # Arrange
        year = "1990th"
        # Act
        result = handler.process(f"Was born in {year}")
        # Assert
        expected_result = set([ScoreEntity(year, 12, 18, ScoreLabel.YEAR)])
        self.assertSetEqual(result, expected_result)

    def test_year_handler_invalid_year(self):
        # Arrange
        year = "2990"
        # Act
        result = handler.process(f"Some random number {year}")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_returns_empty_set(self):
        # Act
        result = handler.process("Date of birth is unknown")
        # Assert
        self.assertSetEqual(result, set())

    def test_year_handler_as_decorator(self):
        # Arrange
        number_handler = NumberHandler()
        year_decorator = YearHandler(number_handler)
        year = "2000's"
        number = "22"
        # Act
        result = year_decorator.process(f"Was born in {year}. He is {number}")
        # Assert
        expected_result = set(
            [
                ScoreEntity(year, 12, 18, ScoreLabel.YEAR),
                ScoreEntity(number, 26, 28, ScoreLabel.NUMB),
            ]
        )
        self.assertSetEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
