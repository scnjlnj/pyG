import pinyin


class Name_pin():
    text = None
    family_name = None
    given_name = None
    def __init__(self,family_name,given_name):
        self.family_name=family_name
        self.given_name=given_name
        self.text=family_name+"".join(given_name)
    def __repr__(self):
        return f"<Namep-{self.text}>"

class Name_han():
    text = None
    family_name = None
    given_name = None
    pin:Name_pin = None
    def __init__(self,family_name,given_name):
        self.family_name=family_name
        self.given_name=given_name
        self.text=family_name+given_name
        self.pin = Name_pin(pinyin.get(family_name),[pinyin.get(x) for x in given_name])
    def __repr__(self):
        return f"<Nameh-{self.text}>"

if __name__ == '__main__':
    n1 = Name_han("何","足道")
    print("")