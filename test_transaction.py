import unittest
from transaction import Transaction, TransactionCollection
from validator import ValidatorException


class TransactionClassTests(unittest.TestCase):
    def setUp(self) -> None:
        self.transaction = Transaction(1, "Name", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000")

    def test_pos_result(self):
        """
            FIELDS:
            ID, payer_name, card_number (XXXX XXXX XXXX XXXX), month, year, CVC (XXX or XXXX), payment_date, amount.

            """
        self.assertEqual(self.transaction.id, 1)

    def test_wrong_id(self):
        with self.assertRaises(ValueError):
            Transaction("f", "Name", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000")

    def test_wrong_name(self):
        with self.assertRaises(ValidatorException):
            Transaction(2, "21", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000")

    def test_wrong_cn(self):
        with self.assertRaises(ValidatorException):
            Transaction(2, "Name", "21111222233334444", "01", "2022", "999", "01.01.2015", "1000")
        with self.assertRaises(ValidatorException):
            Transaction(3, "Name", "1f11222233334444", "01", "2022", "999", "01.01.2015", "1000")

    def test_to_dict(self):
        self.assertEqual(self.transaction.to_dict(), self.transaction.__dict__)

    def test_getter(self):
        self.assertEqual(self.transaction.__getitem__("id"), 1)

    def test_lt(self):
        sec_transaction = Transaction(2, "Matter", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000")
        self.assertFalse(sec_transaction < self.transaction)

    def test_str(self):
        st = "id: 1,\npayer name: Name,\ncard number: 1111222233334444,\nmonth: 1,\nyear: 2022," \
             "\npayment date: 01.01.2015,\ncvc: 999,\namount: 1000.0,"
        self.assertEqual(str(self.transaction), st)

    def test_setattr(self):
        self.transaction.__setattr__("id", 6)
        self.assertEqual(self.transaction.id, 6)


class TransactionCollectionClassTest(unittest.TestCase):
    def setUp(self) -> None:
        self.collection = TransactionCollection()
        self.collection.append([1, "Name", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000"])
        self.collection.append([2, "Name", "1111222233334444", "01", "2022", "999", "01.01.2015", "1000"])

    def test_append(self):
        self.assertEqual(len(self.collection.container), 2)

    def test_edit(self):
        self.collection.edit_by_id(1, field_name="payer_name", value="LastName")
        res = self.collection.edit_by_id(5, field_name="payer_name", value="LastName")
        self.assertEqual(self.collection.container[0].payer_name, "LastName")
        self.assertEqual(res, None)

    def test_remove(self):
        obj = self.collection.find_by_id(2)
        self.collection.remove_object(obj)
        self.assertEqual(len(self.collection.container), 1)
        self.collection.remove_object(2)
        self.assertEqual(len(self.collection.container), 1)

    def test_remove_by_id(self):
        self.collection.remove_by_id(1)
        self.assertEqual(len(self.collection.container), 1)
        self.collection.remove_by_id(1)
        self.assertEqual(len(self.collection.container), 1)

    def test_get_value(self):
        self.assertEqual(self.collection.get_values("payer_name"), ["Name", "Name"])

    def test_get_data_in_dicts(self):
        self.assertEqual(self.collection.get_data_in_dicts(), [self.collection.container[0].to_dict(),
                                                               self.collection.container[1].to_dict()])

    def test_find_by_id(self):
        self.assertEqual(self.collection.find_by_id(1), self.collection.container[0])

    def test_sort(self):
        self.assertEqual(self.collection.sort(), sorted(self.collection.container))

    def test_print_all(self):
        collection = TransactionCollection()
        self.assertEqual(str(collection), '')