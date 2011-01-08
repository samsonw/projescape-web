from projescapeweb.tests import *

class TestPortalController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='portal', action='index'))
        # Test response...
