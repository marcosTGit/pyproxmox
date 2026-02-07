from apyproxmoxtest import Promox

px=Promox()
print(px.getVersion())

datos=px.getInfoVMI(200)
print(datos['qmpstatus']['resources'])

for d in datos['qmpstatus']:
    print(f"\t{d}:\t {datos['qmpstatus'][d]}")