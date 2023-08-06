

#Global Constants
SEPARATOR = '_'


# File Processor
# ==============
def readictionary(handle):
    filename = 'a2/dict.txt'
    words = {}
    ctr = 0
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f]
    for line in lines:  
                if(handle == 'enc'):
                        words[line.lower()] = ctr
                else:
                        words[ctr] = line.lower()

                ctr = ctr + 1
    return words


# Word Finder
# ==============
def find_word(start_letter, end_letter, length):
        words = readictionary('enc')
        rt = [w for w in words if str(w)[0].lower() == start_letter.lower() and str(w)[len(w) - 1].lower() == end_letter.lower() and len(w) == length]
        return rt

# Encrypt
# ================
def aichin(phrase):
        letters_map = get_mapper()
     
        hex_string = SEPARATOR.join(format(ord(x), 'x') for x in phrase)
        encrypted_value = ''.join([letters_map[letter_in_hex] for letter_in_hex in hex_string])
       
        return (encrypted_value)



# Decrypt
# ================
def aichout(phrase):
        phrase = str(phrase)
        letters_map = get_mapper()
        reversed_letters_map = {v: k for k, v in letters_map.items()}
        # seperator = list(reversed_letters_map.keys())[-1]
        separator = letters_map[SEPARATOR]
        words_in_phrase = phrase.split(separator)
        
         
        p2 = []
        for word in words_in_phrase:
           p1 = ''  
        #     p1 = ''.join([(reversed_letters_map[l] if (l in reversed_letters_map) else l) for l in word])
        # Not Using Above List Comprehension method for readability.
           for letter_in_word in word:
               letter_in_word = str(letter_in_word)
               if reversed_letters_map[letter_in_word] != '':
                   p1 = p1 + "" + reversed_letters_map[letter_in_word]
               else:
                   p1 = p1 + "" + letter_in_word
           p2.append(chr(int(p1, 16)))
        decrypted_value = ''.join(p2)

        return decrypted_value

# Mapper
def get_mapper():
    l = {'1': {'0':'h', '1':'o', '2':'x', '3':'r', '4':'w', '5':'z', '6':'u', '7':'s', '8':'g', '9':'v', 'a':'i','b':'k','c':'k','d':'l','e':'m','f':'n', '_':'j'},
                '2': {'0':'म', '1':'ण', '2':'य', '3':'क', '4':'न', '5':'ष', '6':'द', '7':'ख', '8':'प', '9':'श', 'a':'ह','b':'ज','c':'ट','d':'त','e':'ए','f':'ग', '_':'फ'}}

    return l['2']

# Mapping Key Date Handler
def date_add(ini_date):
    y = 0
    l = []
    for id in ini_date:
        y = y + int(id)
    
    
    while len(str(y)) > 1:
        x = 0
        for y1 in str(y):
            x = x + int(y1)
            # print (x)
        y = x

        return y