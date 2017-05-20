import tkinter as tk
from PIL import Image, ImageTk
import time
from utils.definitions import Form


class Application(tk.Frame):
	def __init__(self, master=tk.Tk()):
		super().__init__(master, width = 992, height = 502, bg='white')
		self.width = 992
		self.height = 502
		self.lock = 1
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
		if self.lock == 1:
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
			self._save_button = tk.Button(self._form_move_frame,text = "Save", command = self.save)
			self._save_button.place(x = self.width//99.2*13, y = self.height//50.2*30)
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
			self.lock = 1

	def setMoves(self,evt):
		self.selected_form = self._form_listbox.get(tk.ACTIVE)
		if self.selected_form != self.last_selected_form:
			self._move_listbox.delete(0,tk.END)
			for moves in Form.forms[self.selected_form].values():
				self._move_listbox.insert(tk.END,moves)
			self._move_listbox.place(x = self.width//99.2, y = self.height//50.2*20)
			self.last_selected_form = self.selected_form

	def loadMenu(self):
		self._menubar.add_command(label='Training Mode', command=self.trainingMode)
		self._menubar.add_command(label='Test Mode', command=self.testMode)
		self._menubar.add_command(label='Exit', command=self.root.quit)
		self.root.config(menu=self._menubar)

	def save(self):
		self.selected_form = self._form_listbox.get(tk.ACTIVE)
		self.selected_move = self._move_listbox.get(tk.ACTIVE)
		print(self.selected_form)
		print(self.selected_move)

	# LoadVideoHolder receives a numpy array as a parameter
	def loadVideoHolder(self, img):
		img = Image.fromarray(img, 'RGB')
		self.photo = ImageTk.PhotoImage(img)
		self._video_holder.imgtk = self.photo
		self._video_holder.config(image = self.photo)
		self._video_holder.pack()
		#if self.selected_form != "":
		#	self.setMoves()

	def loadVideoHolderTestWindow(self):
		self._video_holder.imgtk = self.photo
		self._video_holder.config(image = self.photo)
		self._video_holder.pack()

	def hello(self):
		print('hello')