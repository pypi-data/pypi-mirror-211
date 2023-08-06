import unittest

from odoo_env_config import utils


class TestUtils(unittest.TestCase):
    def test_is_true(self):
        self.assertTrue(utils.is_true(str(True)))
        self.assertTrue(utils.is_true(str(1)))

        self.assertTrue(utils.is_true(True))
        self.assertTrue(utils.is_true(1))

        self.assertFalse(utils.is_true(str(False)))
        self.assertFalse(utils.is_true(str(0)))
        self.assertFalse(utils.is_true(str(0.0)))
        self.assertFalse(utils.is_true(str(None)))

        self.assertFalse(utils.is_true(False))
        self.assertFalse(utils.is_true(0))
        self.assertFalse(utils.is_true(0.0))
        self.assertFalse(utils.is_true(1.0))

        self.assertFalse(utils.is_true(object()))
        self.assertFalse(utils.is_true(None))
        self.assertFalse(utils.is_true([]))
        self.assertFalse(utils.is_true([1, 2, 3]))
        self.assertFalse(utils.is_true((1, 2, 3)))
        self.assertFalse(utils.is_true({1, 2, 3}))
        self.assertFalse(utils.is_true({"key": "value"}))

    def test_to_int(self):
        self.assertEqual(0, utils.to_int(str(True)))
        self.assertEqual(0, utils.to_int(True))
        self.assertEqual(1, utils.to_int(str(1)))

        self.assertEqual(1, utils.to_int(1))

        self.assertEqual(0, utils.to_int(str(False)))
        self.assertEqual(0, utils.to_int(str(0)))
        self.assertEqual(0, utils.to_int(str(0.0)))
        self.assertEqual(0, utils.to_int(str(None)))

        self.assertEqual(0, utils.to_int(False))
        self.assertEqual(0, utils.to_int(0))
        self.assertEqual(0, utils.to_int(0.0))
        self.assertEqual(1, utils.to_int(1.0))
        self.assertEqual(0, utils.to_int(object()))
        self.assertEqual(0, utils.to_int(None))

        self.assertEqual(12, utils.to_int(12.5))
        self.assertEqual(13, utils.to_int(str(13.6)))

    def test_add_dash(self):
        self.assertEqual("--my_option", utils.add_dash("my_option"))
        self.assertEqual("-k=value", utils.add_dash("k=value"))
        self.assertEqual("--key=value", utils.add_dash("key=value"))
        self.assertEqual("--key=value", utils.add_dash("--key=value"))
        self.assertEqual("-o", utils.add_dash("-o"))
        self.assertEqual("-i", utils.add_dash("i"))
        self.assertEqual("-u=base", utils.add_dash("-u=base"))
        self.assertEqual("", utils.add_dash(None))
        self.assertEqual("", utils.add_dash(""))
