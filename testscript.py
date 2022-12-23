import sys, os, shutil, sqlite3, json, time
#reqArgCount = 2
#print("args:")
#argcount = len(sys.argv)-1


typedict = {
    "LS":"lowShelving",
    "HS":"highShelving",
    "PK":"peakingEQ",
    "LP":"lowPass",
    "HP":"highPass",
    "NO":"notchFilter"
    }




for x in sys.argv[1:]:
    print(x)

    
#print("end")
def check_arg_num(argcount,reqArgCount):
    if argcount<reqArgCount:
        print(f"Not enough arguments, {reqArgCount} required but {argcount} given!")
        exit()
    else:
            return sys.argv[1], sys.argv[2]
    exit()
                
        



#answer = con.execute('''select id from configs where (name = "Default") AND (vad = 2)''')

def check_database():
    if os.path.exists("database.db"):
        #print("Database found")
        if not os.path.exists("database.BAK"):
            shutil.copy("database.db","database.BAK")
            print("Database has been backed up")
        else:
            print("database has already been backed up")
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            return con, cur
        except:
            print("Database could not be connected to")
    else:
        print("Database not found")


def correct_database(cur):
    answer = cur.execute('''SELECT name FROM sqlite_master WHERE type="table";''').fetchall()
    key1 = ('selected_config',)
    key2 = ('configs',)
    if not (key1 in answer and key2 in answer):
        print('''The database given does not match the pattern, are you in "/GG/apps/sonar/db"?''')
        exit()
    else:
        return
        #print("Correct database found")


def db_safety_check(cur,profile_name):
    profile_search = cur.execute(f'''select id from configs where (name = "{profile_name}" AND (vad = 1))''').fetchall()
    if len(profile_search) == 0:
        print("No profiles with that name found")
        exit()
    elif len(profile_search) >1:
        print("There were multiple profiles with that name, somehow. Everything is broken!")
    else:
        profile_id = profile_search[0]
        if cur.execute('''select config_id from selected_config where vad=1''').fetchone()[0] == profile_id:
             print("WARNING, you have the config you're editing currently selected, this can brick your app. If it does, restore the db from backup and try again?")
        
        return profile_id[0]
        
        




def get_file_data(filename):
    try:
        file = open(f"{filename}","r").read().split("\n")[:11]
        file_2d = []
        for x in file:
            file_2d.append(x.split(" ")[3:])
        file_2d = file_2d[1:]
        file_check = check_file_data(file_2d)
        print(file_check)
        if file_check != None:
            return file_check
        else:
            print(f"The file {filename} could not be interpeted properly")
            os._exit(1)
         
    except FileNotFoundError:
        print(f'AutoEQ file {filename} was not found!')
        exit()
    except Exception as e:
        print(e)
        print("AutoEQ file {filename} failed to be read")
        exit()


def check_file_data(file_data):
    for x in file_data:
        if x[0] not in list(typedict.keys()):
            return

    return file_data

    

def exec_db(cur, filters, profile_id):
    
    preamble = '''{"bassBoostState":{"enabled":false,"value":0.0},"trebleBoostState":{"enabled":false,"value":0.0},"voiceClarityState":{"enabled":false,"value":0.0},"smartVolume":{"enabled":false,"volumeLevel":0.0,"loudness":"balanced"},"generalGain":0.0,"parametricEQ":{"enabled":true,'''
    postamble = '''"virtualSurroundState":false,"virtualSurroundChannels":{"frontLeft":{"position":30.0,"gain":0.0},"frontRight":{"position":-30.0,"gain":0.0},"center":{"position":0.0,"gain":0.0},"subWoofer":{"position":0.0,"gain":0.0},"rearLeft":{"position":150.0,"gain":0.0},"rearRight":{"position":-150.0,"gain":0.0},"sideLeft":{"position":90.0,"gain":0.0},"sideRight":{"position":-90.0,"gain":0.0}},"reverbGainDB":0.0,"formFactor":"headphones","globalEnableState":true}'''
    count=1
    print(filters)
    for x in filters:
        curvetype = typedict[str(x[0])]
        qfac = max(min(float(x[8]),10),0.5)
        freq = max(min(float(x[2]),20000),20)
        gain = max(min(float(x[5]),12),-12)
        brackets = '"filter{0}":{{"enabled":true,"qFactor":{1},"frequency":{2},"gain":{3},"type":"{4}"}},'.format(count,qfac,freq,gain,curvetype)
        preamble+=brackets
        count+=1
    preamble = preamble[:-1]+"},"+postamble
    preamble = json.dumps(json.loads(preamble),indent=4).replace("\n","\r\n")
    print(profile_id)
    cur.execute(f'''update configs set data = ? where id = "{profile_id}";''', (preamble,))

def kill_steelseries():
    os.system('taskkill /F /im SteelSeriesGGClient.exe')
    os.system('taskkill /F /im SteelSeriesGGClient.exe')
    os.system('taskkill /F /im SteelSeriesGG.exe')



filename_unsafe, profile_unsafe = check_arg_num(len(sys.argv)-1, 2)


db_connection, db_cursor = check_database()
correct_database(db_cursor)
profile_id = db_safety_check(db_cursor,profile_unsafe)


filter_list = get_file_data(sys.argv[1])

kill_steelseries()
time.sleep(1)
exec_db(db_cursor, filter_list, profile_id)
db_connection.commit()
print("Completed sucessfully!")
