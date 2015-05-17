Title: Create custom pytest skipif markers
Status: published
category: tech
tags: pytest
slug: custom_pytest_skipif_markers 

Quick example how to create reusable parametric 'skipif' markers

<!-- PELICAN_END_SUMMARY -->

[Pytest](https://pytest.org/latest/contents.html) is my favourite testing tool, it provides a lot of useful and highly configurable features. The idea  is to create custom [skipif](https://pytest.org/latest/skipping.html#skipping) markers that implement a complex logic removing the need to duplicate to much code, or using logic that cannot be read easily in one line.

So instead to write these:

	@skipif('path.to.my.app' not in settings.INSTALLED_APPS)

	@skipif('django.VERSION < (1.7))

I want to use this syntax:


	@skipif_django(1.7)
	
	@requires_app('reversion')
	

## The magic: autoused fixture and request object

We can use the [request](https://pytest.org/latest/builtin.html#_pytest.python.FixtureRequest) object to retrieve infos about the running test and the [autouse](https://pytest.org/latest/fixture.html#autouse-fixtures-xunit-setup-on-steroids) option to automatically execute our code.


    from django.apps import apps
    
    @pytest.fixture(autouse=True)
    def skip_if_markers_logic(request):
        if request.node.get_marker('requires_app'):
            app = request.node.get_marker('requires_app').args[0]
            if not apps.is_installed(app):
                pytest.skip('skipped as {} is not installed'.format(app))
    	if request.node.get_marker('skipif_django'):
        	arg = request.node.get_marker('skipif_django').args[0]
        	offset = 1
        	compare = {'==': operator.eq,
                   '<': operator.lt,
                   '>': operator.gt}
        	op = compare.get(str(arg)[0], None)
        	if op is None:
            	op = operator.eq
            	val = str(arg)
        	elif op == operator.eq:
            	val = str(arg)[2:]
        	else:
            	val = str(arg)[1:]

        	if op(val.split('.'), pytest.__version__):
            	pytest.skip('skipped as django {}'.format(arg))

now we can:

	@skipif_django('<1.7')
	def test_one():
		...


	@requires_app('reversion')
	def test_two():
		...
		
		
These examples are based on very simple logic, but it is evident how we can use any complex logic and create easy to read custom decorators.





