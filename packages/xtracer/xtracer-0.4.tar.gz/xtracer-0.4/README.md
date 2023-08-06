# X-Tracer
## Multi Tracing Tool
### Example 1 for python3 file or python3 console
#### **`ip_trace()`** Example
```py
>> from xtracer import Tracer
>> trace = Tracer()
>> ip_info = trace.ip_trace('142.250.185.78')
>> print(ip_info)
  IP: 142.250.185.78
  Country: Germany
  country code: DE
  region: HE
  Region Name: Hesse
  City: Frankfurt am Main
  zip code: 60313
  time zone: Europe/Berlin
  ISP: Google LLC
  org: Google LLC
  as: AS15169 Google LLC
  latitude: 50.1109
  longitude: 8.68213
>>
```
.
#### **`mac_trace()`** Example
```py
>>
```

### Example 2 for terminal/cmd
```console
~$ python3 -m xtracer

=========================
 __  _______             |
 \ \/ /_   _|            |
  >  <  | |              |
 /_/\_\ |_|              |
                         |
X-Tracer By: Anikin Luke |
-------------------------|
Your Ip: 142.250.185.78
=========================|
[1] ==> (IP Tracer)
[2] ==> (MAC Tracer)
[0] ==> (Exit)
=========================
Select~>
```
## Installation
```
python3 -m pip install xtracer
```
or
```
pip3 install xtracer
```
**X-Tracer** only supports python3


## Info
Number of tracers: 2
> Tracers list:
> * ip_trace('<target_ip>')
> * mac_trace('<target_mac>')