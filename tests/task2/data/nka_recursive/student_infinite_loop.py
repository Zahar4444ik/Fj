# "{0}"

def q0(s):
    return q0(s) or (s != "" and s[0] == '0' and q0(s[1:]))
