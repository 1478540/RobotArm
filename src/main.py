
import GPIOpre
#import SG90
#import ARM
import MatrixKeyBoard
import ArmOperator
import time




if __name__ == '__main__':

	try:
		GPIOpre.init()
		ArmOperator.init()


		while True:
			if MatrixKeyBoard.check_button(MatrixKeyBoard.R1_PIN,MatrixKeyBoard.C1_PIN):
				ArmOperator.VoiceOperation()
				time.sleep(0.2)
			elif MatrixKeyBoard.check_button(MatrixKeyBoard.R2_PIN,MatrixKeyBoard.C1_PIN):
				ArmOperator.operator_mode=((ArmOperator.operator_mode+1)%4)
				time.sleep(0.2)
			elif MatrixKeyBoard.check_button(MatrixKeyBoard.R3_PIN,MatrixKeyBoard.C1_PIN):
				ArmOperator.AddAngleOperation(10)
				time.sleep(0.2)
			elif MatrixKeyBoard.check_button(MatrixKeyBoard.R4_PIN,MatrixKeyBoard.C1_PIN):
				ArmOperator.ReduceAngleOperation(10)
				time.sleep(0.2)
			else:
				time.sleep(0.1)

		
		
#		SG90.rapidly_servo_move(ARM.f2bServo,90)
#		SG90.smooth_servo_move(ARM.h2lServo,160,140)	
#		ARM.l2rServoMove(-1,10)

	except Exception as err:
		print(err)
	finally:
		ArmOperator.over()
		GPIOpre.over()

	

