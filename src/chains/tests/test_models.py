from django.core.exceptions import ValidationError
from django.db import DataError
from django.test import TestCase, TransactionTestCase
from faker import Faker

from .factories import ChainFactory


class ChainTestCase(TestCase):
    def test_str_method_outputs_name_chain_id(self):
        chain = ChainFactory.create()
        self.assertEqual(
            str(chain),
            f"{chain.name} | chain_id={chain.id}",
        )


class ChainColorValidationTestCase(TransactionTestCase):
    def test_invalid_text_colors(self):
        param_list = ["aaa", "bbb", "#fffffffff", "zzz", "010", "", "a word", "#hhh"]
        for invalid_color in param_list:
            with self.subTest(msg=f"Invalid color {invalid_color} should throw"):
                with self.assertRaises(
                    (
                        ValidationError,
                        DataError,
                    )
                ):
                    chain = ChainFactory.create(theme_text_color=invalid_color)
                    # run validators
                    chain.full_clean()

    def test_valid_text_colors(self):
        param_list = ["#000", "#fff", "#00000000", "#ffffffff"] + [
            Faker().hex_color() for _ in range(20)
        ]
        for valid_color in param_list:
            with self.subTest(msg=f"Valid color {valid_color} should not throw"):
                chain = ChainFactory.create(theme_text_color=valid_color)
                chain.full_clean()
