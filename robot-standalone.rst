.. code:: robotframework
   :class: hidden

   *** Settings ***

   Resource  plone/app/robotframework/server.robot
   Resource  plone/app/robotframework/keywords.robot
   Resource  collective/usermanual/keywords.robot
   Resource  Selenium2Screenshots/keywords.robot

   Suite Setup  Run keywords  Suite Setup  Test Setup
   Suite Teardown  Suite Teardown

   *** Keywords ***

   Suite Setup
       Setup Plone site  plone.app.robotframework.PLONE_ROBOT_TESTING
       Set window size  640  1024

   Test Setup
       Import library  Remote  ${PLONE_URL}/RobotRemote
       Set default language
       Enable autologin as  Manager
       ${user_id} =  Translate  user_id
       ...   default=jane-doe  domain=${DOMAIN}
       ${user_fullname} =  Translate  user_fullname
       ...   default=Jane Doe  domain=${DOMAIN}
       Create user  ${user_id}  Member  fullname=${user_fullname}
       Set autologin username  ${user_id}

   Test Teardown
       Set Zope layer  plone.app.robotframework.PLONE_ROBOT_TESTING
       ZODB TearDown
       ZODB SetUp

   Suite Teardown
       Teardown Plone Site
