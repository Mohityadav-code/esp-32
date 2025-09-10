#include "esp_camera.h"
#include "soc/soc.h"           // Disable brownout problems
#include "soc/rtc_cntl_reg.h"  // Disable brownout problems

// AI Thinker ESP32-CAM Pin definition
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

#define LED_GPIO_NUM       4

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout detector
  
  Serial.begin(115200);
  Serial.println("\n\n===================================");
  Serial.println("ESP32-CAM Camera Diagnostic Tool");
  Serial.println("===================================\n");
  
  // Initialize LED
  pinMode(LED_GPIO_NUM, OUTPUT);
  digitalWrite(LED_GPIO_NUM, LOW);
  
  // Power cycle the camera
  Serial.println("Power cycling camera module...");
  pinMode(PWDN_GPIO_NUM, OUTPUT);
  digitalWrite(PWDN_GPIO_NUM, HIGH);
  delay(500);
  digitalWrite(PWDN_GPIO_NUM, LOW);
  delay(500);
  
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 10;
  config.fb_count = 1;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_DRAM;
  
  // Try different clock frequencies
  int frequencies[] = {20000000, 10000000, 5000000};
  const char* freq_names[] = {"20MHz", "10MHz", "5MHz"};
  
  for(int i = 0; i < 3; i++) {
    Serial.printf("\nAttempting camera init with XCLK frequency: %s\n", freq_names[i]);
    config.xclk_freq_hz = frequencies[i];
    
    esp_err_t err = esp_camera_init(&config);
    
    if (err != ESP_OK) {
      Serial.printf("Camera init failed with error 0x%x", err);
      switch(err) {
        case ESP_ERR_NO_MEM:
          Serial.println(" - Out of memory");
          break;
        case ESP_ERR_NOT_FOUND:
          Serial.println(" - Camera not found (check connections)");
          break;
        case ESP_ERR_NOT_SUPPORTED:
          Serial.println(" - Camera not supported (wrong model or connection issue)");
          break;
        case ESP_ERR_INVALID_STATE:
          Serial.println(" - Invalid state");
          break;
        default:
          Serial.println(" - Unknown error");
      }
      
      if(i == 2) {
        Serial.println("\n=== DIAGNOSTIC SUMMARY ===");
        Serial.println("Camera initialization failed at all frequencies.");
        Serial.println("\nPossible causes:");
        Serial.println("1. Camera ribbon cable not properly connected");
        Serial.println("2. Insufficient power supply");
        Serial.println("3. Wrong camera model selected");
        Serial.println("4. Faulty camera module");
        Serial.println("\nRecommended actions:");
        Serial.println("1. Power off completely");
        Serial.println("2. Reseat camera ribbon cable");
        Serial.println("3. Use powered USB hub or external 5V supply");
        Serial.println("4. Try the alternate pin configuration sketch");
      }
    } else {
      Serial.println("✓ Camera initialized successfully!");
      
      // Get camera info
      sensor_t * s = esp_camera_sensor_get();
      Serial.println("\n=== Camera Information ===");
      Serial.printf("Camera PID: 0x%02X\n", s->id.PID);
      
      switch(s->id.PID) {
        case 0x26:
          Serial.println("Camera Model: OV2640");
          break;
        case 0x7F:
          Serial.println("Camera Model: OV7670");
          break;
        case 0x51:
          Serial.println("Camera Model: OV7725");
          break;
        case 0x36:
          Serial.println("Camera Model: OV3660");
          break;
        case 0x56:
          Serial.println("Camera Model: OV5640");
          break;
        default:
          Serial.printf("Unknown camera model: 0x%02X\n", s->id.PID);
      }
      
      // Test LED flash
      Serial.println("\nTesting LED flash...");
      for(int j = 0; j < 3; j++) {
        digitalWrite(LED_GPIO_NUM, HIGH);
        delay(200);
        digitalWrite(LED_GPIO_NUM, LOW);
        delay(200);
      }
      Serial.println("✓ LED flash working");
      
      // Take test photo
      Serial.println("\nTaking test photo...");
      camera_fb_t * fb = esp_camera_fb_get();
      if(!fb) {
        Serial.println("✗ Camera capture failed");
      } else {
        Serial.printf("✓ Photo taken! Size: %d bytes\n", fb->len);
        esp_camera_fb_return(fb);
      }
      
      Serial.println("\n=== SUCCESS ===");
      Serial.println("Camera is working properly!");
      Serial.printf("Optimal XCLK frequency: %s\n", freq_names[i]);
      
      return; // Exit if successful
    }
    
    delay(1000);
  }
}

void loop() {
  // Flash LED to indicate the sketch is running
  digitalWrite(LED_GPIO_NUM, HIGH);
  delay(1000);
  digitalWrite(LED_GPIO_NUM, LOW);
  delay(1000);
} 
