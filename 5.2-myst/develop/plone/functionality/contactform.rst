=============
Contact forms
=============



Introduction
------------

Plone ships with a

* site contact form which is form-to-mail to the site administration email

* document comment form

* email this to friend form

Default address /contact-info.

Customizing site contact form
------------------------------

Contact form files are

* Products/CMFPlone/skins/plone_templates/contact-info.cpt

* Products/CMFPlone/skins/plone_templates/contact-info.cpt.metadata

* Products/CMFPlone/skins/plone_templates/site_feedback_template.pt

* Products/CMFPlone/skins/plone_formscripts/validate_feedback.vpy

* Products/CMFPlone/skins/plone_formscripts/send_feedback.cpy

* Products/CMFPlone/skins/plone_formscripts/send_feedback.cpy.metadata

* Products/CMFPlone/skins/plone_formscripts/send_feedback_site.cpy

* Products/CMFPlone/skins/plone_formscripts/send_feedback_site.cpy.metadata

Inspect the files to known which you need to change.
Copy these files to skin layer folder (any folder under skins) in your add-on product.

.. note::

        Different contact for is displayed for logged-in and anonymous users.
        Logged in user email is not asked, but one stored in member properties is used.

Example
=======

Below is an example how to add "phone number" field for all *not logged in* users
feedback form.

Add a new optional field to contact-info.cpt (language hardcoded)::

        <div class="field">

          <label for="phone_number">
            Puhelinnumero
          </label>

          <div class="formHelp">
            Puhelinnumero, mik&#xe4;li haluatte teihin oltavan yhteydess&#xe4; puhelimitse.
          </div>

          <input type="text"
                 id="phone_number"
                 name="phone_number"
                 size="25"
                 value=""
                 tal:attributes="value request/phone_number|nothing"
                 />
        </div>

Refer this field in site_feedback_template.pt::

        <div i18n:domain="plone"
             tal:omit-tag=""
             tal:define="utool nocall:here/portal_url;
                         portal utool/getPortalObject;
                         charset portal/email_charset|string:utf-8;
                         dummy python:request.RESPONSE.setHeader('Content-Type', 'text/plain;;charset=%s' % charset);"
        >

        <div i18n:translate="site_feedback_mailtemplate_body" tal:omit-tag="">

        You are receiving this mail because <span i18n:name="fullname" tal:omit-tag="" tal:content="options/sender_fullname|nothing" />
        <span i18n:name="from_address" tal:omit-tag="" tal:content="options/sender_from_address"/>
        is sending feedback about the site administered by you at <span i18n:name="url" tal:replace="options/url" />.
        The message sent was:

        <span i18n:name="message" tal:omit-tag="" tal:content="options/message | nothing" />

        </div>
        --
        <span tal:replace="portal/email_from_name" />

        </div>

        Puhelinnumero: <span tal:content="request/phone_number|nothing" />


.. note::

   As a crude hack we add new field to the very bottom of the email, as everything side <div i18n:translate>
   is replaced from translation catalogs.

Replacing the site contact form with a content object
-----------------------------------------------------

Sometimes you want to turn off the builtin form in favour of a piece
of content. For example you might want a PloneFormGen form that
content editors can alter. Naming your content item ``contact-info``
works because Zope traversal will find your content item before the
page template. However Plone won't allow a new piece of content to be
named ``contact-info`` since that's a reserved identifier, so the
trick is to rename it in the Management Interface from the Plone-generated
``contact-info-1`` back to ``contact-info``.

This works for ``accessibility-info`` too.

If you have a PFG contact form at, say, ``about/contact-us`` and want
to turn off the builtin ``contact-info`` form, use the rename trick to
create a ``contact-info`` Link object at the site root that points to
your new form. Through acquisition, even URLS like
``events/contact-info`` will successfully redirect to your custom
form.
