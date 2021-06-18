#include <Wire.h>
#include <Adafruit_HMC5883_U.h>

HMC5883L compass;

int minX = 0;
int maxX = 0;
int minY = 0;
int maxY = 0;
int offX = 0;
int offY = 0;

void setup()
{
 Serial.begin(9600);

 // Initialize Initialize HMC5883L
 while (!compass.begin())
 {
   delay(500);
 }

 // Set measurement range
 compass.setRange(HMC5883L_RANGE_1_3GA);

 // Set measurement mode
 compass.setMeasurementMode(HMC5883L_CONTINOUS);

 // Set data rate
 compass.setDataRate(HMC5883L_DATARATE_30HZ);

 // Set number of samples averaged
 compass.setSamples(HMC5883L_SAMPLES_8);
}

void loop()
{
 Vector mag = compass.readRaw();

 // Determine Min / Max values
 if (mag.XAxis < minX) minX = mag.XAxis;
 if (mag.XAxis > maxX) maxX = mag.XAxis;
 if (mag.YAxis < minY) minY = mag.YAxis;
 if (mag.YAxis > maxY) maxY = mag.YAxis;

 // Calculate offsets
 offX = (maxX + minX)/2;
 offY = (maxY + minY)/2;

 Serial.print(mag.XAxis);
 Serial.print(":");
 Serial.print(mag.YAxis);
 Serial.print(":");
 Serial.print(minX);
 Serial.print(":");
 Serial.print(maxX);
 Serial.print(":");
 Serial.print(minY);
 Serial.print(":");
 Serial.print(maxY);
 Serial.print(":");
 Serial.print(offX);
 Serial.print(":");
 Serial.print(offY);
 Serial.print("\n");
}
