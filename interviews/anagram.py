def is_anagram(str1, str2):
    if lem(str1) != len(str2):
        return False
    if str1 == str2:
        return True
    letter_counter = dict()
    for letter in str1:
        letter_counter.setdefault(letter, 0) += 1
    for letter in str2:
        if letter in letter_counter:
            letter_counter[letter] -= 1
            if letter_counter[letter] < 0:
                return False
        else:
            return False
    return True
    
    
ido doi
ido -> {'i':1, 'd':1, 'o':1}
doii: {'i':-1, 'd':0, 'o':0}
dob: {'i':1, 'd':0, 'o':0}
