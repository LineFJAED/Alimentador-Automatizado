import RPi.GPIO as GPIO
import time

servo_pin = 17 #CAMBIAR PINES!!

# Tweak these values to get full range of servo movement
deg_0_pulse = 0.5  #ms
deg_180_pulse = 2.5 #ms

f = 50.0 #50Hz = 20ms between pulses

# Do some calculations on the pulse width parameters
period = 1000 / f # 20ms
k = 100 / period  #duty 0..100 over 20ms
deg_0_duty = deg_0_pulse * k
pulse_range = deg_180_pulse - deg_0_pulse
duty_range = pulse_range * k

# Initialize the GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, f)
pwm.start(0)

def set_angle(angle):
	duty = deg_0_duty + (angle / 180.0) * duty_range
	pwm.ChangeDutyCycle(duty)

try:
	    #set_angle(28)
	    #time.sleep(1)
	    set_angle(38)
	    time.sleep(0.5)
	    set_angle(3)
	    time.sleep(1)


finally:
	print("Cleaning up")
	GPIO.cleanup()
