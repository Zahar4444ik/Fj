# "{0}1"

def q0(s):
    if s == "":
        return True
    if s[0] == '0':
        return q0(s[1:])
    if s[0] == '1':
        return True
