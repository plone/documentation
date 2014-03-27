How to show full content in folder views
========================================

This how-to only makes sense for folders, smart folder, or other similar
views with a reasonably small number of items. It shows how to display
the full view of content in listings by using the macros already defined
for the content types. The same approach can be used to define viewlets
for layout products like compositepack.

I was looking for a layout product for the front page of a site I am
working on, and the existing products did not meet my needs out of the
box because they only showed summary views of content rather than the
full view. Instead of writing viewlets for different content types from
scratch, I used the existing view macros of the content types as
follows, in a new folder view I called folder\_full\_view (this is just
a code snippet):

::

            <tal:listing condition="folderContents">

                    <div tal:repeat="item folderContents">
                    <tal:block tal:define="here item/getObject;
                                           actions nothing;
                                           view here/defaultView;
                                           object_title item/pretty_title_or_id"
                               tal:on-error="nothing">                  
                       <div metal:use-macro="here/?view/macros/main"/>

                    </tal:block>
                    </div>

            </tal:listing>

The setting of actions to nothing is so that the action icons are not
displayed for every content item. The on-error="nothing" may not be
necessary for you. I have it because I allow the catalog to return
results for which there is no View permission.

Similarly, for the CompositePack product, I defined a viewlet

::

    <div class="viewlet default_view">
    <tal:block on-error="nothing"
         tal:define="here nocall: context;
                     actions nothing;
                     view here/defaultView;
                     object_title here/pretty_title_or_id">
      <metal:block use-macro="context/global_defines/macros/defines" />
      <div metal:use-macro="context/?view/macros/main"/>
    </tal:block>
    </div>

so that complete content can be displayed in a layout.

 

Use these ideas at your own risk. Seems to work for me so far.
