#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define DATA_SIZE 250  // Количество бит в данных
#define POLYNOMIAL "11101111"


void generateRandomData(char *data, int dataSize) {
    srand(time(NULL));

    for (int i = 0; i < dataSize; i++) {
        data[i] = rand() % 2 + '0';
    }
    data[dataSize] = '\0';
}

void calculateCRC(const char *data, const char *polynomial, char *result) {
   int dataLength = strlen(data);
   int polynomialLength = strlen(polynomial);
   
   char extendedData[dataLength + polynomialLength];
   strcpy(extendedData, data);
   for (int i = 0; i < polynomialLength - 1; i++) {
       strcat(extendedData, "0");
   }

   for (int i = 0; i < dataLength; i++) {
       if (extendedData[i] == '1') {
           for (int j = 0; j < polynomialLength; j++) {
               extendedData[i + j] ^= polynomial[j] - '0';
           }
       }
   }

   strncpy(result, extendedData + dataLength, polynomialLength);
   result[polynomialLength] = '\0';
}

void calculateExtendedCRC(const char *data, const char *polynomial, char *result) {
   char crcResult[DATA_SIZE + 1];
   calculateCRC(data, polynomial, crcResult);

   int dataLength = strlen(data);
   int crcResultLength = strlen(crcResult);
   
   char extendedData[crcResultLength + dataLength];
   strcpy(extendedData, crcResult);
   strcat(extendedData, data);

   for (int i = 0; i < crcResultLength; i++) {
       if (extendedData[i] == '1') {
           for (int j = 0; j < crcResultLength; j++) {
               extendedData[i + j] ^= polynomial[j] - '0';
           }
       }
   }
   strncpy(result, extendedData + crcResultLength, crcResultLength);
   result[crcResultLength] = '\0';
}


int main() {
 char data[DATA_SIZE + 1];
 char crcResult[DATA_SIZE + 1];
 char extendedCRCResult[DATA_SIZE + 1];

 generateRandomData(data, DATA_SIZE);

 printf("Сгенерированные данные: %s\n", data);

 // Определение полинома
 char polynomial[9];
 for (int i = 0; i < 8; i++) {
    polynomial[i] = rand() % 2 + '0';
 }
 polynomial[8] = '\0';

 for (int polynomialLength = 2; polynomialLength <= 8; polynomialLength++) {
    // Создание полинома нужной длины
    char poly[polynomialLength + 1];
    strncpy(poly, polynomial, polynomialLength);
    poly[polynomialLength] = '\0';

    printf("Полином длины %d: %s\n", polynomialLength, poly);

    calculateCRC(data, poly, crcResult);
    printf("Вычисленное значение CRC: %s\n", crcResult);

    int detectedErrors = 0;
    int undetectedErrors = 0;
    for (int i = 0; i < 10; i++) {
        for (int bitToFlip = 0; bitToFlip < DATA_SIZE + strlen(crcResult); bitToFlip++) {
            char corruptedData[DATA_SIZE + 1];
            strcpy(corruptedData, data);
            
            if (bitToFlip < DATA_SIZE) {
              // Искажаем бит в данных
              corruptedData[bitToFlip] = (corruptedData[bitToFlip] == '0') ? '1' : '0';
            } else {
              
            }
            
            calculateExtendedCRC(corruptedData, poly, extendedCRCResult);
            
            int errors = 0;
            for (int i = 0; i < strlen(extendedCRCResult); i++) {
              if (extendedCRCResult[i] != '0') {
                errors = 1;
                break;
              }
            }
            
            if (errors) {
              detectedErrors++;
            } else {
              undetectedErrors++;
            }
        }

   //     printf("НЕ обнаружено ошибок для полинома длины %d: %d\n", polynomialLength, undetectedErrors);
        
    }
    printf("НЕ обнаружено ошибок для полинома длины %d: %d\n", polynomialLength, undetectedErrors/10);
    
    // Расчет вероятности ненахождения ошибки
     // Расчет вероятности ненахождения ошибки
     double undetectedErrorProbability = (double)undetectedErrors / (1 << polynomialLength);
     if (undetectedErrorProbability > 1.0) {
        undetectedErrorProbability = 1.0;
     }
     printf("Вероятность ненахождения ошибки для полинома длины %d: %f\n", polynomialLength, undetectedErrorProbability);

 }

 return 0;
}
