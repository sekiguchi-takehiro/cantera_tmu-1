import sys
import cantera as ct
import sdtoolbox
from sdtoolbox.postshock import CJspeed, PostShock_eq, PostShock_fr
from sdtoolbox.reflections import reflected_eq, reflected_fr
from sdtoolbox.thermo import soundspeed_eq, soundspeed_fr
#githubtest
#print(sys.version)
import inspect
import os
print(inspect.getfile(ct))
#圧力kPa,温度K
P1=101.325
T1=288.15
phi=0.8
P2=P1*1

E2=0.75
E4=0.82
P4=P1


inigas = ct.Solution('gri30.xml')

 #初期条件を設定(Air)
gas1 = ct.Quantity(inigas)
gas1.TPX = T1,P1*1000,{'O2':1, 'N2':3.76}
H1=gas1.h
#print(gas1.report())
#初期条件を設定(H2)


gas2 = ct.Quantity(inigas)
gas2.TPX = T1,P2*1000,{'H2':2*phi}

gas1.moles = 1
nO2 = gas1.X[gas1.species_index('O2')]
gas2.moles = nO2 * 2*phi

inigas = gas1 + gas2

H1mix=inigas.h
print(gas1.report())

#断熱圧縮
gas1.SP=None,P2*1000

gas1.SP=None,P2*1000

gas1.SP=None,P2*1000
HS2=gas1.h

print(gas1.report())
#効率を考慮した圧縮
H2=H1+(HS2-H1)/E2


gas1.HP=H2,P2*1000

H2=gas1.h
T2=gas1.T
print(gas1.report())

print(gas2.report())

gas = gas1 + gas2
print(gas.report())

gasmassf=gas.mass_fraction_dict()
H2massf=gasmassf['H2']

"""
#デトネーション
MOL=gas.mole_fraction_dict()
cj_speed = CJspeed(P2*1000, T2, MOL, 'gri30.cti')
gas = PostShock_eq(cj_speed,P2*1000,T2, MOL, 'gri30.cti')
print(gas())


"""
#定圧燃焼

gas.equilibrate('HP')

"""
#定積燃焼
gas.equilibrate('UV')

"""
H3=gas.h


#断熱膨張
gas.SP=None,P4*1000
gas.equilibrate('SP')
print(gas.report())

HS4=gas.h

#効率を考慮した膨張
H4=(HS4-H3)*E4+H3
gas.HP=H4,P4*1000
gas.equilibrate('HP')
print(gas.report())

#熱効率を算出
Eth=(H1mix-H4)/(H2massf*120900000)*100
print(str(Eth)+'[%]')


