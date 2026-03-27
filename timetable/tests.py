from django.test import TestCase, override_settings
from django.urls import reverse

class VisualTimetablingToggleTests(TestCase):
    @override_settings(VISUAL_TIMETABLING_ENABLED=True, VISUAL_TIMETABLING_URL='https://example.com/')
    def test_visual_tool_enabled(self):
        resp = self.client.get(reverse('visual_tool'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Visual Tool')
        self.assertContains(resp, 'iframe')

    @override_settings(VISUAL_TIMETABLING_ENABLED=False)
    def test_visual_tool_disabled(self):
        resp = self.client.get(reverse('visual_tool'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "désactivée")

