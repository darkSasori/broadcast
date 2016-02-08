#define RED 11
#define GREEN 10
#define BLUE 9

int vR = 0;
int vG = 0;
int vB = 0;
int pin;
char color[4];

void setup() {
  Serial.begin(9600);
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(RED,HIGH);
}

void loop() {
  delay(1);
}

void serialEvent() {
  int value = Serial.read();
  switch(value) {
    case 114:
      pin = RED;
      break;
    case 103:
      pin = GREEN;
      break;
    case 98:
      pin = BLUE;
      break;
    case 59:
      Serial.print("PIN: ");
      Serial.print(pin);
      Serial.print("\tVALUE: ");
      Serial.println(color);
      analogWrite(pin, atoi(color));
      color[0] = 0; color[1] = 0; color[2] = 0;
      break;
    default:
      for (int i = 0; i < 3; i++) {
        if( color[i] == 0 ){
          color[i] = value;
          break;
        }
      }
      break;
  }
}
