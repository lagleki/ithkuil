vowels = ['a','â','e','ê','ë','i','î','o','ô','ö','u','û','ü',
		  'á', 'é', 'í', 'ó', 'ú', 'à', 'è', 'ì', 'ò', 'ù']

bare_vowels = ['a', 'e', 'i', 'o', 'u']
acute_vowels = ['á', 'é', 'í', 'ó', 'ú']
grave_vowels = ['à', 'è', 'ì', 'ò', 'ù']

consonants_s = ['b', 'c', 'č', 'ç', 'd', 'f', 'g', 'h', 'j', 
				'k', 'l', 'ļ', 'm', 'n', 'ň', 'p', 'q', 
				'r', 'ř', 's', 'š', 't', 'ţ', 'v', 'w', 'x', 'y', 'z', 
				'ż', 'ž']
consonants_d = ['c’', 'cʰ', 'č’', 'čʰ', 'dh', 'k’', 'kʰ', 'p’', 'pʰ', 
				'q’', 'qʰ', 't’', 'tʰ', 'xh']
geminated = ['l', 'm', 'n', 'ň', 'r']
tones = ['_','/','ˇ','^','¯']

def remove_accents(s, preserve=False):
	s = s.replace('á', 'a')
	s = s.replace('é', 'e')
	s = s.replace('í', 'i')
	s = s.replace('ó', 'o')
	s = s.replace('ú', 'u')
	s = s.replace('à', 'a')
	s = s.replace('è', 'e')
	s = s.replace('ò', 'o')
	s = s.replace('ì', 'i')
	s = s.replace('ù', 'u')
	return s

def validation(s):
	if s in ('h','w','y','hw','hh','hr','hm','hn','lw','ly','rw','ry','řw','řy'):
		return True
	return False

def is_verbal_adjunct(parts):
	if parts[-1][0] in vowels:
		if '-' in parts[-2]:
			return True
	else:
		if '-' in parts[-1]:
			return True
		if len(parts) > 2 and '-' in parts[-3]:
			return True
	return False

def is_personal_adjunct(parts):
	count_consonants = 0
	for p in parts:
		if p[0] not in vowels:
			count_consonants += 1
	if count_consonants == 1 and parts[-1][0] in vowels:
		return True
	if parts[-1][0] in vowels:
		if parts[-2] in ('w','y','h','hw'):
			return True
	else:
		if '’' in parts[-2] and parts[-3] in ('w','y','h','hw'):
			return True
	return False

def is_affixual_adjunct(parts):
	if len(parts) != 2:
		return False
	if parts[0][0] not in vowels or parts[1][0] in vowels:
		return False
	return True

def is_aspectual_adjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] not in vowels:
		return False
	return True

def is_bias_adjunct(parts):
	if len(parts) != 1:
		return False
	if parts[0][0] in vowels:
		return False
	return True

def split_word(s):
	if not s:
		return []
	elif s[0] in tones:
		return [s[0]] + split_word(s[1:])
	elif s[0] in consonants_s + ['’', 'ʰ', '-']:
		part = ''
		while s and s[0] in consonants_s + ['’', 'ʰ', '-']:
			part += s[0]
			s = s[1:]
		return [part] + split_word(s)
	elif s[0] in vowels + ['’']:
		part = ''
		while s and s[0] in vowels + ['’']:
			part += s[0]
			s = s[1:]
		return [part] + split_word(s)
	raise Exception('Something went terribly wrong')
	
