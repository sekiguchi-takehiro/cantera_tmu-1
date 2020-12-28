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
T1=288.15
phi=0.1
P2=P1*1
T3lim=840+273.15
E2=0.75
E4=0.82
Er=0.83
P4=P1
H6=0
T3=0
H2massf=0
H1mix=0
"""

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
#print(gas2.report())




#断熱圧縮
gas1.SP=None,P2*1000



HS2=gas1.h

#print(gas1.report())
#効率を考慮した圧縮
H2=H1+(HS2-H1)/E2


gas1.HP=H2,P2*1000

H2=gas1.h
T2=gas1.T
#print(gas1.report())




gas = gas1 + gas2
#print(gas.report())


gasmassf=gas.mass_fraction_dict()
H2massf=gasmassf['H2']


#定圧燃焼


gas.equilibrate('HP')
H3=gas.h
T30=gas.h
#print(gas.report())

#断熱膨張
gas.SP=None,P4*1000

#print(gas.report())

HS4=gas.h

#効率を考慮した膨張
H4=(HS4-H3)*E4+H3
gas.HP=H4,P4*1000

#print(gas.report())

gas.TP=T2,P4*1000
HS6=gas.h

H60=Er*(HS6-H4)+H4
#print(H4)
#print(H6)

gas.HP=H6,P4*1000
H6prei=H60
T3pre=T30
"""
#print(gas.report())
for i  in range(10000):
    H6prei=H6
    T3pre=T3
    phi=phi+0.0001
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
    H1mixpre=H1mix
    H1mix=inigas.h
    #print(gas2.report())
    
    
    
    
    #断熱圧縮
    gas1.SP=None,P2*1000
    
    
    
    HS2=gas1.h
    
    #print(gas1.report())
    #効率を考慮した圧縮
    H2=H1+(HS2-H1)/E2
    
    
    gas1.HP=H2,P2*1000
    
    H2=gas1.h
    T2=gas1.T
    #print(gas1.report())
   
    
    
    
    gas = gas1 + gas2
    #print(gas.report())
    
    
    gasmassf=gas.mass_fraction_dict()
    H2massfpre=H2massf
    H2massf=gasmassf['H2']
    
    
    #定圧燃焼
    
    
    gas.equilibrate('HP')
    H3=gas.h
    T3=gas.h
  
    
    #断熱膨張
    gas.SP=None,P4*1000
    
    
    
    HS4=gas.h
    
    #効率を考慮した膨張
    H4=(HS4-H3)*E4+H3
    gas.HP=H4,P4*1000
    
    
    
    gas.TP=T2,P4*1000
    HS6=gas.h
    
    H6=Er*(HS6-H4)+H4
    
    
    gas.HP=H6,P4*1000
    #print(gas.report())
    
    for j  in range(10000):
        H6prej=H6
        gas1.HP=H2+(H4-H6),P2*1000
        
        gas = gas1 + gas2
        #print(gas.report())
        
        
        gasmassf=gas.mass_fraction_dict()
        H2massf=gasmassf['H2']
        
    
        #定圧燃焼
    
    
        gas.equilibrate('HP')
        H3=gas.h
        #print(gas.report())
     
      
        T3=gas.T
       
        #断熱膨張
        gas.SP=None,P4*1000
        
        #print(gas.report())
        
        HS4=gas.h
        
        #効率を考慮した膨張
        H4=(HS4-H3)*E4+H3
        gas.HP=H4,P4*1000
        
       # print(gas.report())
        
        gas.TP=T2,P4*1000
        HS6=gas.h
        
        
        H6=Er*(HS6-H4)+H4
        #print(H6)
        gas.HP=H6,P4*1000
       #print(gas.report())
       
        
        if H6-H6prej<1 and H6-H6prej>-1 :
           break
    
    print(j)
    print(H6-H6prej)
    print(T3pre-273.15)
    print(T3-273.15)
    
    if  T3>T3lim and i>0 :
        break
    if  T3>T3lim and i==0 :
        phi=phi/5
print("finish")
print(i)
print(phi)
print(T3pre-273.15)

#熱効率を算出
Eth=(H1mixpre-H6prei)/(H2massfpre*120900000)*100
print(str(Eth)+'[%]')


