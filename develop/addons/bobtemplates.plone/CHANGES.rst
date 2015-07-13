Changelog
=========

0.11 (unreleased)
-----------------

- Move badges from pypin to shields.io.
  [timo]

- Fix coverage on travis template
  [gil-cano]

- Enable code analysis on travis and fail if the code does not pass.
  [gforcada]


0.10 (2015-06-15)
-----------------

- Add check-readme script that detects Restructured Text issues.
  [timo]

- Use only version up to minor version in setup.py of package #56
  [tomgross]

- Use class method to load ZCML in tests
  [tomgross]

- Upgrade default Plone version to 4.3.6.
  [timo]

- Add zest.releaser to package buildout.
  [timo]

- Update README according to Plone docs best practice.
  [do3cc, timo]

- Add flake8-extensions to code-analysis.
  [timo]

- Upgrade Selenium to 2.46.0.
  [timo, pbauer]

- Don't create a type-schema unless it is needed.
  [pbauer]


0.9 (2015-03-24)
----------------

- Add Theme package type with simple bootstrap-based theme.
  [timo]

- Add Dexterity package type.
  [timo]

- Remove example view.
  [timo]

- Remove question for keywords.
  [timo]

- Remove question for locales.
  [timo]

- Remove questions for version and license.
  [timo]

- Remove questions for profile, setuphandler, and testing.
  [timo]

- Unify buildout configuration in buildout.cfg
  [timo]

- Fix bootstrap command in travis.yml.
  [timo]


0.8 (2015-02-06)
----------------

- Add includeDependencies. This fixes #23.
  [timo]


0.7 (2015-02-05)
----------------

- Use latest buildout-bootstrap.py.
  [timo]

- Fix failing nosetests.
  [timo]

- Add test that creates an add_on and runs all its tests and code analysis.
  [timo]

- Run tests on travis.
  [timo]

- Run code analysis on travis. Build fails on PEP8 violations.
  [timo]

- Add code analysis.
  [timo]

- Remove z2.InstallProducts. Not needed any longer.
  [timo]

- Use testing best practices and follow common naming conventions.
  [timo]

- Remove testing profile. Global testing state is considered an anti-pattern.
  [timo]

- Add example robot test.
  [timo]

- Add travis and pypip.in badges.
  [timo]

- Run code analysis on the generated addon as well within the tests to make
  sure we always ship 100% PEP8 compliant code.
  [timo]

- Add REMOTE_LIBRARY_BUNDLE_FIXTURE to acceptance test fixture.
  [timo]


0.6 (2015-01-17)
----------------

- Use PLONE_APP_CONTENTTYPES_FIXTURE for tests on when using Plone 5.
  [pbauer]


0.5 (2015-01-17)
----------------

- Remove useless base-classes for tests. Use 'layer = xxx' instead.
  [pbauer]

- Fix some minor code-analysis issues.
  [pbauer]

- Added .editorconfig file.
  [ale-rt]


0.4 (2014-12-08)
----------------

- Remove grok.
  [pbauer]

- Fix missed removals when testing was deselected.
  [pbauer]

- Only use jbot when there is a profile and a browser layer.
  [pbauer]

- Get username and email from git.
  [do3cc]


0.3 (2014-12-07)
----------------

- Pinn robotframework to 2.8.4 to fix package-tests.
  [pbauer]

- Add browserlayer to demoview to allow multiple addons.
  [pbauer]

- Fix creation of nested packages (wrong __init__.py).
  [pbauer]


0.2 (2014-12-07)
----------------

- Fix documentation
  [pbauer]


0.1 (2014-12-07)
----------------

- Get namespace, name and type from target-dir.
  [pbauer]

- Remove obsolete plone_addon_nested. Auto-nest package in after-render hook.
  [pbauer]

- Add many new features. Most of them are optional.
  [pbauer]

- Initial import based on bobtemplates.ecreall by
  cedricmessiant, vincentfretin and thomasdesvenain.
  [pbauer]
