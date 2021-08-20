class HttpResponse:
    status = 200
    server = None
    date = None
    contentType = None
    transferEncoding = None
    connection = None
    body = None

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status

    def setServer(self, server):
        self.status = server

    def getServer(self):
        return self.server

    def setDate(self, date):
        self.status = date

    def getDate(self):
        return self.date

    def setContentType(self, contentType):
        self.status = contentType

    def getContentType(self):
        return self.contentType

    def setTransferEncoding(self, transferEncoding):
        self.status = transferEncoding

    def getTransferEncoding(self):
        return self.transferEncoding

    def setConnection(self, connection):
        self.status = connection

    def getConnection(self):
        return self.connection

    def setBody(self, body):
        self.status = body

    def getBody(self):
        return self.body


def parseUri(uri):
    uri = uri.replace("http://", "")
    uri = uri.replace("https://", "")
    sub = uri.split("/")
    host = sub[0].split(":")
    domain = host[0]
    port = "80"
    if(len(host) > 1):
        port = host[1]
    path = "/" + uri[len(sub[0]) + 1:]
    return domain, port, path


def response_decode(str):
    strs = str.split("\r\n\r\n")
    if(len(strs) < 2):
        return None

    response = HttpResponse()
    bodys = strs[1].split("\r\n", 1)
    response.body = bodys[1]

    attrs = strs[0].split("\r\n")
    for attr in attrs:
        attr = attr.replace(":", "")
        sp = attr.split(" ", 1)
        if(sp[0] == "HTTP/1.1"):
            sp1 = sp[1].split(" ")
            response.status = int(sp1[0])
        elif(sp[0] == "Server"):
            response.server = sp[1]
        elif(sp[0] == "Date"):
            response.date = sp[1]
        elif(sp[0] == "Content-Type"):
            response.contentType = sp[1]
        elif(sp[0] == "Transfer-Encoding"):
            response.transferEncoding = sp[1]
        elif(sp[0] == "Connection"):
            response.connection = sp[1]

    return response


def request(uri, method, para=None):
    import ujson
    import usocket
    domain, port, path = parseUri(uri)
    path = path.encode("utf-8")
    domain = domain.encode("utf-8")
    method = method.encode("utf-8")
    socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)

    sockaddr = usocket.getaddrinfo(domain, int(port))[0][-1]
    socket.connect(sockaddr)
    str = method + " " + path + b" HTTP/1.1\r\n"
    str += b"Host: " + domain + b"\r\n"
    str += b"Connection: close\r\n"
    str += b"Cache-Control: max-age=0\r\n"
    str += b"sec-ch-ua: \"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Microsoft Edge\";v=\"92\\r\n"
    str += b"sec-ch-ua-mobile: ?0\r\n"
    str += b"Upgrade-Insecure-Requests: 1\r\n"
    str += b"Accept: application/json\r\n"
    str += b"Sec-Fetch-Site: none\r\n"
    str += b"Sec-Fetch-Mode: navigate\r\n"
    str += b"Sec-Fetch-User: ?1\r\n"
    str += b"Sec-Fetch-Dest: document\r\n"
    str += b"Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n"
    str += b"\r\n"
    socket.send(str)
    if(method == "POST"):
        ujson.dumps(para, str)
        socket.send(str)

    socket.settimeout(5)
    datas = socket.read()
    datas = datas.decode()
    resp = response_decode(datas)
    return resp


def parseWeater(str):
    import ujson
    parsed = ujson.loads(str[0:-1])
    return parsed


def weather():
    while True:
        print("Please input your city: ")
        cityid = input()
        if(cityid == "quit" or cityid == "exit"):
            break
        else:
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


if __name__ == '__main__':
    weather()
