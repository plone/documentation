.. code:: robotframework
   :class: hidden

   *** Settings ***

   Resource  plone/app/robotframework/server.robot
   Resource  plone/app/robotframework/keywords.robot
   Resource  collective/usermanual/keywords.robot
   Resource  Selenium2Screenshots/keywords.robot

   Library  OperatingSystem
   Library  Remote  ${PLONE_URL}/RobotRemote

   Suite Setup  Run keywords  Suite Setup  Test Setup
   Suite Teardown  Run keywords  Test Teardown  Suite Teardown

   *** Keywords ***

   Suite Setup
       ${language} =  Get environment variable  LANGUAGE  'en'
       Set default language  ${language}
       Open test browser
       Set window size  640  1024

    Test Setup
       Remote ZODB SetUp
       ...  plone.app.robotframework.PLONE_ROBOT_TESTING

       Enable autologin as  Manager
       ${user_id} =  Translate  user_id
       ...  default=jane-doe  domain=${DOMAIN}
       ${user_fullname} =  Translate  user_fullname
       ...  default=Jane Doe  domain=${DOMAIN}
       Create user  ${user_id}  Member  fullname=${user_fullname}
       Set autologin username  ${user_id}

   Test Teardown
       Remote ZODB TearDown
       ...  plone.app.robotframework.PLONE_ROBOT_TESTING

   Suite Teardown
       Close all browsers
