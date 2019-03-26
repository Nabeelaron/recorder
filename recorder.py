import sounddevice as sd 
from time import sleep
import numpy as np 
class Recorder ( object ):
	def __init__(self):
		self._duration = 0
		self.__data_type = 'float64'
		self.__device_input = 9
		self.__device_output = 3
		self.__samplerate = 44100
		self.__channels = 1

	def record(self, duration = 3 , data_type = 'float64', channels = 1) :
		self._duration = duration
		self.__data_type = data_type
		self.__channels = channels
		try : 
			recorded_data = sd.rec( int (self.__samplerate * self._duration),
									samplerate = self.__samplerate, dtype = data_type,
									channels = channels )
			sd.wait()
		except:
			return None

		# recorded_data = noise_reduction(recorded_data)
		# recorded_data = np.array(recorded_data)

		return recorded_data


	def play(self, data ):
		try:
			
			sd.play(data , self.__samplerate , device = self.__device_output)

			sleep( self._duration)

			sd.stop()
		except :
		 
			print(" some error occured in ",__file__," @ 24" )
			return False


	def list_devices(self):
		return sd.query_devices()

	def save_recorded_file(self, data = '' , file_name = 'file'):
		if len(data) <= 0:
			print('corrupted data')
			return False
		



		from scipy.io.wavfile import write as wave_write
		file_name = 'SoundFiles\\'+file_name+'.wav'

		try:
			wave_write(file_name, self.__samplerate, data)
			return True
		except:
			return False
	

	def __del__(self):
		pass
	
	

def load_file( name= '' ,for_ = 1):
	from scipy.io.wavfile import read as wave_read
	if name == '':
		print ("error name : null ")
		return False
				
	if for_ :
		name += '.wav'
		fs, data = wave_read('./'+name)
	else :
		fs, data = wave_read(name)

	return (fs, data)


def filter_(x):
		import scipy.signal as signal
		data = signal.savgol_filter(x, 151, 5, deriv=0, delta=1.0, axis=-1, mode='mirror', cval=0.0)
		# data = signal.savgol_filter(x, 101, 5)
		return data


def noise_reduction(data): 
	frames = 0
	index = 0
	new_data = list()

	for ii in data:
		if frames == 80:
			frames = 0

		if ( ii == 0 or (ii < 0.006 and ii > -0.006) ):
			frames += 1
		else :
			frames = 0
			new_data.append(data[index][0])
		index += 1
	# for i in data:
	# 	new_data.append(i[0])
	return  filter_(new_data)  



def test(data):
	import numpy as np 
	import feature_extraction
	import SVM

	data = np.ravel(data)

	features = feature_extraction.mfcc_convert(np,data)
	# print(features[:5])
	svc = SVM.control_information()
	print("Predicted as :",SVM.test(svc,features))



	

