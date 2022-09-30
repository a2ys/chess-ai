import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        import main

        a = main.Main()
        mainloop = a.mainloop()

        self.assertEqual(a.mainloop(), 0)


if __name__ == '__main__':
    unittest.main()
