import sqlite3, json, time

profilename = "eq2"
parfilename = "arctis pre-eq.txt"



con = sqlite3.connect("database.db")
cur = con.cursor()
#res = cur.execute(f"select * from configs where name = '{profilename}';")
#data = res.fetchone()
#print(data)
preamble = '''{"bassBoostState":{"enabled":false,"value":0.0},"trebleBoostState":{"enabled":false,"value":0.0},"voiceClarityState":{"enabled":false,"value":0.0},"smartVolume":{"enabled":false,"volumeLevel":0.0,"loudness":"balanced"},"generalGain":0.0,"parametricEQ":{"enabled":true,'''
postamble = '''"virtualSurroundState":false,"virtualSurroundChannels":{"frontLeft":{"position":30.0,"gain":0.0},"frontRight":{"position":-30.0,"gain":0.0},"center":{"position":0.0,"gain":0.0},"subWoofer":{"position":0.0,"gain":0.0},"rearLeft":{"position":150.0,"gain":0.0},"rearRight":{"position":-150.0,"gain":0.0},"sideLeft":{"position":90.0,"gain":0.0},"sideRight":{"position":-90.0,"gain":0.0}},"reverbGainDB":0.0,"formFactor":"headphones","globalEnableState":true}'''
file = open(f"{parfilename}","r").read().split("\n")[:11]
splitup = []
for x in file:
    print(x)
    splitup.append(x.split(" ")[3:])
splitup = splitup[1:]
#print(splitup)
count=1
#exit()
typedict = {
    "LS":"lowShelving",
    "HS":"highShelving",
    "PK":"peakingEQ",
    "LP":"lowPass",
    "HP":"highPass",
    "NO":"notchFilter"
    }


for x in splitup:
    #print(x)
    curvetype = typedict[str(x[0])]
    qfac = max(min(float(x[8]),10),0.5)
    freq = max(min(float(x[2]),20000),20)
    gain = max(min(float(x[5]),12),-12)
    brackets = '"filter{0}":{{"enabled":true,"qFactor":{1},"frequency":{2},"gain":{3},"type":"{4}"}},'.format(count,qfac,freq,gain,curvetype)
    #print(brackets)
    preamble+=brackets
    count+=1

preamble = preamble[:-1]+"},"+postamble
preamble = json.dumps(json.loads(preamble),indent=4).replace("\n","\r\n")
#print(preamble)
cur.execute(f'''update configs set data = ? where name = "{profilename}";''', (preamble,))
#data2 = cur.execute(f'select * from configs where name = "{profilename}";')

#print("\n\n\n\n\n\n\n\n\n\n")
#print(data2.fetchone())
con.commit()
#"filter1":{"enabled":true,"qFactor":0.7071,"frequency":35.0,"gain":0.0,"type":"peakingEQ"},
print("done (:")
time.sleep(3)
print("probably not well but eh")
