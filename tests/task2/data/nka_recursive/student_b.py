# "{0}"

def q0(s):
    if s == "":
        return True
    if s[0] == '0':
        return q0(s[1:])
    return False
