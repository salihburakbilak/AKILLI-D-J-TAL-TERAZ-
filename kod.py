import RPi.GPIO as GPIO # GPIO KÜTÜPHANESİNİ TANIMLADIM
import time # TİME KÜTÜPHANESİNİ TANIMLADIM
import spidev # SPİDEV KÜTÜPHANESİNİ TANIMLADIM
import Adafruit_CharLCD as LCD # LCD KÜTÜPHANESİNİ TANIMLADIM

# Raspberry Pi İle LCD ekran arasındaki pin bağlantıları tanımlandı
lcd_rs = 26
lcd_en = 24
lcd_d4 = 22
lcd_d5 = 18
lcd_d6 = 16
lcd_d7 = 12
lcd_backlight = 2

# Program İçerisinde kullanılacak olan değişkenleri tanımladım 
lcd_columns = 16
lcd_rows = 2
delay = 0.5
ldr_channel = 0
NUM_CYCLES = 10
spi = spidev.SpiDev()
spi.open(0, 0)
kg=0
# Lcd pin bağlantılarını fonksiyon içerisinde tanımladım
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# Terazinin İlk açılışında Hoşgeldiniz Yazsını Lcd ye yazdırma
lcd.message('HOÅGELDÄ°NÄ°Z')

# GY-31 sensörün 
def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(37,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(33,GPIO.OUT)
  GPIO.setup(35,GPIO.OUT)
  print("\n")
  
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  
  #    0      0    
  #   78      4    
  #  155      7.5    
  #  233      8.4    
  #  310      12.5    
  #  465      17    
  #  775      25    
  # 1023      50    
 
  temp = ((data * 330)/float(1023))
  temp = round(temp,places)
  return temp

def loop():
  tamp = 1
  while(1):  

    GPIO.output(33,GPIO.LOW)
    GPIO.output(35,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(37, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    
    GPIO.output(33,GPIO.LOW)
    GPIO.output(35,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(37, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    
    GPIO.output(33,GPIO.HIGH)
    GPIO.output(35,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(37, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    time.sleep(2)  

lcd.clear()


    if green<11000 and blue<15000 and red>19000:
      meyve=domates
      kg=2
      lcd.message('domates')
      tamp=1
    elif red<14000 and  blue<16000 and green>15000:
      meyve=marul
      kg=3
      lcd.message('marul')
      tamp=1
    elif green<10000 and red<11000 and blue>12000:
      meyve=patlÄ±can
      kg=4
      lcd.message('patlÄ±can')
      tamp=1
    elif red>10000 and green>10000 and blue>10000 and temp==1:
      meyve=yok
      lcd.message('meyve veya sebze yok')
      tamp=0

temp_level = ReadChannel(1)
temp       = ConvertTemp(temp_level,2)

fiyat= temp*kg

lcd.message('aldÄ±ÄŸÄ±nÄ±z Ã¼rÃ¼n tutarÄ±=' fiyat ' kadar ')

def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        endprogram()

