import urllib.request
import json
import configparser
import os


def YibanCheckin():
    username = input('Username: ')
    password = input('Password: ')
    print('Login......',end='')
    url = 'https://mobile.yiban.cn/api/v2/passport/login?v=9.9.9&ct=99&account=' + urllib.request.quote(username) + '&passwd=' + urllib.request.quote(password)  #+'&app=0&apn=wifi&identify=123456789&sig=a47a6db4540b4e7e&token=&device=unknown%3Aunknown&sversion=28'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        json_data = data.decode()
    if '\\u8bf7\\u6c42\\u6210\\u529f' in json_data: #请求成功
        print('Success!')
        config = configparser.ConfigParser()
        config.read('option.ini')
        if(config.has_section(username) == False):
            back = ''
            while back not in ['Y','N']:
                back = input('Save your user&pass? Press Y or N.').upper()
                if(back == 'Y'):
                    config.add_section(username)
                    config.set(username,'password',password)
                    with open('option.ini','w+') as f:
                        config.write(f)
                    break
                elif(back == 'N'):
                    break
        else:
            if(config.get(username,'password') != password):
                config.set(username,'password',password)
                with open('option.ini','w+') as f:
                    config.write(f)
        json_data = json.loads('%s' % json_data)
        json_data = json_data['data']
        token = json_data['access_token']
        print('token: ' + token)
        json_data = json_data['user']
        print("name: " + json_data['name'])
#        url = 'http://mobile.yiban.cn/api/v3/checkin/question?access_token=' + token
#        print('Question...',end='')
#        req = urllib.request.Request(url)
#        with urllib.request.urlopen(req) as response:
#            data = response.read()
#            json_data = data.decode()
#        if json_data.find('\\u8bf7\\u6c42\\u6210\\u529f') > 0: #请求成功
#            print('Success!')
#            json_data = json.loads('%s' % json_data)
#            json_data = json_data['data']
#            if json_data['isChecked'] is True:
#                print('\n\n[You have already cheakin!!!]')
#                exit(0)
#            if('survey' not in json_data):
#                print('[WRONG!!]')
#                exit(0)
#            json_data = json_data['survey']
#            json_data = json_data['question']
#            print('id: ' + json_data['id'],'title: ' + json_data['title'])
#            json_data = json_data['option']
#            id = json_data[0]['id']
#            print('Checkin......',end='')
        url = 'http://mobile.yiban.cn/api/v3/checkin/answer?access_token=' + token + '&optionId=666666' #+ id
        req = urllib.request.Request(url,data={})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            json_data = data.decode()
        if '\\u8bf7\\u6c42\\u6210\\u529f' in json_data:
            json_data = json.loads('%s' % json_data)
            json_data = json_data['data']
            if 'money' in json_data:
                print('\n\n[Success!!]')
            else:
                print('\n\n[You have already cheakin!!!]')
            os.system('pause')
            exit(0)
    print('Fail!')
    json_data = json.loads('%s' % json_data)
    print(json_data)

def YibanCheckin_Auto():
    config = configparser.ConfigParser()
    config.read('option.ini')
    success = 0
    fail = 0
    i = 0
    for username in config.sections():
        i+=1
        print(i,username,end=' ')
        password = config.get(username,'password')
        url = 'https://mobile.yiban.cn/api/v2/passport/login?account=' + urllib.request.quote(username) + '&passwd=' + urllib.request.quote(password) + '&v=9.9.9&ct=99' #+'&ct=0&app=0&v=4.6.13&apn=wifi&identify=123456789&sig=a47a6db4540b4e7e&token=&device=unknown%3Aunknown&sversion=28'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            json_data = data.decode()
        if '\\u8bf7\\u6c42\\u6210\\u529f' in json_data: #请求成功
            json_data = json.loads('%s' % json_data)
            json_data = json_data['data']
            token = json_data['access_token']
            json_data = json_data['user']
            print(json_data['name'],end=' ')
#            url = 'http://mobile.yiban.cn/api/v3/checkin/question?access_token=' + token
#            req = urllib.request.Request(url)
#            with urllib.request.urlopen(req) as response:
#                data = response.read()
#                json_data = data.decode()
#            if '\\u8bf7\\u6c42\\u6210\\u529f' in json_data: #请求成功
#                json_data = json.loads('%s' % json_data)
#                json_data = json_data['data']
#                if json_data['isChecked'] is True:
#                    print('[Already cheakin!!]')
#                    fail+=1
#                    continue
#                if('survey' not in json_data):
#                    print('[WRONG!!]')
#                    fail+=1
#                    continue
#                json_data = json_data['survey']
#                json_data = json_data['question']
#                json_data = json_data['option']
#                id = json_data[0]['id']
            url = 'http://mobile.yiban.cn/api/v3/checkin/answer?access_token=' + token + '&optionId=666666' #+ id
            req = urllib.request.Request(url,data={})
            with urllib.request.urlopen(req) as response:
                data = response.read()
                json_data = data.decode()
            if '\\u8bf7\\u6c42\\u6210\\u529f' in json_data:
                json_data = json.loads('%s' % json_data)
                json_data = json_data['data']
                if 'money' in json_data:
                    print('[Success!!]')
                    success+=1
                else:
                    print('[You have already cheakin!!!]')
                    fail+=1
                continue
        print('[Fail!] ',end='')
        json_data = json.loads('%s' % json_data)
        print(json_data)
        fail+=1
    print('\n\nAll done!!All:',i,'Success:',success,'Fail:',fail)

print('**********  Created By Avenshy  **********\nVer 0.3dev')
try:
    f = open('option.ini')
    f.close()
except IOError:
    YibanCheckin()
    exit(0)
back = ''
while back not in ['Y','N']:
    back = input('Auto mode? Press Y or N.').upper()
    if(back == 'Y'):
        YibanCheckin_Auto()
        os.system('pause')
        exit(0)
    elif(back == 'N'):
        YibanCheckin()
        os.system('pause')
        exit(0)