def analyze_stress(parts):
	parts2 = parts[:]
	parts_no_stress = parts[:]
	
	for p in parts:
		if p[0] not in vowels and '-' not in p:
			parts2.remove(p)
			
	parts3 = []
	for p in parts2:
		parts4 = p.split('’')
		i = parts.index(p)
		for p4 in parts4:
			if p4: 
				if len(p4) == 2 and p4[0] == p4[1]:
					parts3.append((i, p4))
				elif len(p4) == 2 and remove_accents(p4[1]) not in ('i','u'):
					parts3.append((i, p4[0]))
					parts3.append((i, p4[1]))
				elif len(p4) == 2 and p4[1] in grave_vowels:
					parts3.append((i, p4[0]))
					parts3.append((i, remove_accents(p4[1])))
				elif len(p4) == 2 and p4[1] in acute_vowels:
					parts3.append((i, p4[0]))
					parts3.append((i, p4[1]))
				else:
					parts3.append((i, p4[0]))
	
	for i in range(len(parts3)-1, -1, -1):
		p = parts3[i][1]
		if len(p)>1 and p[0] == p[1]:
			parts_no_stress[parts3[i][0]] = p[0]
			return str(i-len(parts3)), parts_no_stress
		
	for i in range(len(parts3)-1, -1, -1):
		p = parts3[i][1]
		if p[0] in acute_vowels:
			part = parts_no_stress[parts3[i][0]]
			if p[0] in ('í', 'ú') and part.index(p[0]) > 0 and part[part.index(p[0])-1] in ('a','e','i','o','u','ö','ë'):
				part = part.replace(p[0], grave_vowels[acute_vowels.index(p[0])])
				parts_no_stress[parts3[i][0]] = part
			else:
				parts_no_stress[parts3[i][0]] = remove_accents(parts_no_stress[parts3[i][0]])
			return str(i-len(parts3)), parts_no_stress
		
	for i in range(len(parts3)-1, -1, -1):
		p = parts3[i][1]
		if p[0] in grave_vowels:
			parts_no_stress[parts3[i][0]] = remove_accents(parts_no_stress[parts3[i][0]])
			if i == len(parts3)-1:
				try:
					if parts3[-3][1] not in bare_vowels:
						return '-3', parts_no_stress
					elif parts3[-4][1] not in bare_vowels:
						return '-4', parts_no_stress
				except:
					return 'wtf', []
				return 'wtf', []
			elif i == len(parts3)-2:
				try:
					if parts3[-1][1] not in bare_vowels:
						return '-1', parts_no_stress
					elif parts3[-3][1] not in bare_vowels:
						return '-3', parts_no_stress
					elif parts3[-4][1] not in bare_vowels:
						return '-4', parts_no_stress 
				except:
					return 'wtf', []
				return 'wtf', []
			elif i == len(parts3)-3:
				try:
					if parts3[-1][1] not in bare_vowels and parts3[-2][1] not in bare_vowels:
						return '-1', parts_no_stress
					else:
						return '-4', parts_no_stress
				except:
					return 'wtf', []
				return 'wtf', []
		
	return '-2', parts_no_stress

def analyze_affixual_adjunct(parts):
	slots = {'type': 'Affixual adjunct', 1: (parts[0], parts[1])}
	return slots

def analyze_aspectual_adjunct(parts):
	slots = {'type': 'Aspectual adjunct', 1: parts[0]}
	return slots

def analyze_bias_adjunct(parts):
	slots = {'type': 'Bias adjunct', 1: parts[0]}
	return slots

def analyze_verbal_adjunct(parts):
	slots = {'type': 'Verbal adjunct'}
	
	if len(parts)>2 and parts[-2][-1] == '’':
		parts[-2] = parts[-2][:-1]
		slots['G'] = parts[-1]
		parts = parts[:-1]
	
	if parts[-1][0] in vowels:
		slots['F'] = parts[-1]
		parts = parts[:-1]
		
	if parts[0] in tones:
		slots['H'] = parts[0]
		parts = parts[1:]
		
	slots['E'] = parts[-1]
	if len(parts) > 1:
		slots['D'] = parts[-2]
	if len(parts) > 2:
		slots['C'] = parts[-3]
	if len(parts) > 3:
		slots['B'] = parts[-4]
	if len(parts) > 4:
		slots['A'] = parts[-5]
	
	return slots

