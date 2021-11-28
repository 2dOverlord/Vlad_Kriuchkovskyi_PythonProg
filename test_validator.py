import unittest
from transaction import Transaction
from validator import ValidatorException, Validator


class ValidatorClassTests(unittest.TestCase):
    def setUp(self) -> None:
        self.validator = Validator()
        self.validator.obj_id = 1

    def test_validator_info(self):
        try:
            transaction = Transaction(1, "12", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000")
        except ValidatorException as val_err:
            err = val_err
        self.assertEqual(err.get_field_name(), "payer_name")
        self.assertEqual(str(err), "Payer name must not contain anything except of letters")

    def test_if_poss_to_int(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_if_possible_to_int(card_number="ab")

    def test_check_month(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_month("13")

    def test_check_year(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_year("2012")

    def test_check_cvc(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_cvc("090909")

    def test_check_payment_date(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_payment_date("01.01.2100")
        with self.assertRaises(ValidatorException):
            self.validator.check_payment_date("01.13.2020")
        with self.assertRaises(ValidatorException):
            self.validator.check_payment_date("49.09.2020")

    def test_paymount(self):
        with self.assertRaises(ValidatorException):
            self.validator.check_amount("0")
        with self.assertRaises(ValidatorException):
            self.validator.check_amount("av")

