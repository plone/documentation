=====================================
Customizing an individual thanks page
=====================================

.. admonition :: Description

    It's not hard to customize the thanks page for an individual form.
    This trick is particularly useful for purposes like adding 'pay now' buttons.

If you can tolerate a little work in the Management Interface, you'll find it very easy to customize the Thanks Page for an individual form.

The steps:


1. Create your form;

2. Bring up the Management Interface; navigate to portal_skins/PloneFormGen;

3. Open the fp_thankspage_view template; push the Customize button; this puts an editable copy of the thanks page template in your custom skin folder.

4. Step back to the Custom folder listing (still in the Management Interface); cut the fp_thankspage_view template;

5. Navigate to your form folder; paste it there.

6. Edit the template to insert your Pay/Donate Now form and button code, or whatever other custom code you might need just for this form.

 .. note::

    Note: If there is already an fp_thankspage_view template in your custom skin folder
    (perhaps because you've already customized the template for the site),
    you'll be cutting and pasting a new copy.