def analyze_personal_adjunct(parts):
	slots = {'type': 'Personal adjunct'}
	
	if parts[0] in tones:
		slots['[tone]'] = parts[0]
		parts = parts[1:]
		
	if parts[-1][0] not in vowels:
		slots['bias'] = parts[-1]
		parts[-2] = parts[-2][:-1]
		parts = parts[:-1]
		
	if parts[-2] in ('w', 'y', 'h', 'hw'):
		slots['Cz'] = parts[-2]
		slots['Vz'] = parts[-1]
		if parts[-3][-1] == '’':
			parts[-3] = parts[-3][:-1]
			slots['Cz'] = '’' + slots['Cz']
		parts = parts[:-2]
		
	slots['C1'] = parts[-2]
	slots['V1'] = parts[-1]
	parts = parts[:-2]
	
	if (len(slots['C1']) == 1 and slots['C1'] not in ('g', 'd', 'j', 'ż', 'c', 'b')) or slots['C1'] == 'xh':
		#single-referent
		slots['CsVs'] = []
		if len(parts) == 1:
			slots['V2'] = parts[0]
		else:
			while parts:
				slots['CsVs'].append((parts[-1], parts[-2]))
				parts = parts[:-2]
	else:
		#dual-referent
		slots['Ck'] = slots['C1']
		del slots['C1']
		
		slots['V2'] = parts[-1]
		parts = parts[:-1]
		if parts:
			slots['C2'] = parts[-1]
			parts = parts[:-1]
		if parts:
			slots['Vw'] = parts[-1]
			
	return slots

