==========
Flowplayer
==========

.. admonition :: Description

    Using Flowplayer video player in your Plone add-ons.


Introduction
============

Flowplayer is a GPL'ed Flash-based video player.

Plone integration exists as an add-on product:

* https://plone.org/products/collective-flowplayer

Creating a custom Flowplayer
==============================

Here is a walkthrough how to create a custom content type with a video field
which plays the uploaded video using Flowplayer in a page template with
parameters you define.

Dexterity model definition::

    from plone.namedfile.field import NamedFile, NamedImage

    class IPortletSource(form.Schema):
        """ Portlet source content
        """

        videoFile = NamedFile(
                    title=u"Video file",
                    description=u"Upload video file from local computer to show mini-video-player in the portlet",
                    required=False
                    )

Helper view Python code::

    class MiniVideo(grok.View):
        """ Render a mini Flowplayer (inside portlet)
        """

        grok.context(IPortletSource)

        def hasVideo(self):
            """ Check if plone.namedfile field exist and has a video file uploaded on the context item.
            """

            return self.context.videoFile != None

Helper view template:

.. code-block:: html

    <div class="video" tal:condition="view/hasVideo">

        <!-- The href references the FLV file. It is not safe to use XHTML
            style self-closing tags here. -->
        <tal:video define="video nocall:context/videoFile"
             tal:condition="nocall:video">
                <a class="flow-player" tal:attributes="href string:${context/absolute_url}/@@download/videoFile/${video/filename}">
                </a>
        </tal:video>

        <!-- Helper for JavaScript which is used to determine location of
            Flowplayer resource files -->
        <span class="flowplayer-site-url" style="display:none" tal:content="context/portal_url" />

    </div>

Using the view:

.. code-block:: html

    <div class="portletSimulator">

        <div tal:attributes="class string:ls-portlet ${context/extraCSS}">

          <h3 tal:condition="view/has_title"
              tal:attributes="class string:portletHeader ls-portlet-header">
            <a class="header"
               tal:omit-tag=""
               tal:content="context/title" />
          </h3>

          <div tal:define="videoView nocall:context/@@minivideo"
               tal:replace="structure videoView" />

        </div>

    </div>


JavaScript, registered in ``portal_javascripts``, doing the magic:

.. xxx: In the following, some keys are not quoted (playlist, fullscreen). Is that OK?

.. code-block:: javascript

    /**
     * Bootstrap flow player.
     *
     * Call this when DOM is ready ( jq(document).ready() ).
     */
    function setupPortletVideo() {

        // Site base URL must be available in some hidden variable
        // so that we can build references to our media resources
        var urlBase = jq(".flowplayer-site-url").text();

        console.log("Video set-up:" + urlBase);

        // Iterate through all links which are tagged as video on the page
        // Use a special marker class for videos which we want to configure ourselves
        jq('a.flow-player').each(function() {

            console.log("Found flowplayer");

            var self = jq(this);

            // Config help
            // http://flowplayer.org/documentation/configuration/index.html
            // http://flowplayer.org/documentation/configuration/clips.html#properties
            // Styling properties http://flowplayer.org/documentation/configuration/plugins.html
            var config = {
                    "clip": {
                        "scaling": "orignal",
                        "autoBuffering": true,
                        "autoPlay": false,
                        },

                    "plugins": {
                        // Note that + must be escaped as %2B
                        "audio": {
                            "url": urlBase + "/%2B%2Bresource%2B%2Bcollective.flowplayer/flowplayer.audio.swf" },
                        // Disable control plug-in
                        // On mouse over Play button still appears
                        "controls" : {
                            "url": urlBase + "/%2B%2Bresource%2B%2Bcollective.flowplayer/flowplayer.controls.swf",
                            playlist:false,
                            fullscreen:false,
                            mute:false,
                            time:false,
                            }
                        },

                        // http://flowplayer.org/documentation/configuration/player.html
                        // debug : true,

                    log: {
                        // Enable debug output (lots of it)
                        // level  : 'debug'
                        },

                    }

            config.clip.url = self.attr('href');

            // Create Flowplayer by calling its own JS API
            var player = flowplayer(this,
                   {"src": urlBase + "/++resource++collective.flowplayer/flowplayer.swf"
                   }, config);
        });
    }

    jq(document).ready(setupPortletVideo);

Needed CSS:

.. code-block:: css

    /* Videos */

    a.flow-player {
            display: block;
            width: 235px;
            height: 180px;
    }

.. note::

    if your player is not displayed on the page load, but is displayed
    after you click somewhere to the player container area, be sure
    there is no HTML code nor text inside the player container HTML tag.
    Such code/text is considered as player splash screen and player is
    waiting for click to the splash.

Non-buffered MP4 playback fix
================================

MPEG4 files must be specially prepared (quick play fix),
so that the playback starts instantly and the player does
not try to buffer the whole file first

* https://twitter.com/moo9000/status/253947688276594688
