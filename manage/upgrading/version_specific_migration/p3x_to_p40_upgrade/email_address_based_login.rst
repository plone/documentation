=========================
Email address-based login
=========================

You can now allow users to use their email address as login name. This feature can be switched on in the Security settings control panel. The effect is that on the registration form no field is shown for the user name. On the login form the user is now asked to fill in an email address. A list of questions and answers about this new feature, including use and migration, is presented here.

When this feature is enabled, can I log in with either my username and my email address or only my email address?
=================================================================================================================

After you enable this feature, new users can only login with their email address.

For existing accounts that were created before enabling this feature, it is slightly different. They need to login once with their username, edit their preferences and save that form. That will update their account info. Now they can logout and then login with their email address.

To prevent this strange situation, as Manager you can add @@migrate-to-emaillogin to the url of your website. In that form you can set the email address as the login name for all existing users. Now all existing users can also login with their email address.

Is this feature enabled by default in new Plone 4 sites? Will it get activated if I migrate to P4 from a previous version?
==========================================================================================================================

No, it is not enabled by default. No, it will not get activated during migration.

How can I activate/deactivate this feature? Are there any possible issues during activation/deactivation I should know about?
=============================================================================================================================

In the Site Setup go to the Security Panel. Check or uncheck the Use email address as login name option and save the form.

Activating this on a website that already has users may be confusing for those users. When logging in they will be asked for their email address, but these existing users should actually still login with the login name they have chosen. They should edit their personal preferences once and save the form and then they can login with their email address.

Also, activating this may give unexpected results when there are two user accounts that have the same email address. At least they will not be able to use their email address for logging in, so they should still use their original login name.

The solution for those two situations, is the @@migrate-to-emaillogin form. Add that to the url of your website. In that form, you can check if any existing users have the same email address. Also, you can set the email address as the login name for all existing users. Now all existing users can immediately login with their email address, without having to edit their preferences.

When you no longer want users to login with their email address, you can use this form to reset their login name to their user id. Note that this has no real effect for users that never had a separate user id to begin with; their email address will remain their user id.

What happens when I change my email address?
============================================

When you change your email address, you can only login with your new address, not your old. Also, for safety no-one can register an account with the email address you initially used.
