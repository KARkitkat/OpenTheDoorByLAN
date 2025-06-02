#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

const char* ssid = "FUCKnet";
const char* password = "2416*zDs$";

const int servoPin = 2; // 控制舵机的引脚
Servo servo; // 舵机对象

ESP8266WebServer server(80); // 创建Web服务器，监听端口80

const int initialAngle = 30; // 初始角度值
const int rotatedAngle = 180; // 旋转角度值
bool isRotated = false; // 是否旋转标志

unsigned long rotateTime = 0; // 旋转时间戳

void handleRoot() {
  String buttonText = isRotated ? "Restore" : "rotate";
  String html = "
<!DOCTYPE html>
<html>

<head>
    <meta charset=\'UTF-8\'>
    <title>网络servo开关服务器</title>
    <style>
        .button {
            font-size: 40px;
            padding: 10px 20px;
        }

        .powered-by {
            font-size: 18px;
            margin-top: 10px;
        }
    </style>
</head>

<body>
    <center>
        <h2>局域网开关</h2>
        <form>
            <button class=\"button\" name=\"servo\" value=\'ON\' type=\'submit\'> 🔑 </button>
            <button class=\"button\" name=\"servo\" value=\'OFF\' type=\'submit\'> 🔒 </button>
            <button class=\"button\" name=\"servo\" value=\'keepon\' type=\'submit\'> 🔓 </button>
        </form>
        <p class=\"powered-by\">Powered by KARkitkat</p>
    </center>
</body>

</html>
";
  server.send(200, "text/html", html);
}

void handleServo() {
  isRotated = !isRotated; // 切换旋转状态

  if (isRotated) {
    servo.write(rotatedAngle); // 旋转到指定角度
    rotateTime = millis(); // 记录旋转开始时间
  } else {
    servo.write(initialAngle); // 恢复到初始角度
  }

  server.sendHeader("Location", "/");
  server.send(303);
}

void setup() {
  pinMode(servoPin, OUTPUT); // 将舵机引脚设置为输出模式
  servo.attach(servoPin); // 将舵机对象附加到舵机引脚

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: " + WiFi.localIP().toString());

  server.on("/", handleRoot);
  server.on("/Servo", handleServo);

  server.begin();
  Serial.println("Server started");

  servo.write(initialAngle); // 初始角度
}

void loop() {
  server.handleClient();

  // 如果旋转时间超过5秒并且处于旋转状态，则恢复到初始角度
  if (isRotated && (millis() - rotateTime >= 3000)) {
    servo.write(initialAngle);
    isRotated = false;
  }
}

