def is_sub_str(str1, str2):
    return str1 in str2
    
def is_rotation(str1, str2):
    rotation = -1
    for i in range(len(str1)):
        if is_sub_str(str1[:i], str2):
            rotation = i
    if rotation == -1:
        return False
    if is_sub_str(str1[rotation:], str2):
        return True
    return False

str1, str2 = 'ido', 'ido'
print(str1, str2, is_rotation(str1, str2))
str1, str2 = 'ido', 'oid'
print(str1, str2, is_rotation(str1, str2))
str1, str2 = 'ido', 'doi'
print(str1, str2, is_rotation(str1, str2))
str1, str2 = 'ido', 'iod'
print(str1, str2, is_rotation(str1, str2))
str1, str2 = 'ido', 'idd'
print(str1, str2, is_rotation(str1, str2))
