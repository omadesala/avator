#!/usr/bin/env python
#encoding=utf-8

import wave
import urllib, urllib2, pycurl
import base64
import json
import wavrecord as wr
## get access token by api key & secret key

def get_token():

#App ID: 7558253
#API Key: Tkx5GNDTZ4yH3HA1UD8GTuz2
#Secret Key: 4bf377baf2fb82ef584abbd3f514f2fc
    apiKey = "Tkx5GNDTZ4yH3HA1UD8GTuz2"
    secretKey = "4bf377baf2fb82ef584abbd3f514f2fc"

    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;

    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    print json_data

    return json.loads(json_data)['access_token']

def dump_res(buf):
    print buf


## post audio to server
def use_cloud(token):
#    fp = wave.open('zmsk.wav', 'rb')
    fp = wave.open('output.wav', 'rb')

    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)

    cuid = "18:03:73:7c:3d:7b" #my xiaomi phone MAC
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=16000',
        'Content-Length: %d' % f_len
    ]

    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, dump_res)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform() #pycurl.perform() has no return val

if __name__ == "__main__":
    print("start rec ...")
    wr.recordwave()
    # wr.test()
    print("end rec ...")
    token = get_token()
    use_cloud(token)
