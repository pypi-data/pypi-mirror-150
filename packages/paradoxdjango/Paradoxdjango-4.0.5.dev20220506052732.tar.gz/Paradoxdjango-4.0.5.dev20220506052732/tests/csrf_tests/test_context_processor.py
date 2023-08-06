from paradoxdjango.http import HttpRequest
from paradoxdjango.middleware.csrf import _does_token_match as equivalent_tokens
from paradoxdjango.template.context_processors import csrf
from paradoxdjango.test import SimpleTestCase


class TestContextProcessor(SimpleTestCase):
    def test_force_token_to_string(self):
        request = HttpRequest()
        test_token = "1bcdefghij2bcdefghij3bcdefghij4bcdefghij5bcdefghij6bcdefghijABCD"
        request.META["CSRF_COOKIE"] = test_token
        token = csrf(request).get("csrf_token")
        self.assertTrue(equivalent_tokens(str(token), test_token))