def analyze_formative(parts, force_cx=False):
	slots = {'type': 'Formative'}
	if not force_cx:
		save_parts = parts[:]
	
	# tone
	if parts[0] in tones:
		slots['[tone]'] = parts[0]
		parts = parts[1:]
	
	# first, we determine if slots I-III are filled
	if parts[0][0] in vowels:
		if validation(parts[1]) or '-' in parts[1]:
			slots['Vl'] = parts[0]
			if validation(parts[1]):
				slots['Cg'] = parts[1]
			else:
				slots['Cs'] = parts[1]
			slots['Vr'] = parts[2]
			parts = parts[3:]
		else:
			slots['Vr'] = parts[0]
			parts = parts[1:]
	else:
		# is slot I filled?
		if '-' in parts[2]:
			slots['Cv'] = parts[0]
			slots['Vl'] = parts[1]
			slots['Cs'] = parts[2]
			slots['Vr'] = parts[3]
			parts = parts[4:]
		# if not, do we begin with slot III?
		elif validation(parts[0]) or '-' in parts[0]:
			if validation(parts[0]):
				slots['Cg'] = parts[0]
			else:
				slots['Cs'] = parts[0]
			slots['Vr'] = parts[1]
			parts = parts[2:]
	# now slots I-IV are determined and parts begin with slot V or VII	 
	
	# are slots V and VI filled?
	# check for glottal stop:
	if 'Vr' in slots and slots['Vr'][-1] == '’':
		slots[5] = parts[0]
		slots[6] = parts[1]
		parts = parts[2:]
		slots['Vr'] = slots['Vr'][:-1]

	# if there was no glottal stop, check -wë-
	try:
		if 5 not in slots:
			for i in range(len(parts)):
				if parts[i] in ('w', 'y', 'h', 'hw') and i != 2:
					slots[5] = parts[0]
					slots[6] = parts[1]
					parts = parts[2:]
					break
	except:
		pass
		
	# last - check format
	if parts[-1][0] in vowels:
		slots['Vf'] = parts[-1]
		parts = parts[:-1]
	elif parts[-2][-1] == '’' and len(parts)-2 > 1:
		slots['Vf'] = parts[-2][:-1]
		slots['Cb'] = parts[-1]
		parts = parts[:-2]
	else:
		slots['Vf'] = 'a'
		
	if 5 not in slots and (slots['Vf'] not in ('a', 'i', 'e', 'u') or force_cx):
		slots[5] = parts[0]
		slots[6] = parts[1]
		parts = parts[2:]

	# now slots V and VI are determined and we are at slot VII	
	slots['Cr'] = parts[0]
	slots['Vc'] = parts[1]
	parts = parts[2:]
	# now we know slots VII and VIII

	if '’' in slots['Vc'] and slots['Vc'][-1] != '’':
		# handle xx'V case
		pts = slots['Vc'].split('’')
		if pts[1] != 'a' or 'Vr' not in slots:
			slots['Vr'] = pts[1]
		elif pts[1] != 'a' and 'Vr' in slots:
			raise Exception('Stem and Pattern defined twice: in Vr and Vc')
		slots['Vc'] = pts[0] + '’V'

	# check for slot IX
	if parts[0] in ('w', 'y', 'h', 'hw'):
		if parts[0] == 'hw' and len(slots['Vc']) > 1 and slots['Vc'][-1] == 'i' and slots['Vc'][-2] != '’':
			slots['Ci+Vi'] = 'y' + parts[1]
		elif parts[0] == 'hw' and slots['Vc'] in ('a','e','i','o','ö','ë'):
			slots['Ci+Vi'] = 'w' + parts[1]
			slots['Vc'] = slots['Vc'] + 'u'
		else:
			slots['Ci+Vi'] = parts[0] + parts[1]
		parts = parts[2:]
	
	# slot X	
	slots['Ca'] = parts[0]
	parts = parts[1:]

	# suffixes
	slots['VxC'] = []
	while len(parts) > 1:
		slots['VxC'].append((parts[0], parts[1]))
		parts = parts[2:]
	
	if parts:
		raise Exception('Unexpected slot after Ca/VxC!')
	
	fe_suffix = False
	for _, typ in slots['VxC']:
		if typ in ['tt', 'pk', 'qq', 'tk',
					'st’', 'sp’', 'sq’', 'sk’',
					'št’', 'šp’', 'šq’', 'šk’']:
			fe_suffix = True
			break
			
	if fe_suffix and 5 not in slots:
		return analyze_formative(save_parts, True)
	
	# if there is format or format expansion suffix		
	if fe_suffix or slots['Vf'] not in ('a', 'i', 'e', 'u'):
		if 5 in slots and 6 in slots:
			slots['Cx'] = slots[5]
			slots['Vp'] = slots[6]
			del slots[6]
			del slots[5]
		else:
			raise Exception('Format was specified but there is no incorporated root!')
	
	# if slots V and VI are present, but they are not the incorporated root		
	if 5 in slots and 6 in slots:
		if 'Cv' in slots:
			raise Exception('Cv defined twice (in slot I and V)!')
		if 'Vl' in slots:
			raise Exception('Vl defined twice (in slot II and VI)!')
		slots['Cv'] = slots[5]
		slots['Vl'] = slots[6]
		del slots[5]
		del slots[6]
		
	if 'Vr' not in slots:
		slots['Vr'] = 'a'

	return slots
	
def analyze_word(word):
	word = word.replace('\'', '’').replace('‾', '¯')
	
	try:
		parts_stress = split_word(word.lower())
	except:
		return {'error': 'Couldn\'t split word: %s (maybe it contained illegal characters?)' % word}
		
	try:
		stress, parts = analyze_stress(parts_stress)
	except:
		return {'error': 'Couldn\'t analyze stress in word: %s' % word}

	try:
		if is_bias_adjunct(parts):
			slots = analyze_bias_adjunct(parts)
	
		elif is_aspectual_adjunct(parts):
			slots = analyze_aspectual_adjunct(parts)
		
		elif is_verbal_adjunct(parts):
			slots = analyze_verbal_adjunct(parts)
	
		elif is_affixual_adjunct(parts):
			slots = analyze_affixual_adjunct(parts)

		elif is_personal_adjunct(parts):
			slots = analyze_personal_adjunct(parts)
			slots['[stress]'] = stress
		
		else:
			slots = analyze_formative(parts)
			slots['[stress]'] = stress
	except IndexError as e:
		slots = {'error': 'A filled slot was expected, but it was empty!'}
	except Exception as e:
		slots = {'error': e.args[0]}
		
	return slots