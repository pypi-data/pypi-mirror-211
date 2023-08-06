from unittest import TestCase

from marshaller.cli import main


class MarshallerTests(TestCase):
    def test_main(self):
        self.assertIsNone(main())
