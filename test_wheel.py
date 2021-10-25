import unittest

class TestWheel(unittest.TestCase):
    def test_import(self):
        try:
            import pyroscope_io as pyro
        except ImportError:
            self.fail("Unable to import pyroscope_io")

    def test_content(self):
        expected_functions = ["build_summary", "change_name", "configure", "remove_tags", "stop", "tag", "tag_wrapper", "test_logger"]
        import pyroscope_io as pyro
        content = dir(pyro)
        for item in expected_functions:
            self.assertIn(item, content)

    def test_build_summary(self):
        import pyroscope_io as pyro
        summary = pyro.build_summary().lower()
        self.assertIn("goarch", summary)
        self.assertIn("goos", summary)
        self.assertIn("go version", summary)
