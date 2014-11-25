Including a pattern from Mockup
===============================

So, you have seen all the patterns already bundled with the mockup project in the `examples page <http://plone.github.io/mockup/dev/#pattern>`_ and you want to use one (or several). You'll find this incredible easy.

We will be assuming you have created your project using the instructions from the previous chapter. If not, then adjust your variables and file names accordingly.


Assume the following HTML
-------------------------

This step is not really needed in order to include a dependency, we will use it just as an example.
Let's say you have the following HTML:

.. code-block:: html

    <table border="1" style="text-align:center;">
        <thead>
            <tr>
                <th>Name</th>
                <th>Surname</th>
                <th>Arbitrary Number</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Linus</td>
                <td>Torvalds</td>
                <td>4</td>
            </tr>
            <tr>
                <td>Ada</td>
                <td>Lovelace</td>
                <td>1</td>
            </tr>
            <tr>
                <td>Alan</td>
                <td>Turing</td>
                <td>3</td>
            </tr>
            <tr>
                <td>Dennis</td>
                <td>Ritchie</td>
                <td>2</td>
            </tr>
            <tr>
                <td>Richard</td>
                <td>Stallman</td>
                <td>5</td>
            </tr>
        </tbody>
    </table>

You can include this in your ``dev/dev.html`` file from your project. Now, if you open it using your web browser, you will notice you have a basic table with no functionality whatsoever. But we want to be able to sort its content by clicking the titles.


Pick the pattern to use
-----------------------

For this exercise, we will pick the `Table Sorter <http://plone.github.io/mockup/dev/#pattern/tablesorter>`_ pattern. To use it, we need to add the special css class ``pat-tablesorter`` to the HTML snippet we have, so replace:

.. code-block:: html

    <table border="1" style="text-align:center;">

with:

.. code-block:: html

    <table border="1" style="text-align:center;" class="pat-tablesorter">

Be aware that you can include several classes at the same time, as you would normally do. That doesn't affect mockup functionality.
Now refresh your browser. You will see that nothing has changed, and you still cannot order your table. Don't despair. Inside your project folder, look for the ``config.js``. This is the file where all dependencies are listed. We see that Table Sorter pattern 'internal name' is 'mockup-patterns-tablesorter'.


Include the dependency in your bundle
-------------------------------------

Now that we know the internal name for the pattern we want to use, let's include it in our bundle. Go to your project directory, and open ``js/bundles/myproject.js``. You will notice a section as follows:

