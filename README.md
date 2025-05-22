# OpenTheDoorByLAN

English | [简体中文](README_ZH.md)

A small invention that attaches to a physical door lock to enable remote control without replacing the existing lock. Designed for dormitories, shared apartments, and other scenarios where hardware replacement is impractical.

**Key Features:**
- Remote door opening via Wi-Fi
- No physical modification to the existing lock required
- Simple web interface for control
- Emergency solution for forgotten keys

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Hardware Requirements
- ESP8266 microcontroller
- Micro servo motor (SG90 recommended)
- 3D printed or crafted mechanical attachment for door handle
- Power source (USB or battery)

## Software Requirements
- MicroPython firmware

## Installation
1. Flash MicroPython firmware to your ESP8266
2. Upload `main.py` to the device
3. Connect servo to GPIO14
4. Connect status LED to GPIO2 (optional)

## Usage
1. Power on the device
2. Connect to the same Wi-Fi network as configured in the code
3. Open a web browser and navigate to the device's IP address
4. Use the web interface to control the door handle

**Web Interface Features:**
- One-button control (rotate/restore)
- 3-second auto-restore function (C version)
- Multiple control buttons (Python version)

## Configuration
Edit the following parameters in the code:
```python
ssid = "My Router WiFi"   # Your Wi-Fi SSID
passwd = "12345678"       # Your Wi-Fi password
servo_pin = 14            # GPIO pin for servo
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## Acknowledgements
- Developed by KARkitkat
- Inspired by real-life dormitory lockout situations
- Thanks to the open-source community for ESP8266 and MicroPython resources

---

*"Never get locked out again!"* 🔑➡️📶