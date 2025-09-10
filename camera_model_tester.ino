#include "esp_camera.h"
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

struct CameraModel {
  const char* name;
  int pwdn_gpio;
  int reset_gpio;
  int xclk_gpio;
  int siod_gpio;
  int sioc_gpio;
  int y9_gpio;
  int y8_gpio;
  int y7_gpio;
  int y6_gpio;
  int y5_gpio;
  int y4_gpio;
  int y3_gpio;
  int y2_gpio;
  int vsync_gpio;
  int href_gpio;
  int pclk_gpio;
};

// Define different camera models
CameraModel models[] = {
  // AI Thinker (Most Common)
  {"AI_THINKER", 32, -1, 0, 26, 27, 35, 34, 39, 36, 21, 19, 18, 5, 25, 23, 22},
  
  // M5Stack variants
  {"M5STACK_PSRAM", -1, 15, 27, 25, 23, 19, 36, 18, 39, 5, 34, 35, 32, 22, 26, 21},
  {"M5STACK_WIDE", -1, 15, 27, 22, 23, 19, 36, 18, 39, 5, 34, 35, 32, 25, 26, 21},
  
  // WROVER KIT
  {"WROVER_KIT", -1, -1, 21, 26, 27, 35, 34, 39, 36, 19, 18, 5, 4, 25, 23, 22},
  
  // ESP EYE
  {"ESP_EYE", -1, -1, 4, 18, 23, 36, 37, 38, 39, 35, 14, 13, 34, 5, 27, 25},
  
  // TTGO T-Journal
  {"TTGO_T_JOURNAL", 0, 15, 27, 25, 23, 19, 36, 18, 39, 5, 34, 35, 17, 22, 26, 21}
};

int num_models = sizeof(models) / sizeof(models[0]);

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout
  
  Serial.begin(115200);
  delay(2000);
  
  Serial.println("\n\n========================================");
  Serial.println("ESP32-CAM Model Auto-Detection Tool");
  Serial.println("========================================\n");
  Serial.println("This tool will test different camera configurations");
  Serial.println("to identify your ESP32-CAM board model.\n");
  
  bool camera_found = false;
  
  for(int i = 0; i < num_models; i++) {
    Serial.printf("\n[%d/%d] Testing model: %s\n", i+1, num_models, models[i].name);
    Serial.println("----------------------------------------");
    
    // Power cycle if PWDN pin is available
    if(models[i].pwdn_gpio >= 0) {
      pinMode(models[i].pwdn_gpio, OUTPUT);
      digitalWrite(models[i].pwdn_gpio, HIGH);
      delay(100);
      digitalWrite(models[i].pwdn_gpio, LOW);
      delay(100);
    }
    
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = models[i].y2_gpio;
    config.pin_d1 = models[i].y3_gpio;
    config.pin_d2 = models[i].y4_gpio;
    config.pin_d3 = models[i].y5_gpio;
    config.pin_d4 = models[i].y6_gpio;
    config.pin_d5 = models[i].y7_gpio;
    config.pin_d6 = models[i].y8_gpio;
    config.pin_d7 = models[i].y9_gpio;
    config.pin_xclk = models[i].xclk_gpio;
    config.pin_pclk = models[i].pclk_gpio;
    config.pin_vsync = models[i].vsync_gpio;
    config.pin_href = models[i].href_gpio;
    config.pin_sccb_sda = models[i].siod_gpio;
    config.pin_sccb_scl = models[i].sioc_gpio;
    config.pin_pwdn = models[i].pwdn_gpio;
    config.pin_reset = models[i].reset_gpio;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    config.frame_size = FRAMESIZE_QVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
    config.fb_location = CAMERA_FB_IN_DRAM;
    config.grab_mode = CAMERA_GRAB_LATEST;
    
    // Try initialization
    esp_err_t err = esp_camera_init(&config);
    
    if (err != ESP_OK) {
      Serial.printf("✗ Failed with error 0x%x\n", err);
      
      // Try with lower frequency
      if(err == ESP_ERR_NOT_SUPPORTED) {
        Serial.println("  Retrying with 10MHz XCLK...");
        config.xclk_freq_hz = 10000000;
        err = esp_camera_init(&config);
        
        if(err != ESP_OK) {
          Serial.printf("  ✗ Still failed with error 0x%x\n", err);
        }
      }
    }
    
    if (err == ESP_OK) {
      Serial.println("✓✓✓ SUCCESS! Camera initialized!");
      camera_found = true;
      
      // Get sensor information
      sensor_t * s = esp_camera_sensor_get();
      Serial.printf("\nCamera Sensor PID: 0x%02X\n", s->id.PID);
      
      // Take a test photo
      camera_fb_t * fb = esp_camera_fb_get();
      if(fb) {
        Serial.printf("Test photo captured: %d bytes\n", fb->len);
        esp_camera_fb_return(fb);
      }
      
      Serial.println("\n========================================");
      Serial.println("RESULT: Your board matches:");
      Serial.printf("Model: %s\n", models[i].name);
      Serial.println("========================================");
      Serial.println("\nTo use this configuration:");
      Serial.println("1. Open board_config.h");
      Serial.printf("2. Comment out: #define CAMERA_MODEL_AI_THINKER\n");
      Serial.printf("3. Uncomment: #define CAMERA_MODEL_%s\n", models[i].name);
      Serial.println("\nPin Configuration:");
      Serial.printf("PWDN: %d, RESET: %d, XCLK: %d\n", 
                    models[i].pwdn_gpio, models[i].reset_gpio, models[i].xclk_gpio);
      Serial.printf("SIOD: %d, SIOC: %d\n", models[i].siod_gpio, models[i].sioc_gpio);
      Serial.printf("Y9-Y2: %d,%d,%d,%d,%d,%d,%d,%d\n",
                    models[i].y9_gpio, models[i].y8_gpio, models[i].y7_gpio, 
                    models[i].y6_gpio, models[i].y5_gpio, models[i].y4_gpio,
                    models[i].y3_gpio, models[i].y2_gpio);
      Serial.printf("VSYNC: %d, HREF: %d, PCLK: %d\n", 
                    models[i].vsync_gpio, models[i].href_gpio, models[i].pclk_gpio);
      
      break;
    }
    
    delay(500);
  }
  
  if(!camera_found) {
    Serial.println("\n========================================");
    Serial.println("ERROR: No compatible camera model found!");
    Serial.println("========================================");
    Serial.println("\nTroubleshooting steps:");
    Serial.println("1. Check camera ribbon cable connection:");
    Serial.println("   - Power off completely");
    Serial.println("   - Lift the black latch on the connector");
    Serial.println("   - Reinsert cable (contacts facing the board)");
    Serial.println("   - Press latch down firmly");
    Serial.println("\n2. Check power supply:");
    Serial.println("   - Use a quality USB cable");
    Serial.println("   - Try a powered USB hub");
    Serial.println("   - Or use external 5V power supply");
    Serial.println("\n3. The camera module may be faulty");
  }
}

void loop() {
  delay(10000);
} 
