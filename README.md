# RasPi PICO：Use rt-thread micropython package to get weather online

### Description

This project use raspi PICO and ESP8266 as hardware and use [RT-Thread MicroPython - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=RT-Thread.rt-thread-micropython) to develop the software to get weather by http request. 

### Embedded Software Configuration

#### Use RT-Thread Studio

* install the SDK of RP2040-RASPBERRYPI-PICO

  ![image-20210820142601496](C:/Users/RTT/Desktop/Test/figures/sdk.png)

* Create RT-Thread Project，select based on Development board--->RP2040-RASPBERRYPI-PICO

* Open RT-Thread Settings on your project，and add micropython, AT-Device packages

* Configure micropython

  Enable usocket and ujson, and turn up Heap size appropriately

  ![image-20210820142951434](C:/Users/RTT/Desktop/Test/figures/mp_conf.png)

* Configure AT_Device

* Enable ESP8266，and enable samples，input your SSID and password，then set the device name as "uart1"

  ![image-20210820143119457](C:/Users/RTT/Desktop/Test/figures/atdevice_conf.png)

* Enable components--->network--->AT commands

* Enable components--->Device Driver--->Using WiFi Framework

* Connect esp8266 to uart1 of Raspi pico

* build the project and download it to the Raspi

#### Use ENV

* clone rt-thread code

  ``` bash
  git clone https://github.com/RT-Thread/rt-thread.git
  ```

* Enter the bsp directory

  ``` bash
  cd rt-thread/bsp/raspberry-pico
  ```

* Open menuconfig，and configure RT-Thread, Please reference the last chapter [Use RT-Thread Studio]

  ``` bash
  scons --menuconfig
  ```

* update the software packages

  ``` bash
  pkgs --update
  ```

* compile

  ``` bash
  scons
  ```

### HTTP request process

* Create the socket, and connect to the http server. 

* send http request

  HTTP request consist of request line, headers, blank line, and request body. 

  > request line
  >
  > > consists of method, url, and http version.
  > >
  > > > request method: HTTP/1.1 defined the following 8 methods：GET/POST/PUT/DELETE/PATCH/HEAD/OPTIONS/TRACE
  > > >
  > > > url: the path to request
  > > >
  > > > version: HTTP/major version number.minor version number，such as HTTP/1.0 or HTTP/1.1
  > >
  > > eg：`GET /user/login HTTP/1.1`
  >
  > headers
  >
  > > The request header adds some additional information to the request message, one for each line, and each one is separated by ":"
  > >
  > > such as: 
  > >
  > > | Key             | Detail                                                       |
  > > | --------------- | ------------------------------------------------------------ |
  > > | Host            | Host of the server                                           |
  > > | User-Agent      | The User-Agent request header is a characteristic string that lets servers and network peers identify the application, operating system, vendor, and/or version of the requesting user agent. |
  > > | Connection      | The Connection general header controls whether or not the network connection stays open after the current transaction finishes. If the value sent is `keep-alive`, the connection is persistent and not closed, allowing for subsequent requests to the same server to be done. |
  > > | Accept-Encoding | The Accept-Encoding request HTTP header advertises which content encoding, usually a compression algorithm, the client is able to understand. Using content negotiation, the server selects one of the proposals, uses it and informs the client of its choice with the `Content-Encoding` response header. |
  > >
  > > eg：` Connection: keep-alive`
  >
  > blank line
  >
  > > This line only consists of `\r\n`
  >
  > request body
  >
  > > This part is used for the methods which need parameters such as POST. 

* receive Response

  Response consists of status line, headers, blank line, response body. 

* close the socket

### code implementation

Create RT-Thread MicroPython Project

define request:  `def request(uri, method, para=None):`

> decode the uri to domain, port and path.
>
> create the socket connection using usocket
>
> send  http request.
>
> receive response
>
> parse the response to class`HttpResponse` and return it.

Call `request()` to get the weather.

API interface: [免费实时天气接口API 实况天气api (yiketianqi.com)](https://yiketianqi.com/index/doc?version=day)

``` python
uri = "https://tianqiapi.com/free/day?appid=&appsecret="
uri += "&cityid=" + cityid
resp = request(uri, "GET")
parsed = parseWeater(resp.body)
if("errmsg" in parsed):
    print(parsed["errmsg"])
    continue
    print("cityid: " + parsed["cityid"])
    print("city: " + parsed["city"])
    print("update time: " + parsed["update_time"])
    print("weather: " + parsed["wea"])
    print("temparature: " +
          parsed["tem_night"] + "~" + parsed["tem_day"] + "C")
    print("current temparature: " + parsed["tem_day"] + "C")
    print("wind: " + parsed["win"] +
          parsed["win_speed"] + " " + parsed["win_meter"])
    print()
```

### Running Example

Get the weather of Beijing

![image-20210820133929156](C:\Users\RTT\Desktop\readme\figures\eg.png)

