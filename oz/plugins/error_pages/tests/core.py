from __future__ import absolute_import, division, print_function, with_statement, unicode_literals

import oz.plugins.error_pages
import oz
import unittest
import sys

class Stringable(object):
    def __str__(self):
        return "Hi!"

@oz.test
class ErrorPagesCoreTest(unittest.TestCase):
    def test_get_lines_from_file(self):
        try:
            raise Exception()
        except Exception as e:
            _, _, tback = sys.exc_info()
            filename = tback.tb_frame.f_code.co_filename
            pre_context_lineno, pre_context, context_line, post_context = oz.plugins.error_pages.get_lines_from_file(filename, 2, 7)
            self.assertEqual(pre_context_lineno, 0)
            self.assertEqual(pre_context, ['from __future__ import absolute_import, division, print_function, with_statement, unicode_literals', ''])
            self.assertEqual(context_line, 'import oz.plugins.error_pages')
            self.assertEqual(post_context, ['import oz', 'import unittest', 'import sys', '', 'class Stringable(object):', '    def __str__(self):'])

    def test_get_frames_noerror(self):
        _, _, tback = sys.exc_info()
        frames = oz.plugins.error_pages.get_frames(tback, False)
        self.assertEqual(frames, [])

    def test_get_frames_error(self):
        try:
            raise Exception()
        except Exception as e:
            _, _, tback = sys.exc_info()
            frames = oz.plugins.error_pages.get_frames(tback, False)

            self.assertEqual(len(frames), 1)

            for frame in frames:
                self.assertTrue(isinstance(frame, oz.plugins.error_pages.ErrorFrame))

    def test_get_frames_debug(self):
        try:
            oz.plugins.error_pages.debug()
        except Exception as e:
            _, _, tback = sys.exc_info()
            frames = oz.plugins.error_pages.get_frames(tback, False)

            self.assertEqual(len(frames), 2)

            for frame in frames:
                self.assertTrue(isinstance(frame, oz.plugins.error_pages.ErrorFrame))

    def test_prettify_object(self):
        self.assertEqual(oz.plugins.error_pages.prettify_object(Stringable()), "'Hi!'")