def choice(text, choices):
	'''given a question text and a list of choice strings, asks the user
	to choose one and returns it'''
	print text,":"
	for i, c in enumerate(choices):
		print str(i+1)+") "+c
	response=""
	while type(response)!=type(0) or response<0 or response>len(choices):
		print "> ",
		response= raw_input()
		try:
			response= int(response)
		except:
			pass
	return response-1

print question("why",["yes","no"])
