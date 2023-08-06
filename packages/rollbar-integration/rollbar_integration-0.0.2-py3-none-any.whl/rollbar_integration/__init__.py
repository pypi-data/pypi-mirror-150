import os

# rollbar configuration and setup
if os.getenv('ROLLBAR_TOKEN'):
    import sys
    import rollbar

    rollbar.init(os.getenv('ROLLBAR_TOKEN'))


    def rollbar_except_hook(exc_type, exc_value, traceback):
        # Report the issue to rollbar here.
        rollbar.report_exc_info((exc_type, exc_value, traceback))
        # display the error as normal here
        sys.__excepthook__(exc_type, exc_value, traceback)


    sys.excepthook = rollbar_except_hook
