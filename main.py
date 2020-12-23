import sys
import cantera as ct
import sdtoolbox
from sdtoolbox.postshock import CJspeed, PostShock_eq, PostShock_fr
from sdtoolbox.reflections import reflected_eq, reflected_fr
from sdtoolbox.thermo import soundspeed_eq, soundspeed_fr
#githubtest
print(sys.version)

#圧力kPa,温度K
P1=101.325
T1=298.15
phi=0.5
P2=180
E2=0.65
E4=1.0
P4=P1

#定圧燃焼
gas = ct.Solution('gri30.xml')

#初期条件を設定
gas.TPX = T1,P1*100,{'H2':2*phi, 'O2':1, 'N2':3.76}

H1=gas.h

print(gas())
gasmassf=gas.mass_fraction_dict()
H2massf=gasmassf['H2']
#断熱圧縮
gas.SP=None,P2*100

print(gas())

HS2=gas.h


#効率を考慮した圧縮
H2=H1+(HS2-H1)/E2


gas.HP=H2,P2*100
print(gas())

H2=gas.h
T2=gas.T

""""
#デトネーション
MOL=gas.mole_fraction_dict()
cj_speed = CJspeed(P2*100, T2, MOL, 'gri30.cti')
gas = PostShock_eq(cj_speed,P2*100,T2, MOL, 'gri30.cti')
print(gas())
H3=gas.h
"""
#定圧燃焼

gas.equilibrate('HP')

H3=gas.h


print(gas())

#断熱膨張
gas.SP=None,P4*100

print(gas())

HS4=gas.h

#効率を考慮した膨張
H4=(HS4-H3)*E4+H3
gas.HP=H4,P4*100

print(gas())

#熱効率を算出
Eth=(H1-H4)/(H2massf*120900000)*100
print(str(Eth)+'[%]')


