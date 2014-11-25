Creating your first pattern
===========================

Now that you have generated your first package, we will be creating a pattern.
The generator already creates the boilerplate for a pattern and the needed bits to use it, so we will be just adding code to it.


Write the pattern
-----------------

Open the ``js/patterns/mypattern.js`` file. Its sections are already commented:

.. code-block:: js

    define([
        'jquery',
        'mockup-patterns-base'
    ], function($, Base) {
        'use strict';

    var mypatternPattern = Base.extend({
        // The name for this pattern
        name: 'mypattern',

        defaults: {
            // Default values for attributes
        },

        init: function() {
            // The init code for your pattern goes here
            var self = this;
            // self.$el contains the html element
            self.$el.append('<p>Your Pattern "' + self.name + '" works!</p>');
        }
    });

    return mypatternPattern;

    });


See it in action
----------------

There are two ways of seeing the pattern through the web:

1) Open it in a browser
~~~~~~~~~~~~~~~~~~~~~~~

The best way to understand how all this works is to see it working. Open ``dev/dev.html`` in your browser

WARNING: Working locally will make the browser to complain with::

    XMLHttpRequest cannot load ... Cross origin requests are only supported for HTTP.

This is a security feature. To go around it in Chrome, you need to start it with a ``--disable-web-security`` parameter


2) Use Python's SimpleHTTPServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the project root, start Python's SimpleHTTPServer like so:

.. code-block:: bash

    $ python -m SimpleHTTPServer 8000

And open your web browser pointing to http://localhost:8000/dev/dev.html


Now, after this, you should see the message ``Your Pattern "mypattern" works!``. This is because the pattern we have just created does this in its ``init`` class ( ``self.$el.append('<p>Your Pattern "' + self.name + '" works!</p>');`` ) where, ``self.$el`` is the HTML element which loads the pattern.

Let's make something interesting
--------------------------------

Add some HTML
~~~~~~~~~~~~~

Open ``dev/dev.html`` file in your editor and replace:

.. code-block:: html

    <div class="pat-mypattern">
    </div>

with:

.. code-block:: html

    <div class="pat-mypattern">
        <p class="target">This will get a background color</p>
        <button class="trigger">Press me!</button>
    </div>


Add some CSS
~~~~~~~~~~~~

Open ``less/myproject.less`` file in your editor and add:

.. code-block:: css

    .red-background {
        background-color: red;
    }

    .blue-background {
        background-color: blue;
    }


Write your pattern
~~~~~~~~~~~~~~~~~~

Open ``js/patterns/mypattern.js`` file and replace everything with:

.. code-block:: js

    define([
        'jquery',
        'mockup-patterns-base'
    ], function($, Base) {
        'use strict';

    var mypatternPattern = Base.extend({
        name: 'mypattern',

        defaults: {
            initial_color: 'red'
        },

        change_color: function ($this) {
            var self = this;
            self.$el.find('p.target').removeClass(self.$current_color+'-background');
            if ( self.$current_color === 'red' ){
                self.$current_color = 'blue';
            }
            else {
                self.$current_color = 'red';
            }
            self.$el.find('p.target').addClass(self.$current_color+'-background');
        },

        init: function() {
            var self = this;
            self.$el.find('button.trigger').on('click', function(e) {
                self.change_color();
            });
            self.$current_color = self.options.initial_color;
            self.$el.find('p.target').addClass(self.$current_color+'-background');
        }
    });

    return mypatternPattern;

    });

So, let's explain what the things are that we added:

- We modified the ``init`` method, so:

    1. It will subscribe to an event when pressing the button to call the ``change_color`` method
    2. It will get the default value of ``initial_color``, defined in ``defaults`` and save it in an internal variable
    3. We assign the class to the <p> element

- We defined a default initial ``red`` value for the ``initial_color``. More on this later.

- We created a new method, called ``change_color`` that will change from ``red`` to ``blue`` and back.

Now, if you refresh your browser, the paragraph should have a red background, but when pressing the button, it switches to blue, and then back to red when pressed again.


Defining initial default values
-------------------------------

As we saw before, we defined an ``initial_color`` variable under ``defaults`` in our pattern. Variables defined here are the ones that we are going to be able to modify with data attributes from our HTML, so if you plan on developing a reusable pattern that you can use in several ways, this is the way to do it.

In our example, if we change our HTML as follows:

.. code-block:: html

    <div class="pat-mypattern" data-pat-mypattern="initial_color:blue;">
        <p id="target">This will get a background color</p>
        <button id="trigger">Press me!</button>
    </div>

Then, instead of our paragraph starting as ``red``, it will first be ``blue`` and change to red when first pressing the button.

As you can see, all default variables defined under ``defaults`` will be available under ``self.options``


Isolation
---------

One great thing about patterns is that they only affect the HTML code where they were applied. For this, you should always work with the ``self.$el`` element, as we did in our example.
In order to understand this idea better, open your ``dev/dev.html`` file again, and replace:

.. code-block:: html

    <div class="pat-mypattern">
        <p class="target">This will get a background color</p>
        <button class="trigger">Press me!</button>
    </div>

With:

.. code-block:: html

    <div class="pat-mypattern">
        <p class="target">This will start with a red background color</p>
        <button class="trigger">Press me!</button>
    </div>

    <div>
        <p class="target">This will get no background color</p>
        <button class="trigger">Press me!</button>
    </div>

    <div class="pat-mypattern" data-pat-mypattern="initial_color:blue;">
        <p class="target">This will start with a blue background color</p>
        <button class="trigger">Press me!</button>
    </div>


If you now refresh your browser, you'll see that even though we did no changes to the javascript code, and just by defining some classes and data attributes, we can change the functionality, but have it be specific to a portion of the HTML.

