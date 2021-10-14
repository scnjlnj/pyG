import pinyin
from control.juzi import JuziContoller
#
# juzi="学而时习之，不易乐乎。"
#
# JuziContoller.add_juzi(juzi)
from model import Name_han

n1 = Name_han("石","易习")
ret = JuziContoller.name_quote_info(n1.pin)
print("")