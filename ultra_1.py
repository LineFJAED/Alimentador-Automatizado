#Libraries
import RPi.GPIO as GPIO
import time
import smtplib

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins CAMBIAR PINES!
GPIO_TRIGGER = 18
GPIO_ECHO = 24

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

#Email Configuration
smtpUser= 'alimentadorautomatico2018@gmail.com'
smtpPass= 'VigiliA27'

toAdd= 'jedgardo.trigueros@gmail.com'
fromAdd= smtpUser

subject= 'AVISO IMPORTANTE'
header= 'To: ' + toAdd + '\n' + 'From: ' + fromAdd + '\n' + 'Subject: ' + subject
body= 'EL ALIMENTADOR DE TU MASCOTA SE HA QUEDADO SIN COMIDA. Por favor, deposita comida en el de nuevo, para mantener a tu mascota saludable.'

x=0
y=0

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while (x<=2):
            dist = distance()
            #print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
            if(dist <= 5.0):
                
                print("Lleno") #Cambiar por el código que mande el correo
                x+=1
            else:
                
                if(y==0):
                    #Notification email send
                    print (header + '\n' + body)
                    s = smtplib.SMTP('smtp.gmail.com',587)

                    s.ehlo()
                    s.starttls()
                    s.ehlo()

                    s.login(smtpUser, smtpPass)
                    s.sendmail(fromAdd, toAdd, header + '\n\n' + body)

                    s.quit()
                    x=3
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
