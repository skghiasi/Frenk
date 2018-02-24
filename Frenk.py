import sublime
import sublime_plugin



class ExampleCommand(sublime_plugin.TextCommand):
	__char_dic =  {"e1":'é' , "e2":'è', "e3":'ê' , "e4":'ë', 			"e10":'É', "e20":'È',"e30":'Ê',"e40":'Ë' , 
				   			  "a2":'à', "a3":'â' , "a4":'ä', 					   "a20":'À',"a30":'Â', 
			  	                  		"o3":'ô' , "o4":'ö',            		   			 "o30":'Ô', 
				                 		"u3":'û' , "u4":'ü',	  	   			   			 "u30":'Û',
															 "a5": 'æ' , 		   								  "a50": 'Æ',
					"c1":'ç', 											"c10":'Ç',
										"i3":'î' , "i4":'ï'}

	
	__specialchars = {'\\':2 , '/':1 , '^':3 , '.':4 , '}':5}

	__raw_charlist = {'a','e','o','u','c','i'}

	__func = None 
	__coeff = 1


	def run(self, edit ):
		view = self.view 
		character = None	
		pos = view.sel()[0].begin()
		if(pos >= 2):
			if(self.is_specialchar(view.substr(pos-2))):
				character = view.substr(pos-2)
				if(character == '.' and pos > 2): 
					if(view.substr(pos - 3) == '.'): 
						self.__func = self.__specialchars['.'] 

				else: 
					self.__func = self.__specialchars[character]

				if(view.substr(pos-1).isupper()): 
					self.__coeff = 10 

		real_char = view.substr(pos - 1).lower()
		if((real_char in self.__raw_charlist) and self.__func != None ): 
			idx = real_char + str(self.__func * self.__coeff)
			region = sublime.Region(pos-2 , pos)
			if(self.__func == 4): 
				region = sublime.Region(pos-3 , pos)
			repl = self.__char_dic.get(idx , 'na')
			if(repl != 'na'): 
				self.view.replace(edit , region , self.__char_dic[idx]) 

		self.__func = None
		self.__coeff = 1



	def is_specialchar(self, x): 
		if(x in self.__specialchars): 
			return True 

		else: 
			return False 


class secondCommand (sublime_plugin.EventListener):
	already_in = False 
	def on_modified(self , view ): 
		filename = view.file_name()
		ext = filename[-3] + filename[-2] + filename[-1]
		if(ext == ".fr"): 
			if(secondCommand.already_in == False): 
				secondCommand.already_in = True
				view.run_command('example')		
				secondCommand.already_in = False


	
