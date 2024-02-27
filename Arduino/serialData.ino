void setup() {
  // Inicia la comunicación serie a 9600 baudios.
  Serial.begin(9600);
  
  // Configura el pin 4 como salida.
  pinMode(4, OUTPUT);
}

void loop() {
  // Verifica si hay datos disponibles para leer en el puerto serie.
  if (Serial.available() > 0) {
    // Lee el próximo carácter del puerto serie.
    char receivedChar = Serial.read();
    
    // Verifica si el carácter recibido es '1'.
    if (receivedChar == '1') {
      // Enciende el LED.
      digitalWrite(4, HIGH);
      
      // Espera un segundo (1000 milisegundos).
      delay(1000);
      
      // Apaga el LED.
      digitalWrite(4, LOW);
    }
  }
}
