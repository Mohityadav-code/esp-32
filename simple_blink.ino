// Simple ESP32-CAM LED Blink Test
// This will blink the built-in flash LED to verify upload works

#define LED_BUILTIN 4  // Flash LED on GPIO 4

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.println("\n\n================================");
  Serial.println("ESP32-CAM Upload Test - SUCCESS!");
  Serial.println("================================");
  Serial.println("If you see this, upload worked!");
  Serial.println("LED should be blinking now...\n");
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("LED ON");
  delay(1000);
  
  digitalWrite(LED_BUILTIN, LOW);
  Serial.println("LED OFF");
  delay(1000);
} 
