===============
Quick Reference
===============

.. contents :: :local:

.. admonition:: Description

    A quick reference sheet.

.. TODO:: UPDATE!

Complete list of the field types including their default settings
=================================================================

string -- StringField

- StringField
- searchable=1

text -- TextField

- StringField
- searchable=1
- TextAreaWidget()

richtext -- TextField

- TextField
- default_output_type=text/html
- allowed_content_types=('text/plain','text/structured','text/html','application/msword',)

selection -- StringField with SelectionWidget

- StringField

multiselection -- LinesField with SelctionWidget

- LinesField
- multiValued=1

integer -- IntegerField

- IntegerField
- searchable=1

float -- Floatfield

- FloatField
- searchable=1
- DecimalWidget()

boolean -- BoleanField

- BooleanField
- searchable=1

lines -- LinesField

- LinesField
- searchable=1

date -- DateTimeField

- DateTimeField
- searchable=1

image -- ImageField

- ImageField
- sizes ={'small':(100,100),'medium':(200,200),'large':(600,600)}
- AttributeStorage()

file -- FileField

- FileField
- AttributeStorage()
- FileWidget()

lines -- LinesField

- LinesField
- searchable=1

fixedpoint -- FixedPointField

- FixedPointField

reference -- ReferenceField

- ReferenceField

backreference -- BackReferenceField

- BackReferenceField

computed -- ComputedField

- ComputedField

color -- StringField w/Color picker

- StringField

country -- StringField

- StringField
- CountryWidget

datagrid -- DataGridField

- DataGridField
- DataGridWidget

photo -- PhotoField

- PhotoField

Tagged values for fields
=========================

searchable -- register and index the field in the catalog,

* 1 .. register and index
* 0 .. don't register and index

storage -- AttributeStorage(), SQLStorage(), ....

sizes -- defines the sizes of the images in a ImageField
example: python:{'small':(80,80),'medium':(200,2000),'large':(600,600)}

default_method -- no idea what that does

required -- defines whether a field should be rendered required, or not.

- 1 .. field is required
- 0 .. field is not required

accessor -- defines the accessor of a field

vocabulary -- defines the vocabulary or the method generating a vocabulary

allowed_types -- defines the allowed types in a ReferenceField

relationship -- defines the relationship, used in a ReferenceField

multiValued -- defines whether a SelectionField accepts one or more values,

- 1 .. multivalued
- 0 .. singlevalued

These tagged values are just the ones handy for fields, the full lists of tagged values
and stereotypes are shown on the next two pages.
