# Optional Hardware Version

The cloud architecture is intentionally hardware-agnostic. Replace the Python simulator with an ESP32 that sends the same JSON fields.

## Components
- ESP32 DevKit
- capacitive soil moisture sensor
- DHT11/DHT22
- optional LDR/light sensor
- low-voltage relay module/driver
- suitable low-voltage mini pump and power supply
- tubing/reservoir

## Wiring concept
Use 3.3V-compatible sensors where appropriate. Connect analog soil moisture output to an ESP32 ADC input; DHT data to a digital GPIO; LDR through an appropriate voltage-divider/ADC circuit. The relay control input goes to a GPIO. Power the pump from a separate suitable supply through a properly rated relay/driver.

**Safety:** never connect mains voltage to an ESP32 GPIO or breadboard. Use only low-voltage educational hardware unless qualified electrical supervision and proper isolation are available.

The example sketch under `sensor_simulator/esp32/` sends telemetry over HTTPS. For a real production system, use per-device credentials/certificates and TLS validation rather than a shared demonstration key.
