=====
To Do
=====

- Add yamllint config
- Finish writing vale checks
- plone-vale container should include all checks (ttd)
- Move content out of source
- Improve Makefile
- Check why the "link" check is here not working

This And That
=============

docker org for vale: #@docker run --rm -it -v "${PWD}/styles":/styles --rm -v "${PWD}/source":/docs -w /docs jdkato/vale .
