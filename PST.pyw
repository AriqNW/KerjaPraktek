import os
import schedule
import datetime
import mysql.connector
import getpass
import sys
import pandas as pd
from pandas import DataFrame

## Proses saat reboot script akan otomatis running

USER_NAME = getpass.getuser()

def add_to_startup(file_path=""):
    file_python = sys.executable
    if file_path == "":
        file_path = os.path.dirname(os.path.realpath(__file__))+'\PST.pyw'
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
    with open(bat_path + '\\' + "PST.bat", "w+") as bat_file:
        bat_file.write(r'%s %s %s' % (file_python, file_path, '%*'))

## Connect database

mydb = mysql.connector.connect(
    host="localhost",
    user="haru",
    passwd="haru",
    database="mydb"
)
mycursor = mydb.cursor()
    
def sendPST():
    # Mendapatkan waktu sekarang
    timenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ## Cek id_st terakhir

    mycursor.execute("SELECT id_st FROM data_speedtest ORDER BY id_st DESC LIMIT 1")
    id_speedtest = mycursor.fetchall()
    # Jika data pada tabel kosong
    if (len(id_speedtest) == 0):
        id_speedtest = 1
    # Jika data ada pada tabel
    else:
        id_speedtest = id_speedtest[0]
        id_speedtest = list(id_speedtest)
        id_speedtest = id_speedtest[0]
        id_speedtest = int(id_speedtest)
        id_speedtest += 1

    ## Cek ping

    # Inisialisasi list untuk proses ping
    txtPingStat = []
    ip = []
    byte = []   
    times = []
    ttl = []
    id_st = []
    
    # Get ping
    cekPing = os.popen('ping www.google.com -n 10').read()
    # Membuat list untuk data ping dan ping statistics
    txtPing = cekPing.split('\n')
    # Jika tidak terdapat koneksi
    if 'Ping request could not find host' in txtPing[0]:

        ## Proses Ping

        for i in range(10):
            ip.append('Time Out')
            byte.append('None')
            times.append('None')
            ttl.append('None')
            id_st.append(id_speedtest)

        ## Proses Ping Statistics

        ipS = 'Time Out'
        packetS = 'None'
        packetR = 'None'
        packetL = 'None'
        packetMN = 'None'
        packetMX = 'None'
        packetAV = 'None'
    
    # Jika terdapat koneksi
    else:
        for i in range(len(txtPing)-5, len(txtPing)):
            txtPingStat.append(txtPing[i])
        del txtPingStat[-1:]
        del txtPing[0:2]
        del txtPing[-6:]

        ## Proses Ping
        
        for i in range(len(txtPing)):
            # Mendapatkan data ip
            koor = txtPing[i].find(':')
            koorIP = txtPing[i][0:koor]
            koor = koorIP.find('from')
            vIP = koorIP[koor:]
            vIP = list(vIP)
            vIP[0:5] = ''
            vIP = ''.join(vIP)
            ip.append(vIP)
            # Mendapatkan data byte
            koor = txtPing[i].find('time')
            koorByte = txtPing[i][0:koor]
            koor = koorByte.find('bytes')
            vByte = koorByte[koor:]
            vByte = list(vByte)
            vByte[0:6] = ''
            vByte[-1:] = ''
            vByte = ''.join(vByte)
            byte.append(vByte)
            # Mendapatkan data time
            koor = txtPing[i].find('TTL')
            koorTime = txtPing[i][0:koor]
            koor = koorTime.find('time')
            vTime = koorTime[koor:]
            vTime = list(vTime)
            vTime[0:5] = ''
            vTime[-1:] = ''
            vTime = ''.join(vTime)
            times.append(vTime)       
            # Mendapatkan data TTL
            koor = txtPing[i].find('TTL')
            vTTL = txtPing[i][koor:]
            vTTL = list(vTTL)
            vTTL[0:4] = ''
            vTTL = ''.join(vTTL)
            ttl.append(vTTL)
            # Memasukkan data id_st
            id_st.append(id_speedtest)


        ## Proses Ping Statistics

        # Mendapatkan data ip
        ipS = txtPingStat[0]
        koor = ipS.find('for')
        ipS = ipS[koor:]
        ipS = list(ipS)
        ipS[0:4] = ''
        ipS[-1:] = ''
        ipS = ''.join(ipS)
        # Mendapatkan data packet send
        packetS = txtPingStat[1]
        koor = packetS.find('Received')
        koorPS = packetS[0:koor]
        koor = koorPS.find('Sent')
        packetS = koorPS[koor:]
        packetS = list(packetS)
        packetS[0:7] = ''
        packetS[-2:] = ''
        packetS = ''.join(packetS)
        # Mendapatkan data packet received
        packetR = txtPingStat[1]
        koor = packetR.find('Lost')
        koorPR = packetR[0:koor]
        koor = koorPR.find('Received')
        packetR = koorPR[koor:]
        packetR = list(packetR)
        packetR[0:11] = ''
        packetR[-2:] = ''
        packetR = ''.join(packetR)
        # Mendapatkan data packet lost
        packetL = txtPingStat[1]
        koor = packetL.find('Lost')
        packetL = packetL[koor:]
        packetL = list(packetL)
        packetL[0:7] = ''
        packetL[-1:] = ''
        packetL = ''.join(packetL)
        # Mendapatkan data RTT minimum
        packetMN = txtPingStat[3]
        koor = packetMN.find('Minimum')
        koorMN = packetMN[koor:]
        koor = koorMN.find('Maximum')
        packetMN = koorMN[0:koor]
        packetMN = list(packetMN)
        packetMN[0:10] = ''
        packetMN[-2:] = ''
        packetMN = ''.join(packetMN)
        # Mendapatkan data RTT maximum
        packetMX = txtPingStat[3]
        koor = packetMX.find('Maximum')
        koorMX = packetMX[koor:]
        koor = koorMX.find('Average')
        packetMX = koorMX[0:koor]
        packetMX = list(packetMX)
        packetMX[0:10] = ''
        packetMX[-2:] = ''
        packetMX = ''.join(packetMX)
        # Mendapatkan data RTT average
        packetAV = txtPingStat[3]
        koor = packetAV.find('Average')
        packetAV = packetAV[koor:]
        packetAV = list(packetAV)
        packetAV[0:10] = ''
        packetAV = ''.join(packetAV)

    # Membuat df Ping
    dfP = pd.DataFrame()
    dfP['ip'] = ip
    dfP['bytes'] = byte
    dfP['time'] = times
    dfP['ttl'] = ttl
    # Mengubah data jika Time Out
    for i in range(len(dfP)):
        if(dfP.loc[i].time == " ou"):
            dfP.loc[i].ip = "Time Out"
            dfP.loc[i].bytes = "None"
            dfP.loc[i].time = "None"
            dfP.loc[i].ttl = "None"

    # Get speedtest
    speed = os.popen("speedtest-cli --csv").read()
    speedtest = speed.split('\n')

    ## Proses Speedtest

    # Jika tidak terdapat koneksi
    if(speedtest[0] == ''):
        serverID = 'Time Out'
        sponsor = 'None'
        serverName = 'None'
        timespan = timenow
        distance = 'None'
        pingSp = 'None'
        download = 'None'
        upload = 'None'
        IPadr = 'None'
    # Jika terdapat koneksi
    else:
        # Mengolah data Speedtest
        dataS = speedtest[0].split(',')
        serverID = dataS[0]
        sponsor = dataS[1]
        serverName = dataS[2]
        timespan = dataS[3]
        distance = dataS[4]
        pingSp = dataS[5]
        download = dataS[6]
        upload = dataS[7]
        IPadr = dataS[9]
        # Mengubah nilai Download dan Upload kedalam MB dan membulatkan 2 angka desimal
        temp = download
        temp = float(temp)
        temp = temp/8e+6
        temp = round(temp, 2)
        temp = str(temp)
        download = temp
        temp = upload
        temp = float(temp)
        temp = temp/8e+6
        temp = round(temp, 2)
        temp = str(temp)
        upload = temp   
        # Menghapus milisecond pada data timespan dan menambahkan hr + 7
        temp = timespan
        temp = list(temp)
        temp[-8:] = ''
        temp[10] = ' '
        temp[0] += temp[1] + temp[2] + temp[3]
        del temp[1:4]
        temp[2] += temp[3]
        del temp[3]
        temp[4] += temp[5]
        del temp[5]
        temp[6] += temp[7]
        del temp[7]
        jam = temp[6]
        jam = int(jam)
        hari = temp[4]
        hari = int(hari)
        bulan = temp[2]
        bulan = int(bulan)
        tahun = temp[0]
        tahun = int(tahun)
        jam += 7
        if(jam >= 24):
            jam -= 24
            hari += 1
            if ((bulan == 1) or (bulan == 3) or (bulan == 5) or (bulan == 7) or (bulan == 8) or (bulan == 10) or (bulan == 12)) and (hari > 31):
                hari -= 31
                bulan += 1
            if ((bulan == 4) or (bulan == 6) or (bulan == 9) or (bulan == 11)) and (hari > 30):
                hari -= 30
                bulan += 1
            if (bulan == 2) and (hari > 28):
                hari -= 28
                bulan += 1
            if (bulan > 12):
                bulan -= 12
                tahun += 1
        jam = str(jam)
        if(len(jam) == 1):
            jam = '0'+ jam
        temp[6] = jam
        hari = str(hari)
        if(len(hari) == 1):
            hari = '0'+ hari
        temp[4] = hari
        bulan = str(bulan)
        if(len(bulan) == 1):
            bulan = '0'+ bulan
        temp[2] = bulan
        tahun = str(tahun)
        temp[0] = tahun
        temp = ''.join(temp)
        timespan = temp

    ## Proses insert df ke MySQL

    sql = "INSERT INTO data_speedtest (serverId, sponsor, serverName, distance, ping, download, upload, ip, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (serverID, sponsor, serverName, distance, pingSp, download, upload, IPadr, timespan)
    mycursor.execute(sql, val)
    sql1 = "INSERT INTO data_pingstatistics (ip, packetSend, packetReceived, packetLoss, packetMinimum, packetMaximum, packetAverage, id_st) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val1 = (ipS, packetS, packetR, packetL, packetMN, packetMX, packetAV, id_speedtest)
    mycursor.execute(sql1, val1)
    mydb.commit()
    for i in range(len(dfP)):
        sql = "INSERT INTO data_ping (ip, bytes, time, ttl, id_st) VALUES (%s, %s, %s, %s, %s)"
        val = (dfP['ip'][i], dfP['bytes'][i], dfP['time'][i], dfP['ttl'][i], id_st[i])
        mycursor.execute(sql, val)
        mydb.commit()
        
add_to_startup()
sendPST()

## Proses Scheduling

schedule.every(1).minutes.do(sendPST)
while True: 
    schedule.run_pending()