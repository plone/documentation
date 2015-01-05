==============================
Deprecated Templates Checklist
==============================

A number of the templates in plone_deprecated have now been removed completely.
If your theme or product has customized these, you will need to replace them with the corresponding viewlet or portlet.

+----------------------------------------------+----------------------------------------+-----------------+
| Deprecated template                          | Replacement in Plone 4                 | Type            |
+----------------------------------------------+----------------------------------------+-----------------+
| colophon.pt                                  | plone.colophon                         | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| document_actions.pt                          | plone.documentactions                  | viewletmanager  |
+----------------------------------------------+----------------------------------------+-----------------+
| document_byline.pt                           | plone.belowcontenttitle.documentbyline | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| footer.pt                                    | plone.footer                           | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| global_contentviews.pt                       | plone.contentviews                     | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| global_pathbar.pt                            | plone.path_bar                         | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| global_personalbar.pt                        | plone.personal_bar                     | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| global_searchbox.pt                          | plone.searchbox                        | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| global_sections.pt                           | plone.global_sections                  | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_calendar.pt                          | portlets.Calendar                      | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_events.pt                            | portlets.Events                        | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_languages.pt                         | portlets.Language                      | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_login.pt                             | portlets.Login                         | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_navigation.pt                        | portlets.Navigation                    | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_news.pt                              | portlets.News                          | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_recent.pt                            | portlets.Recent                        | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_related.pt                           | plone.belowcontentbody.relateditems    | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| portlet_review.pt                            | portlets.Review                        | portlet         |
+----------------------------------------------+----------------------------------------+-----------------+
| review_history.pt                            | plone.belowcontentbody.contenthistory  | viewlet         |
+----------------------------------------------+----------------------------------------+-----------------+

For more info about how the viewlet architecture replaced METAL macros check the `Customizing the viewlets in main_template <https://plone.org/documentation/kb/customizing-main-template-viewlets/>`_ tutorial.

For an overview of the Plone portlets infrastucture, see the :doc:`Portlets </develop/plone/functionality/portlets>` section of the Developer Manual.
