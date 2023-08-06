#!/usr/bin/python3
import os, sys, platform, time
try:
    import requests
    import ip_address
except ImportError:
    #print('Grant Us Root To Auto Install Required Modules!.')
    os.system('pip3 install ip_address')
    os.system(f'python3 {os.path.basename(__file__)}')
    exit(0)

def clear():
    if(platform.system() == 'Windows'):
        os.system('cls')
    else:
        os.system('clear')


def banner():
    print("=========================")
    print(" __  _______             |")
    print(" \\ \\/ /_   _|            |")
    print("  >  <  | |              |")
    print(" /_/\\_\\ |_|              |")
    print("                         |")
    print("X-Tracer By: Anikin Luke |")
    print("-------------------------|")
    print("Your Ip: {}".format(ip_address.get()))
    print("=========================|")

def selections():
    user_input = input("Select~> ")
    if(user_input == '0'):
        os._exit(0)
    elif(user_input == '1'):
        ip = input("Enter IP: ")
        print(trace.ip_trace(ip))
    else:
        print('Error!')
        time.sleep(.3)
        clear()
        trace.menu()


def menu():
    banner()
    print("[1] ==> (IP Tracer)      ")
    print("[2] ==> ()               ")
    print("[0] ==> (Exit)           ")
    print("=========================")
    try:
        selections()
    except KeyboardInterrupt:
        print('Exiting..')
        os._exit(0)

class Tracer:
    def ip_trace(self, ip):
        req = requests.get(f"http://ip-api.com/json/{ip}")
        ip_data = req.json()
        content = f"""
  IP: {ip_data['query']}
  Country: {ip_data['country']}
  country code: {ip_data['countryCode']}
  region: {ip_data['region']}
  Region Name: {ip_data['regionName']}
  City: {ip_data['city']}
  zip code: {ip_data['zip']}
  time zone: {ip_data['timezone']}
  ISP: {ip_data['isp']}
  org: {ip_data['org']}
  as: {ip_data['as']}
  latitude: {ip_data['lat']}
  longitude: {ip_data['lon']}"""
        return content


if __name__=='__main__':
    trace = Tracer()
    menu()
