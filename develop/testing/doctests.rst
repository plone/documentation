=========
Doctests
=========

Doctests are way to do tests with interactive Python interpreter.

* https://plone.org/documentation/tutorial/testing/doctests

Doctests and pdb
----------------

Python debugger (pdb) works little differently when invoked from doctests.

Your locals stack frame is not what you might expect and refers to doctests internals::

	(Pdb) locals()
	{'__return__': None, 'self': <zope.testing.doctest._OutputRedirectingPdb instance at 0x5a7c8f0>}

Corrective action is to go one level up in the stack::

	(Pdb) up
	> /Users/moo/mmaspecial/src/Products.PloneGetPaid/Products/PloneGetPaid/notifications.py(22)__call__()
	-> import pdb ; pdb.seT_trace()
	(Pdb) locals()
	{'settings': <Products.PloneGetPaid.preferences.StoreSettings object at 0x5f631b0>, 'store_url': 'http://nohost/plone', 'self': <Products.PloneGetPaid.notifications.MerchantOrderNotificationMessage object at 0x56c30d0>, 'order_contents': u'11 pz @84.00 total: US$924.00\n22 ph @59.00 total: US$1298.00\n12 pf @98.00 total: US$1176.00\n23 pX @95.00 total: US$2185.00\n3 pM @89.00 total: US$267.00\n22 po @60.00 total: US$1320.00\n23 pj @39.00 total: US$897.00\n15 po @34.00 total: US$510.00\n5 pS @76.00 total: US$380.00\n1 pm @70.00 total: US$70.00', 'template': u'To: ${to_email}\nFrom: "${from_name}" <${from_email}>\nSubject: New Order Notification\n\nA New Order has been created\n\nTotal Cost: ${total_price}\n\nTo continue processing the order follow this link:\n${store_url}/@@admin-manage-order/${order_id}/@@admin\n\nOrder Contents\n\n${order_contents}\n\nShipping Cost: ${shipping_cost}\n\n', 'pdb': <module 'pdb' from '/Users/moo/code/python-macosx/parts/opt/lib/python2.4/pdb.pyc'>}
	(Pdb)


Interlude
---------

Interlude is a Python package, which you can use to start an interactive Python
shell from doctests, bypassing the limitations described above.

Just depend on 'interlude' and pass it via the globs dict to the doctest or
import it from there::

    >>> from interlude import interac
    >>> interact(locals())

When the testrunner passes interact, you'll get an interactive Python prompt.

For more information see: https://pypi.python.org/pypi/interlude


Get fields from browser
-----------------------

The most common operation when using a doctest is filling fields of a form::

    >>> browser.getControl(name='form.widgets.text').value = 'Some text'

One common problem with this is that you can get an ``LookupError: name ...``.
If there is a typo, or the field does not exist, etc etc.

A quick way to see which fields exist on the current browser helps a lot while debugging test failures::

    >>> [[c.name for c in f.controls] for f in browser.mech_browser.forms()]
