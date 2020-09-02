def launch_func(func,args):
	#Get the func args
	func_args = list(func.__code__.co_varnames)[0:func.__code__.co_argcount]
	kwargs={}
	for arg in args:
		if arg.lower() in func_args:
			kwargss[arg.lower()] = argss[arg]

	return func(**kwargs)