.. code-block:: js

    define([
        'jquery',
        'mockup-registry',
        'mockup-patterns-base',
        //   Uncomment the line below to include all patterns from plone-mockup
        //   'mockup-bundles-widgets',
        //   <!~~ Add patterns below this line ~~!>
        'myproject-patterns-mypattern'
    ], function($, Registry, Base) {
        'use strict';

Just edit this list, and include our dependency.
Friendly reminder: Be aware that this is a Javascript list, and as such it should NOT include a comma at the end of the last item.

That section should now look as follows:

.. code-block:: js

    define([
        'jquery',
        'mockup-registry',
        'mockup-patterns-base',
        //   Uncomment the line below to include all patterns from plone-mockup
        //   'mockup-bundles-widgets',
        //   <!~~ Add patterns below this line ~~!>
        'mockup-patterns-tablesorter',
        'myproject-patterns-mypattern'
    ], function($, Registry, Base) {
        'use strict';

That's it, now refresh again... you should be able to sort your table by clicking the column headers. If you now run ``make``, Table sorter will be included in the compiled Javascript file.


Include a pattern with style dependencies
-----------------------------------------

We have seen a very basic example of a small pattern that doesn't need much. Let's try again, but now we will include the `Autotoc <http://plone.github.io/mockup/dev/#pattern/autotoc>`_ pattern.


Consider the following HTML
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: html

    <div>
        <h1>Title 1</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ultrices <br/> tempus purus vel condimentum. Nulla in tortor <br/> sit amet ex tincidunt gravida ut eget ante. </p>
        <h2>Title 1.1</h2>
        <p>Aenean suscipit ligula nibh, vel congue dui mattis vel.<br/>  Phasellus ut nulla eget nisi vehicula sodales nec non turpis. Phasellus non mi eu sapien <br/> scelerisque ornare et id dolor. Aenean tempus egestas purus, nec tempor ligula. Donec at lorem dolor. <br/> Vestibulum vitae lacus nec nibh <br/> volutpat malesuada</p>
        <h3>Title 1.1.1</h3>
        <p>Phasellus interdum <br/> interdum nisi eu sagittis. Ut hendrerit feugiat <br/> nisl auctor venenatis. Praesent aliquam ipsum <br/> nec mollis congue. Quisque eu mollis nisl.</p>
        <h2>Title 1.2</h2>
        <p>Fusce posuere turpis a lacus laoreet, in <br/> blandit mauris vehicula. Cras mattis vitae ex eu scelerisque. <br/> Donec ut nibh tortor. In pharetra arcu eget sollicitudin tempus. Nunc condimentum ex vel massa fringilla iaculis. <br/> In scelerisque sit amet justo sed suscipit. Quisque vel <br/> tincidunt risus, sit amet laoreet enim.</p>
        <h1>Title 2</h1>
        <p>Sed vel tellus et <br/> ligula aliquet volutpat eget nec ante. Nulla eu pretium est. <br/> Morbi ac vulputate massa. Vivamus condimentum mauris non justo sodales, at sollicitudin tortor tempor. <br/> Quisque rutrum diam cursus orci facilisis pharetra. <br/> Pellentesque ante ex, commodo nec massa ac, ullamcorper hendrerit turpis. Mauris id nisl <br/> semper, aliquam risus et, gravida diam. <br/> Proin et lorem risus.</p>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    </div>

We will now try to use the "Autotoc" pattern, so again, we search for its internal name in the ``config.js`` file, and include it as dependency in our bundle. So replace:

.. code-block:: js

    define([
        'jquery',
        'mockup-registry',
        'mockup-patterns-base',
        //   Uncomment the line below to include all patterns from plone-mockup
        //   'mockup-bundles-widgets',
        //   <!~~ Add patterns below this line ~~!>
        'mockup-patterns-tablesorter',
        'myproject-patterns-mypattern'
    ], function($, Registry, Base) {
        'use strict';

With:

.. code-block:: js

    define([
        'jquery',
        'mockup-registry',
        'mockup-patterns-base',
        //   Uncomment the line below to include all patterns from plone-mockup
        //   'mockup-bundles-widgets',
        //   <!~~ Add patterns below this line ~~!>
        'mockup-patterns-tablesorter',
        'mockup-patterns-autotoc',
        'myproject-patterns-mypattern'
    ], function($, Registry, Base) {
        'use strict';

And add the proper class to the outer div of our example, so it will look like this:

.. code-block:: html

    <div class="pat-autotoc">
        <h1>Title 1</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ultrices <br/> tempus purus vel condimentum. Nulla in tortor <br/> sit amet ex tincidunt gravida ut eget ante. </p>
        <h2>Title 1.1</h2>
        <p>Aenean suscipit ligula nibh, vel congue dui mattis vel.<br/>  Phasellus ut nulla eget nisi vehicula sodales nec non turpis. Phasellus non mi eu sapien <br/> scelerisque ornare et id dolor. Aenean tempus egestas purus, nec tempor ligula. Donec at lorem dolor. <br/> Vestibulum vitae lacus nec nibh <br/> volutpat malesuada</p>
        <h3>Title 1.1.1</h3>
        <p>Phasellus interdum <br/> interdum nisi eu sagittis. Ut hendrerit feugiat <br/> nisl auctor venenatis. Praesent aliquam ipsum <br/> nec mollis congue. Quisque eu mollis nisl.</p>
        <h2>Title 1.2</h2>
        <p>Fusce posuere turpis a lacus laoreet, in <br/> blandit mauris vehicula. Cras mattis vitae ex eu scelerisque. <br/> Donec ut nibh tortor. In pharetra arcu eget sollicitudin tempus. Nunc condimentum ex vel massa fringilla iaculis. <br/> In scelerisque sit amet justo sed suscipit. Quisque vel <br/> tincidunt risus, sit amet laoreet enim.</p>
        <h1>Title 2</h1>
        <p>Sed vel tellus et <br/> ligula aliquet volutpat eget nec ante. Nulla eu pretium est. <br/> Morbi ac vulputate massa. Vivamus condimentum mauris non justo sodales, at sollicitudin tortor tempor. <br/> Quisque rutrum diam cursus orci facilisis pharetra. <br/> Pellentesque ante ex, commodo nec massa ac, ullamcorper hendrerit turpis. Mauris id nisl <br/> semper, aliquam risus et, gravida diam. <br/> Proin et lorem risus.</p>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    </div>

After refreshing your browser, you can see that the TOC has been generated, but is missing the styling.


Include less
~~~~~~~~~~~~

Open ``less/myproject.less`` file and add this line to the end of it:

.. code-block:: css

    @import "../bower_components/plone-mockup/patterns/autotoc/pattern.autotoc.less";

Now refresh again, and you will see your TOC has a default styling applied.


Configure the pattern
~~~~~~~~~~~~~~~~~~~~~

As a final exercise, this pattern allows configuration to be passed from the HTML, so let's make the duration of the movement to be fast and to only include h1 and h2 in the TOC:

.. code-block:: html

    <div class="pat-autotoc" data-pat-autotoc="scrollDuration:fast;levels:h1,h2;">
        <h1>Title 1</h1>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla ultrices <br/> tempus purus vel condimentum. Nulla in tortor <br/> sit amet ex tincidunt gravida ut eget ante. </p>
        <h2>Title 1.1</h2>
        <p>Aenean suscipit ligula nibh, vel congue dui mattis vel.<br/>  Phasellus ut nulla eget nisi vehicula sodales nec non turpis. Phasellus non mi eu sapien <br/> scelerisque ornare et id dolor. Aenean tempus egestas purus, nec tempor ligula. Donec at lorem dolor. <br/> Vestibulum vitae lacus nec nibh <br/> volutpat malesuada</p>
        <h3>Title 1.1.1</h3>
        <p>Phasellus interdum <br/> interdum nisi eu sagittis. Ut hendrerit feugiat <br/> nisl auctor venenatis. Praesent aliquam ipsum <br/> nec mollis congue. Quisque eu mollis nisl.</p>
        <h2>Title 1.2</h2>
        <p>Fusce posuere turpis a lacus laoreet, in <br/> blandit mauris vehicula. Cras mattis vitae ex eu scelerisque. <br/> Donec ut nibh tortor. In pharetra arcu eget sollicitudin tempus. Nunc condimentum ex vel massa fringilla iaculis. <br/> In scelerisque sit amet justo sed suscipit. Quisque vel <br/> tincidunt risus, sit amet laoreet enim.</p>
        <h1>Title 2</h1>
        <p>Sed vel tellus et <br/> ligula aliquet volutpat eget nec ante. Nulla eu pretium est. <br/> Morbi ac vulputate massa. Vivamus condimentum mauris non justo sodales, at sollicitudin tortor tempor. <br/> Quisque rutrum diam cursus orci facilisis pharetra. <br/> Pellentesque ante ex, commodo nec massa ac, ullamcorper hendrerit turpis. Mauris id nisl <br/> semper, aliquam risus et, gravida diam. <br/> Proin et lorem risus.</p>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
    </div>
