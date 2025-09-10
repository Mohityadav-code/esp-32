// ESP32-CAM Standalone Capture Logger (no WiFi/BLE)
// Purpose: isolate camera from WiFi/BLE, avoid power cycling, and print detailed logs

#include "esp_camera.h"
#include <WiFi.h>
#include "esp_log.h"
#include "esp_bt.h"

// AI-THINKER pin map
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

static const char* TAG = "standalone";

// Current camera configuration (will be initialized once)
bool camera_ok = false;
bool using_grayscale = false;

// Build a conservative config for DVP sensors
static void build_config(camera_config_t& config, bool grayscale) {
  memset(&config, 0, sizeof(config));
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
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;

  // Slow XCLK and tiny frame to minimize DMA pressure
  config.xclk_freq_hz = 8000000;      // 8 MHz
  config.frame_size   = FRAMESIZE_QQVGA;  // 160x120
  config.pixel_format = grayscale ? PIXFORMAT_GRAYSCALE : PIXFORMAT_RGB565;
  config.jpeg_quality = 12;
  config.fb_count     = 1;
  config.fb_location  = CAMERA_FB_IN_DRAM;   // Avoid PSRAM path first
  config.grab_mode    = CAMERA_GRAB_LATEST;  // Prevent queue growth
}

static void print_sensor_id(sensor_t* s) {
  if (!s) return;
  ESP_LOGI(TAG, "Sensor IDs: PID=0x%04X VER=0x%02X MIDH=0x%02X MIDL=0x%02X",
           s->id.PID, s->id.VER, s->id.MIDH, s->id.MIDL);
}

static void dump_env() {
  ESP_LOGI(TAG, "CPU freq: %d MHz", getCpuFrequencyMhz());
  ESP_LOGI(TAG, "Free heap: %u", (unsigned)ESP.getFreeHeap());
  ESP_LOGI(TAG, "PSRAM present: %s, size=%u, free=%u",
           psramFound() ? "yes" : "no",
           (unsigned)ESP.getPsramSize(), (unsigned)ESP.getFreePsram());
}

static bool init_camera_sequence() {
  camera_config_t cfg;

  // Try RGB565 first
  build_config(cfg, false);
  ESP_LOGI(TAG, "Init attempt #1: RGB565, 8MHz, QQVGA");
  esp_err_t err = esp_camera_init(&cfg);
  if (err == ESP_OK) {
    sensor_t* s = esp_camera_sensor_get();
    print_sensor_id(s);
    using_grayscale = false;
    return true;
  }
  ESP_LOGE(TAG, "esp_camera_init RGB565 failed: 0x%x (%s)", err, esp_err_to_name(err));

  // Fallback to GRAYSCALE
  build_config(cfg, true);
  ESP_LOGI(TAG, "Init attempt #2: GRAYSCALE, 8MHz, QQVGA");
  err = esp_camera_init(&cfg);
  if (err == ESP_OK) {
    sensor_t* s = esp_camera_sensor_get();
    print_sensor_id(s);
    using_grayscale = true;
    return true;
  }
  ESP_LOGE(TAG, "esp_camera_init GRAYSCALE failed: 0x%x (%s)", err, esp_err_to_name(err));

  return false;
}

void setup() {
  Serial.begin(115200);
  delay(2000);

  // Maximize logs from camera stack to understand failures
  esp_log_level_set("*", ESP_LOG_INFO);
  esp_log_level_set("sccb", ESP_LOG_DEBUG);
  esp_log_level_set("camera", ESP_LOG_DEBUG);
  esp_log_level_set(TAG, ESP_LOG_DEBUG);

  // Ensure radios are fully off
  WiFi.mode(WIFI_OFF);
  btStop();

  ESP_LOGI(TAG, "=== ESP32-CAM Standalone Capture Logger ===");
  dump_env();

  // Avoid power cycling between attempts; keep camera powered
  pinMode(PWDN_GPIO_NUM, OUTPUT);
  digitalWrite(PWDN_GPIO_NUM, LOW);   // Power ON

  camera_ok = init_camera_sequence();
  if (!camera_ok) {
    ESP_LOGE(TAG, "Camera init failed in both modes. Capture will fail.");
  } else {
    ESP_LOGI(TAG, "Camera init OK (%s)", using_grayscale ? "GRAYSCALE" : "RGB565");
  }

  // If sensor available, print extra status and set smallest framesize again explicitly
  sensor_t* s = esp_camera_sensor_get();
  if (s) {
    print_sensor_id(s);
    s->set_framesize(s, FRAMESIZE_QQVGA);
    // Optionally try enabling colorbar to see if sensor path works
    ESP_LOGI(TAG, "Colorbar OFF");
    if (s->set_colorbar) s->set_colorbar(s, 0);
  }

  ESP_LOGI(TAG, "Starting periodic capture loop... (no WiFi, no BLE, no power-down)");
}

void loop() {
  static uint32_t attempt = 0;
  attempt++;

  ESP_LOGI(TAG, "Capture attempt %u", (unsigned)attempt);
  uint32_t t0 = millis();
  camera_fb_t* fb = esp_camera_fb_get();
  uint32_t dt = millis() - t0;

  if (!fb) {
    ESP_LOGE(TAG, "fb==NULL (timeout or not supported), elapsed=%ums", (unsigned)dt);

    // Try one time with test pattern to verify the pixel path
    sensor_t* s = esp_camera_sensor_get();
    if (s && s->set_colorbar) {
      ESP_LOGW(TAG, "Enabling test pattern and retrying once...");
      s->set_colorbar(s, 1);
      delay(300);
      t0 = millis();
      fb = esp_camera_fb_get();
      dt = millis() - t0;
      if (fb) {
        ESP_LOGI(TAG, "Test-pattern capture OK: %dx%d len=%u bytes in %ums",
                 fb->width, fb->height, (unsigned)fb->len, (unsigned)dt);
        esp_camera_fb_return(fb);
      } else {
        ESP_LOGE(TAG, "Test-pattern capture failed as well, elapsed=%ums", (unsigned)dt);
      }
      s->set_colorbar(s, 0);
    }
  } else {
    ESP_LOGI(TAG, "Capture OK: %dx%d len=%u bytes, fmt=%s, elapsed=%ums",
             fb->width, fb->height, (unsigned)fb->len,
             (using_grayscale ? "GRAYSCALE" : "RGB565"), (unsigned)dt);
    esp_camera_fb_return(fb);
  }

  // Short pause between attempts to keep logs readable
  delay(1500);
}