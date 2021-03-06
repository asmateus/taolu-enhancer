import tkinter as tk
from PIL import Image, ImageTk
import time
from utils.definitions import Form,Joints
from pyserial.connector import Reader
import cv2

class Application(tk.Frame):
	def __init__(self, proc, master=tk.Tk()):
		super().__init__(master, width = 992, height = 502, bg='white')
		self.proc = proc
		self.width = 992
		self.height = 502
		self.lock = 0
		self.operation_pending = False
		self.selected_form = tk.StringVar()
		self.last_selected_form = "None"
		self.selected_move = tk.StringVar()
		self.identified_move = "Unknown"
		self.root = master
		self.photo = 1;
		self.root.title('Taolu  Enhancer - no active session')
		self.pack()
		x = self.winfo_screenwidth() // 2 - self.width // 2
		y = self.winfo_screenheight() // 2 - self.height // 2
		self.geometry =('{}x{}+{}+{}'.format(self.width,self.height,x,y))

	
		self._menubar = tk.Menu(master)
		self.loadMenu()
		self.trainingMode()

		# image show
		self._image_frame = tk.Frame(master = self, width=self.width//1.545, height=self.height//1.048,bg='white')
		self._image_frame.place(x = self.width//2.916, y = self.height//50.2)
		self._video_holder = tk.Label(self._image_frame)


	def trainingMode(self):
		if self.lock == 1 or self.lock == 0:
			# left panel
			self._form_move_frame = tk.Frame(master = self, width=self.width//3.08, height=self.height//1.048, bg='#F0F0F0', colormap="new")
			self._form_move_frame.place(x = self.width//99.2, y = self.height//50.2)

			# Set form
			self._form_label = tk.Label(self._form_move_frame, text = "Select form: ",bg='#E0E0E0')
			self._form_label.place(x = self.width//99.2, y = self.height//50.2)
			
			self._form_listbox = tk.Listbox(self._form_move_frame, width = int((self.width//99.2)*5), height = int(self.height//502*3))
			for key in Form.forms:
				self._form_listbox.insert(tk.END,key)
			self._form_listbox.place(x = self.width//99.2, y = self.height//50.2*4)
			self._form_listbox.bind('<<ListboxSelect>>', self.setMoves)

			self._form_scrollbar = tk.Scrollbar(self._form_move_frame)
			self._form_scrollbar.place(x = int(self.width//3.08-(self.width//99.2)*5), y = int(self.height//50.2*4))
			self._form_scrollbar.config(command=self._form_listbox.yview)
			
			# Set moves
			self._moves_label = tk.Label(self._form_move_frame, text = "Select Move: ",bg='#E0E0E0')
			self._moves_label.place(x = self.width//99.2, y = self.height//50.2*17)

			self._move_listbox = tk.Listbox(self._form_move_frame, selectmode=tk.EXTENDED, width = int((self.width//99.2)*5), height = int(self.height//502*3))
			self._move_listbox.place(x = self.width//99.2, y = self.height//50.2*20)
			#self._move_listbox.bind('<<ListboxSelect>>', self.hello)

			self._move_scrollbar = tk.Scrollbar(self._form_move_frame)
			self._move_scrollbar.place(x = int(self.width//3.08-(self.width//99.2)*5), y = int(self.height//50.2*20))
			self._move_scrollbar.config(command=self._move_listbox.yview)

			#Save button
			self._save_button = tk.Button(self._form_move_frame,text = "Start", command = self.startToSaveData)
			self._save_button.place(x = self.width//99.2*13, y = self.height//50.2*30)
			if self.lock == 1:
				self._form_identified_label.destroy()
				self._form_identified_label_show.destroy()
				self._identify_move_button.destroy()
			self.lock = 2


	def testMode(self):
		if self.lock == 2:
			self._move_listbox.destroy()
			self._form_listbox.destroy()
			self._form_scrollbar.destroy()
			self._move_scrollbar.destroy()
			self._moves_label.destroy()
			self._form_label.destroy()
			self._save_button.destroy()
			self._form_identified_label = tk.Label(self._form_move_frame, text = "The move is: ",bg='#E0E0E0')
			self._form_identified_label.place(x = self.width//99.2, y = self.height//50.2)
			self._form_identified_label_show = tk.Label(self._form_move_frame, text = self.identified_move,bg='#E0E0E0')
			self._form_identified_label_show.place(x = self.width//99.2, y = self.height//50.2*4)
			self._identify_move_button = tk.Button(self._form_move_frame,text = "Identify Move", command = self.identifyMove)
			self._identify_move_button.place(x = self.width//99.2*13, y = self.height//50.2*8)
			self.lock = 1



	def setMoves(self,evt):
		self.selected_form = self._form_listbox.get(tk.ACTIVE)
		if self.selected_form != self.last_selected_form:
			self._move_listbox.delete(0,tk.END)
			for m in Form.forms[self.selected_form].keys():
				self._move_listbox.insert(tk.END,Form.forms[self.selected_form][m])
			self._move_listbox.place(x = self.width//99.2, y = self.height//50.2*20)
			self.last_selected_form = self.selected_form

	def loadMenu(self):
		self._menubar.add_command(label='Training Mode', command=self.trainingMode)
		self._menubar.add_command(label='Test Mode', command=self.testMode)
		self._menubar.add_command(label='Exit', command=self.root.quit)
		self.root.config(menu=self._menubar)

	def startToSaveData(self):
		self.selected_move = self._move_listbox.get(tk.ACTIVE)
		val = ''
		for name, value in Form.forms[self.selected_form].items():
			if value == self.selected_move:
				val = name

		print(Form.abbreviations[self.selected_form][val])
		self.c2p = Reader(1,self.proc, Form.abbreviations[self.selected_form][val]) # (pipe, conn_type)
		self.c2p.startReading(10)

	def identifyMove(self):
		self.c2p = Reader(2,self.proc) # (conn_type, proc)
		self.c2p.startReading(10)

		self.operation_pending = True

	def checkPendingOperations(self):
		if self.operation_pending:
			if self.c2p.move:
				val = ''
				for name, value in Form.abbreviations.items():
					for n,v in value.items():
						if v == self.c2p.move or v == [self.c2p.move]:
							val = Form.forms[name][n]
							break
				print(self.c2p.move)
				self._form_identified_label_show.config(text=val)
				self.operation_pending = False

	def drawJoints(self, img, joints, r, color = (255,100,185)):
		if joints != []:
			for pos in joints:
				img = cv2.circle(img, pos, r, color, thickness=1, lineType=8, shift=0)
			#img = cv2.circle(img, joints[18], r, (0,0,0), thickness=2, lineType=8, shift=0)

		return img

	def drawBones(self, img, joints, t, colorl = (0,0,255), colorc = (255,0,0), colorr = (0,255,0)):
		if joints != []:
			#head-neck
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_HEAD], joints[Joints.NUI_SKELETON_POSITION_SHOULDER_CENTER], colorc,t)
			#neck-spine
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SHOULDER_CENTER], joints[Joints.NUI_SKELETON_POSITION_SPINE], colorc,t)
			#spine-hipcenter
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SPINE], joints[Joints.NUI_SKELETON_POSITION_HIP_CENTER], colorc,t)

			#-----left arm-----#
			#neck-shoulderleft
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SHOULDER_CENTER], joints[Joints.NUI_SKELETON_POSITION_SHOULDER_LEFT], colorl,t)
			#shoulderleft-elbowright
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SHOULDER_LEFT], joints[Joints.NUI_SKELETON_POSITION_ELBOW_LEFT], colorl,t)
			#elbowleft-wristrigth
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_ELBOW_LEFT], joints[Joints.NUI_SKELETON_POSITION_WRIST_LEFT], colorl,t)
			#wristleft-handright
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_WRIST_LEFT], joints[Joints.NUI_SKELETON_POSITION_HAND_LEFT], colorl,t)

			#-----right arm-----#
			#neck-shoulderright
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SHOULDER_CENTER], joints[Joints.NUI_SKELETON_POSITION_SHOULDER_RIGHT], colorr,t)
			#shoulderright-elbowright
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_SHOULDER_RIGHT], joints[Joints.NUI_SKELETON_POSITION_ELBOW_RIGHT], colorr,t)
			#elbowright-wristrigth
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_ELBOW_RIGHT], joints[Joints.NUI_SKELETON_POSITION_WRIST_RIGHT], colorr,t)
			#wristright-handright
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_WRIST_RIGHT], joints[Joints.NUI_SKELETON_POSITION_HAND_RIGHT], colorr,t)

			#-----LEFT leg-----#
			#hipcenter-hipLEFT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_HIP_CENTER], joints[Joints.NUI_SKELETON_POSITION_HIP_LEFT], colorl,t)
			#hipLEFT-kneeLEFT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_HIP_LEFT], joints[Joints.NUI_SKELETON_POSITION_KNEE_LEFT], colorl,t)
			#kneeLEFT-ankleLEFT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_KNEE_LEFT], joints[Joints.NUI_SKELETON_POSITION_ANKLE_LEFT], colorl,t)
			#ankleLEFT-footLEFT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_ANKLE_LEFT], joints[Joints.NUI_SKELETON_POSITION_FOOT_LEFT], colorl,t)

			#-----RIGHT leg-----#
			#hipcenter-hipRIGHT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_HIP_CENTER], joints[Joints.NUI_SKELETON_POSITION_HIP_RIGHT], colorr,t)
			#hipRIGHT-kneeRIGHT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_HIP_RIGHT], joints[Joints.NUI_SKELETON_POSITION_KNEE_RIGHT], colorr,t)
			#kneeRIGHT-ankleRIGHT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_KNEE_RIGHT], joints[Joints.NUI_SKELETON_POSITION_ANKLE_RIGHT], colorr,t)
			#ankleRIGHT-footRIGHT
			img = cv2.line(img, joints[Joints.NUI_SKELETON_POSITION_ANKLE_RIGHT], joints[Joints.NUI_SKELETON_POSITION_FOOT_RIGHT], colorr,t)
		return img
	# LoadVideoHolder receives a numpy array as a parameter
	def loadVideoHolder(self, img, joints):
		img = self.drawJoints(img, joints, 3)
		img = self.drawBones(img, joints, 2)
		img = Image.fromarray(img, 'RGB')
		self.photo = ImageTk.PhotoImage(img)
		self._video_holder.imgtk = self.photo
		self._video_holder.config(image = self.photo)
		self._video_holder.pack()

	def loadVideoHolderTestWindow(self):
		self._video_holder.imgtk = self.photo
		self._video_holder.config(image = self.photo)
		self._video_holder.pack()

	def hello(self):
		print('hello')