import unittest

from kubeshift.queries import utils


class TestQueryUtils(unittest.TestCase):

    def test_invalid_selector_inputs(self):
        self.assertIsNone(utils.selectors_to_qs(None))
        self.assertIsNone(utils.selectors_to_qs({}))
        self.assertIsNone(utils.selectors_to_qs(''))

    def test_empty_selector_inputs(self):
        self.assertIsNone(utils.selectors_to_qs([]))

    def test_selector_missing_key(self):
        self.assertIsNone(utils.selectors_to_qs([{}]))

    def test_selector_unknown_op(self):
        self.assertIsNone(utils.selectors_to_qs([{'key': 'name', 'op': 'x'}]))

    def test_selector_exists(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name'}]),
            '?labelSelector=name'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '='}]),
            '?labelSelector=name'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '=='}]),
            '?labelSelector=name'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': 'in'}]),
            '?labelSelector=name'
        )

    def test_selector_not_exists(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '!='}]),
            '?labelSelector=%21name'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': 'notin'}]),
            '?labelSelector=%21name'
        )

    def test_selector_equality(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'value': 'testapp'}]),
            '?labelSelector=name+in+%28testapp%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '=', 'value': 'testapp'}]),
            '?labelSelector=name+in+%28testapp%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '==', 'value': 'testapp'}]),
            '?labelSelector=name+in+%28testapp%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': 'in', 'value': 'testapp'}]),
            '?labelSelector=name+in+%28testapp%29'
        )

    def test_selector_oneof_equality(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+in+%28proxy%2Cweb%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': '=', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+in+%28proxy%2Cweb%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': '==', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+in+%28proxy%2Cweb%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': 'in', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+in+%28proxy%2Cweb%29'
        )

    def test_selector_inequality(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': '!=', 'value': 'testapp'}]),
            '?labelSelector=name+notin+%28testapp%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'name', 'op': 'notin', 'value': 'testapp'}]),
            '?labelSelector=name+notin+%28testapp%29'
        )

    def test_selector_oneof_inequality(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': '!=', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+notin+%28proxy%2Cweb%29'
        )

        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': 'notin', 'value': ['proxy', 'web']}]),
            '?labelSelector=tier+notin+%28proxy%2Cweb%29'
        )

    def test_selector_multiple_inputs(self):
        self.assertEqual(
            utils.selectors_to_qs([{'key': 'tier', 'op': '=', 'value': ['proxy', 'web']},
                                   {'key': 'name', 'op': '!=', 'value': 'testapp'}]),
            '?labelSelector=tier+in+%28proxy%2Cweb%29%2Cname+notin+%28testapp%29'
        )
