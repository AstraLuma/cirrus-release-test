def setup_hypothesis():
    from hypothesis import settings, Verbosity

    settings.register_profile("ci", max_examples=1000)
    settings.register_profile("dev", max_examples=10)
    settings.register_profile("debug", max_examples=10, verbosity=Verbosity.verbose)


setup_hypothesis()
