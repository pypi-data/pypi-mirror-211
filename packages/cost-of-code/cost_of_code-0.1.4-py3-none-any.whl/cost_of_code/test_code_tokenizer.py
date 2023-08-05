import unittest
from cost_of_code.code_tokenizer import tokenize_code


class TestCodeTokenizer(unittest.TestCase):
    def test_tokenize_code(self):
        code = "for i in range(10):"
        num_tokens = tokenize_code(code)
        self.assertEqual(num_tokens, 7)


if __name__ == "__main__":
    unittest.main()
