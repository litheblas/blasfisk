from django.test.simple import DjangoTestSuiteRunner
from django.conf import settings

class IncludeAppsTestSuiteRunner(DjangoTestSuiteRunner):
    """Override the default django 'test' command, exclude from testing
    apps which we know will fail."""

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if not test_labels:
            # No appnames specified on the command line, so we run all
            # tests, but remove those which we know are troublesome.

            test_labels = [app for app in settings.APPS_TO_TEST]
        return super(IncludeAppsTestSuiteRunner, self).run_tests(
                                      test_labels, extra_tests, **kwargs)