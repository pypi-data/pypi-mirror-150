import string
import unicodedata
import re
from difflib import SequenceMatcher

class TextUtils:
	def encode_text(self, text_to_encode):
		if text_to_encode == None:
			return ''

		return " ".join(str(unicodedata.normalize('NFKD', text_to_encode).encode('ascii', 'replace').decode('utf8')).strip().lower().split())


	def num_repeating_characters(self, check_string):
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			count = {}
			length = 0
   
			for s in check_string:
				if s in count:
					count[s] += 1
				else:
					count[s] = 1
     
			for key in count:
				if count[key] > 1:
						length += 1
      
			return length

	def length_longest_substring(self, check_string):
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			len_substring = 0
			longest = 0   
			for i in range(len(check_string)):
				if i > 0:
					if check_string[i] != check_string[i-1]:
						len_substring = 0
      
				len_substring += 1
				if len_substring > longest:
					longest = len_substring
     
			return longest

	def num_repeating_sequences(self, check_string): 
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			n = len(check_string) 
			count = 0
			cur_count = 1
	
			# Traverse string except last character 
			for i in range(n): 
			
				# If current character matches with next 
				if (i < n - 1 and 
					check_string[i] == check_string[i + 1]): 
					cur_count += 1
	
				# If doesn't match, update result (if required) and reset count 
				else: 
					if cur_count > 1:
						count += 1
					cur_count = 1

			return count

	def vowel_score(self, check_string):
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			v = {'a','e','i','o','u'}
			dist = 0
			prev = -1
			nv = 1
			for index in range(len(check_string)):
				if check_string[index] in v:				
					if (prev == -1):
						prev = index
						continue
  
					dist = dist + (index-prev-1)
					prev = index 
					nv = nv + 1
		
		return dist/(nv * len(check_string))

	def get_alphanumeric_code(self, check_string):
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			if all(x.isalpha() or x.isspace() for x in check_string):
				return 1
			elif all(x.isdigit() for x in check_string):
				return 2
			else:
				return 0

	def matches_phone_number_pattern(self, check_string):
		if(check_string == None) or (len(check_string) == 0):
			return 0
		else:
			if(re.search("^[0-9\s+_()-]*$", check_string) == None):
				return 0
			else:
				return 1

	def sequence_similarity(self, str1, str2):
		if(str == None) or (len(str1) == 0):
			return -1

		if(str2 == None) or (len(str2) == 0):
			return -1
     
		return SequenceMatcher(None, str1, str2).ratio()

class TextNormalizer:

    def tokenize(self,x,delim=','):
        x = x.split(delim)
        return x
