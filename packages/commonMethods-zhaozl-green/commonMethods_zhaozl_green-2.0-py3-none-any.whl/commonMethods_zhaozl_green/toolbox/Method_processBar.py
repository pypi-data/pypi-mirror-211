"""
Notes:
	包括以下几个不同样式的进度条：

	- Wave, 波浪形进度条

	- Rectangle, 方框形进度条

	- SelfDefine, 自定义符号样式的进度条

Example
----------
>>> from commonMethods_zhaozl_green.toolbox.Method_processBar import Wave, Rectangle, SelfDefine

"""
import time
import numpy as np


class Wave:
	"""
	Notes:
		用于表达迭代的执行进度

	Args:
		processBarLength: int,进度条的长度,默认100
		iterateQuant: int,总的迭代次数,默认200

	Examples:
		>>> wave = Wave(processBarLength=100, iterateQuant=200)
		>>> for i in range(200):
		>>> 	time.sleep(0.03)
		>>> 	wave.refresh()
	"""
	def __init__(self, processBarLength=100, iterateQuant=1000):
		self.originWaveSymbols = [chr(9600+i) for i in range(8, 0, -1)]
		self.waveList = [self.originWaveSymbols[0]]*(processBarLength+100) + self.originWaveSymbols
		self.barLength = processBarLength
		self.__waveToDraw = []
		self.__timeRecorder = []
		self.iterateQuant = iterateQuant
		self.iterationCounter = 0

	def refresh(self):
		"""执行一次迭代"""
		self.iterationCounter += 1
		if self.iterationCounter % int(self.iterateQuant // self.barLength) == 0:
			self.__waveToDraw = [self.waveList.pop(-1)] + self.__waveToDraw
			self.__timeRecorder.append(time.time())
			self.__timeRecorder = self.__timeRecorder[-20:None]
			_avgTime = 0.0 if len(self.__timeRecorder) == 1 else np.quantile(np.diff(self.__timeRecorder), 0.75)
			self.__print(delayTime=_avgTime)
		if len(self.__waveToDraw) == self.barLength:
			for _ in range(len(self.originWaveSymbols)):
				_avgTime = np.mean(np.diff(self.__timeRecorder)).ravel()[0]
				time.sleep(_avgTime)
				self.__waveToDraw = [self.waveList.pop(-1)] + self.__waveToDraw
				self.__print(delayTime=_avgTime)

	def __print(self, **kwargs):
		__percentage = len(self.__waveToDraw[0:100]) / self.barLength * 100
		if "delayTime" in kwargs.keys():
			_msg = \
				"|" + \
				"".join(self.__waveToDraw[0:100]) + " " * (self.barLength - len(self.__waveToDraw[0:100])) + \
				"|" + \
				"%3d%%" % __percentage + " " * 3 + \
				"Each: %3.3fs" % kwargs['delayTime']

		else:
			_msg = \
				"|" + \
				"".join(self.__waveToDraw[0:100]) + " " * (self.barLength - len(self.__waveToDraw[0:100])) + \
				f"" + \
				"|" + \
				"%3d%%" % __percentage + " " * 3 + \
				"Each: %3.3fs" % kwargs['delayTime']
		print(_msg, end="\r", flush=False)


class Rectangle:
	"""
	Notes:
		用于表达迭代的执行进度

	Args:
		processBarLength: int,进度条的长度,默认100
		iterateQuant: int,总的迭代次数,默认200

	Examples:
		>>> rec = Rectangle(100, 200)
		>>> for i in range(200):
		>>> 	rec.refresh()
		>>> 	time.sleep(0.01)
	"""
	def __init__(self, processBarLength=100, iterateQuant=200):
		self.placeHolder = chr(9633)
		self.finishedStat = chr(9632)
		self.recList = [self.placeHolder] * (processBarLength)
		self.__counter = 0
		self.__iterateQuant = iterateQuant
		self.__processBarLength = processBarLength
		self.__processTimeList = []

	def __finishOnce(self):
		self.__processTimeList.append(time.time())
		self.recList[int(self.__counter * self.__processBarLength / self.__iterateQuant)] = self.finishedStat
		self.__counter += 1

	def __print(self):
		self.__toPrint = "".join(self.recList)
		_percentage = int(self.__counter * self.__processBarLength / self.__iterateQuant)
		_processTime = 0.0 if len(self.__processTimeList) <= 2 else np.quantile(np.diff(self.__processTimeList), 0.75)
		self.__processTimeList = self.__processTimeList[-20: None]
		print(f"|{self.__toPrint}|{'%3d' % _percentage}%    Each: {'%2.3f' % _processTime}s", end="\r", flush=False)

	def refresh(self):
		"""执行一次迭代"""
		self.__finishOnce()
		self.__print()


class SelfDefine(Rectangle):
	"""
	Notes:
		用于自定义符号样式以表达迭代的执行进度

	Args:
		processBarLength: int,进度条的长度,默认100
		iterateQuant: int,总的迭代次数,默认200
		placeholder: str,代表未执行完成的进度符号,默认"-"
		finishedStat: str,代表执行完成的进度符号,默认"#"

	Examples:
		>>> rec = SelfDefine(processBarLength=100, iterateQuant=200, placeholder="-", finishedStat="O")
		>>> for i in range(200):
		>>> 	rec.refresh()
		>>> 	time.sleep(0.01)
	"""
	def __init__(self, processBarLength=100, iterateQuant=200, placeholder="-", finishedStat="#"):
		super().__init__(processBarLength=processBarLength, iterateQuant=iterateQuant)
		self.placeHolder = placeholder
		self.finishedStat = finishedStat
		self.recList = [self.placeHolder] * (processBarLength)

