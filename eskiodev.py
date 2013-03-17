#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import gobject

import numpy
from numpy import *

N = 25
ITE = 250

class PyApp(gtk.Window):
	def __init__(self):
		super(PyApp, self).__init__()
		self.set_size_request(1300, 640)
		self.set_position(gtk.WIN_POS_CENTER)
		self.connect("destroy", gtk.main_quit)
		self.kalip = gtk.Fixed()
		
		"""
		------------------------------------------------------------------
		"""
		self.katsayigirisleri = [0 for x in range(0, 21)]
		self.katsayietiketleri = [0 for x in range(0, 21)]
		for i in range(1, 21):
			self.katsayigirisleri[i] = gtk.Entry()
			self.katsayigirisleri[i].set_width_chars(3)
			self.kalip.put(self.katsayigirisleri[i], 30*i, 0)
			self.katsayietiketleri[i] = gtk.Label("x" + str(20 - i))
			self.kalip.put(self.katsayietiketleri[i], 30*i, 25)
		self.katsayigirisleri[21 - 1].set_text("16")
		self.katsayigirisleri[21 - 2].set_text("-20")
		self.katsayigirisleri[21 - 3].set_text("0")
		self.katsayigirisleri[21 - 4].set_text("1")
		
		#self.yontemgirisi = gtk.ComboBox()
		self.yontemgirisi = gtk.combo_box_new_text()
		self.yontemgirisi.insert_text(0, "n-r")
		self.yontemgirisi.insert_text(1, "secant")
		self.yontemgirisi.insert_text(2, "regule false")
		self.yontemgirisi.insert_text(3, "düzeltilmiş n-r")
		self.kalip.put(self.yontemgirisi, 640, 0)
		self.yontemgirisi.connect("changed", self.ssyontemgirisi)
		self.kalip.put(gtk.Label("yöntem"), 640, 25)
		
		self.hatagirisi = gtk.SpinButton()
		self.hatagirisi.set_range(0, 1)
		self.hatagirisi.set_increments(0.001, 0.01)
		self.hatagirisi.set_digits(3)
		self.kalip.put(self.hatagirisi, 760, 0)
		self.hatagirisi.set_value(0.001)
		self.kalip.put(gtk.Label("tolerans"), 760, 25)
		
		self.baslangicgirisleri = [0 for x in range(0, 3)]
		for i in range(1, 3):
			self.baslangicgirisleri[i] = gtk.Entry()
			self.baslangicgirisleri[i].set_width_chars(3)
			self.baslangicgirisleri[i].set_sensitive(False)
			self.kalip.put(self.baslangicgirisleri[i], (800 + 30*i), 0)
			self.kalip.put(gtk.Label("bşl" + str(i)), (800 + 30*i), 25)
		self.baslangicgirisleri[1].set_text("3")
		self.baslangicgirisleri[2].set_text("5")
		
		self.buyukkirmizidugme = gtk.Button("hesapla")
		self.buyukkirmizidugme.set_sensitive(False)
		self.kalip.put(self.buyukkirmizidugme, 900, 0)
		self.buyukkirmizidugme.connect("clicked", self.ssbuyukkirmizidugme)
		
		self.sonucetiketi = gtk.Entry()
		self.sonucetiketi.set_width_chars(16)
		self.sonucetiketi.set_editable(False)
		self.kalip.put(self.sonucetiketi, 1000, 0)
		self.kalip.put(gtk.Label("SONUÇ"), 1000, 25)
		
		self.ayrac = gtk.HSeparator()
		self.ayrac.set_size_request(1366, 2)
		self.kalip.put(self.ayrac, 0, 40)
		"""
		------------------------------------------------------------------
		"""
		
		self.islemgirisi = gtk.combo_box_new_text()
		self.islemgirisi.insert_text(0, "traspoz")
		self.islemgirisi.insert_text(1, "invers")
		self.islemgirisi.insert_text(2, "toplama")
		self.islemgirisi.insert_text(3, "çarpma")
		self.islemgirisi.insert_text(4, "determinant")
		self.kalip.put(self.islemgirisi, 0, 0 + (44))
		self.kalip.put(gtk.Label("yöntem"), 0, 25 + (44))
		self.islemgirisi.connect("changed", self.ssislemgirisi)
		
		self.boyutgirisleri = [0 for x in range(0, 5)]
		for i in range(1, 5):
			self.boyutgirisleri[i] = gtk.SpinButton()
			self.boyutgirisleri[i].set_range(2, N)
			self.boyutgirisleri[i].set_increments(1, 5)
			self.boyutgirisleri[i].set_digits(0)
			self.boyutgirisleri[i].set_sensitive(False)
			self.boyutgirisleri[i].connect("value-changed", self.ssboyutgirisleri)
			self.kalip.put(self.boyutgirisleri[i], ((i * 55) + 50), 0 + (44))
		self.kalip.put(gtk.Label("m1"), ((1 * 55) + 50), 25 + (44))
		self.kalip.put(gtk.Label("n1"), ((2 * 55) + 50), 25 + (44))
		self.kalip.put(gtk.Label("m2"), ((3 * 55) + 50), 25 + (44))
		self.kalip.put(gtk.Label("m2"), ((4 * 55) + 50), 25 + (44))
		
		self.almadugmesi = gtk.Button("gir")
		self.kalip.put(self.almadugmesi, 325, 0 + (44))
		self.almadugmesi.set_sensitive(False)
		self.almadugmesi.connect("clicked", self.ssalmadugmesi)
		
		self.hesaplamadugmesi = gtk.Button("hesapla")
		self.kalip.put(self.hesaplamadugmesi, 400, 0 + (44))
		self.hesaplamadugmesi.set_sensitive(False)
		self.hesaplamadugmesi.connect("clicked", self.sshesaplamadugmesi)
											
		self.add(self.kalip)
		self.show_all()
		
	
	def ssislemgirisi(self, widget):
		i = widget.get_active()
		if i == 0 or i == 1 or i == 4:
			self.boyutgirisleri[1].set_sensitive(True)
			self.boyutgirisleri[2].set_sensitive(True)
		elif i == 2 or i == 3:
			self.boyutgirisleri[1].set_sensitive(True)
			self.boyutgirisleri[2].set_sensitive(True)
			self.boyutgirisleri[3].set_sensitive(True)
			self.boyutgirisleri[4].set_sensitive(True)
		self.almadugmesi.set_sensitive(True)
		
	
	def ssboyutgirisleri(self, widget):
		a = self.islemgirisi.get_active()
		"""
		print widget
		"""
	
	def ssalmadugmesi(self, widget):
		self.hesaplamadugmesi.set_sensitive(True)
		m1 = int(self.boyutgirisleri[1].get_value())
		n1 = int(self.boyutgirisleri[2].get_value())
		self.entryler1 = [0 for x in range(m1 * n1)]
		for m in range(m1):
			for n in range(n1):
				i = (m * n1) + n
				self.entryler1[i] = gtk.Entry()
				self.entryler1[i].set_width_chars(1)
				self.kalip.put(self.entryler1[i], (0 + (m * 15)), (50 + (n * 20) + (44)))
		if self.boyutgirisleri[3].get_sensitive() == True:
			m2 = int(self.boyutgirisleri[3].get_value())
			n2 = int(self.boyutgirisleri[4].get_value())
			self.entryler2 = [0 for x in range(m2 * n2)]
			for m in range(m2):
				for n in range(n2):
					i = (m * n2) + n
					self.entryler2[i] = gtk.Entry()
					self.entryler2[i].set_width_chars(1)
					self.kalip.put(self.entryler2[i], (((N + 1) * 15) + (m * 15)), (50 + (n * 20) + (44)))
		self.show_all()
			
	
	def sshesaplamadugmesi(self, widget):
		if self.hesaplamadugmesi.get_sensitive() == True:
			m1 = int(self.boyutgirisleri[1].get_value())
			n1 = int(self.boyutgirisleri[2].get_value())
			self.x1 = [[0 for n in range(n1)] for m in range(m1)]
			for i in range(m1 * n1):
				n = (i % n1)
				m = ((i - n) / n1)
				a = self.entryler1[i].get_text()
				if a == "":
					self.x1[m][n] = 0
				elif self.isnumeric(a) == True:
					self.x1[m][n] = float(a)
			if self.islemgirisi.get_active() == 2 or self.islemgirisi.get_active() == 3:
				m2 = int(self.boyutgirisleri[3].get_value())
				n2 = int(self.boyutgirisleri[4].get_value())
				self.x2 = [[0 for n in range(n2)] for m in range(m2)]
				for i in range(m2* n2):
					n = (i % n2)
					m = ((i - n) / n2)
					a = self.entryler2[i].get_text()
					if a == "":
						self.x2[m][n] = 0
					elif self.isnumeric(a) == True:
						self.x2[m][n] = float(a)
			islem = self.islemgirisi.get_active()
			flag = False
			if islem == 0:
				"""transpoz"""
				m3 = n1
				n3 = m1
				flag = True
				self.x3 = [[0 for n in range(n3)] for m in range(m3)]
				self.transpoz()
			elif islem == 1 and m1 == n1:
				"""invers"""
				m3 = n1
				n3 = m1
				flag = True
				self.x3 = [[0 for n in range(n3)] for m in range(m3)]
				self.invers()
			elif islem == 2 and m1 == m2 and n1 == n2:
				"""topla"""
				m3 = m1
				n3 = n1
				flag = True
				self.x3 = [[0 for n in range(n3)] for m in range(m3)]
			elif islem == 3 and n1 == m2:
				"""carp"""
				m3 = m1
				n3 = n2
				flag = True
				self.x3 = [[0 for n in range(n3)] for m in range(m3)]
				self.carp()
			elif islem == 4 and m1 == n1:
				"""determinant"""
				flag = True
				d = numpy.linalg.det(self.x1)
				determinantuyarisi = gtk.MessageDialog(self, 
				    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
				    gtk.BUTTONS_CLOSE, ("deterimant: " + str(d)))
				determinantuyarisi.run()
				determinantuyarisi.destroy()
			else:
				flag = False
				uyari = gtk.MessageDialog(self, 
				    gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
				    gtk.BUTTONS_CLOSE, "boyutları lütfen işlem türüne uygun seçin")
				uyari.run()
				uyari.destroy()
			if flag == True and islem != 4:
				self.entryler3 = [0 for x in range(m3 * n3)]
				for m in range(m3):
					for n in range(n3):
						i = (m * n3) + n
						self.entryler3[i] = gtk.Entry()
						self.entryler3[i].set_width_chars(2)
						self.entryler3[i].set_text(str(self.x3[m][n]))
						self.kalip.put(self.entryler3[i], ((((2 * N) + 1) * 15) + (m * 22)), (50 + (n * 20) + (44)))
		self.hesaplamadugmesi.set_sensitive(False)
		self.boyutgirisleri[3].set_sensitive(False)
		self.boyutgirisleri[4].set_sensitive(False)
		self.almadugmesi.set_sensitive(False)
		self.islemgirisi.set_active(-1)
		self.show_all()


	def transpoz(self):
		self.x3 = array(matrix(self.x1).T)
		
	def invers(self):
		self.x3 = array(matrix(self.x1).I)
		
	def topla(self):
		self.x3 = array(matrix(self.x1) + matrix(self.x2))
		
	def carp(self):
		self.x3 = array(matrix(self.x1) * matrix(self.x2))
			
	def isnumeric(self, value):
		return str(value).replace(".", "").replace("-", "").isdigit()

	"""
	------------------------------------------------------------
	"""
	def ssyontemgirisi(self, widget):
		i = widget.get_active()
		self.baslangicgirisleri[1].set_sensitive(False)
		self.baslangicgirisleri[2].set_sensitive(False)
		if i == 0:
			self.baslangicgirisleri[1].set_sensitive(True)
			self.buyukkirmizidugme.set_sensitive(True)
			self.yontem = 0
		elif i == 1:
			self.baslangicgirisleri[1].set_sensitive(True)
			self.baslangicgirisleri[2].set_sensitive(True)
			self.buyukkirmizidugme.set_sensitive(True)
			self.yontem = 1
		elif i == 2:
			self.baslangicgirisleri[1].set_sensitive(True)
			self.baslangicgirisleri[2].set_sensitive(True)
			self.buyukkirmizidugme.set_sensitive(True)
			self.yontem = 2
		elif i == 3:
			self.baslangicgirisleri[1].set_sensitive(True)
			self.buyukkirmizidugme.set_sensitive(True)
			self.yontem = 3
		else:
			pass
	
	def ssbuyukkirmizidugme(self, widget):
		self.hata = float(self.hatagirisi.get_value())
		self.katsayilar = []
		for i in range(1, 21):
			yazi = self.katsayigirisleri[21 - i].get_text()
			if yazi == "":
				break
			elif yazi != "" and self.isnumeric(yazi) == True:
				self.katsayilar.append(float(yazi))
		self.baslangiclar = [0, 1, -1]
		for i in range(1, 3):
			yazi = self.baslangicgirisleri[i].get_text()
			if self.baslangicgirisleri[i].get_sensitive() == True and self.isnumeric(yazi):
				self.baslangiclar[i] = float(yazi)
		if self.yontem > -1:
			if self.yontem == 0:
				x = [self.baslangiclar[1]]
				for i in range (0, ITE):
					x.append(x[i] - (self.f(self.katsayilar, x[i]) / self.ft(self.katsayilar, 1, x[i])))
					if abs(x[i] - x[i - 1]) <= self.hata:
						break
			elif self.yontem == 1:
				x = [self.baslangiclar[1], self.baslangiclar[2]]
				for i in range (1, ITE):
					x.append(x[i] - ((x[i] - x[i-1]) / (self.f(self.katsayilar, x[i]) - self.f(self.katsayilar, x[i-1])) * self.f(self.katsayilar, x[i])))
					if abs(x[i] - x[i - 1]) <= self.hata:
						break
			elif self.yontem == 2:
				x = [self.baslangiclar[1], self.baslangiclar[2]]
				for i in range (1, ITE):
					x.append(x[i] - ((x[i] - x[0]) / (self.f(self.katsayilar, x[i]) - self.f(self.katsayilar, x[0])) * self.f(self.katsayilar, x[i])))
					if abs(x[i] - x[i - 1]) <= self.hata:
						break
			elif self.yontem == 3:
				x = [self.baslangiclar[1]]
				for i in range (0, ITE):
					x.append(x[i] - (self.f(self.katsayilar, x[i]) * self.ft(self.katsayilar, 1, x[i]) / (self.ft(self.katsayilar, 1, x[i])**2 - (self.f(self.katsayilar, x[i]) * self.ft(self.katsayilar, 2, x[i])))))
					if abs(x[i] - x[i - 1]) <= self.hata:
						break
			self.sonucetiketi.set_text(str(x[i]))
		# reset kısmı
		self.buyukkirmizidugme.set_sensitive(False)
		self.baslangicgirisleri[1].set_sensitive(False)
		self.baslangicgirisleri[2].set_sensitive(False)
		self.yontem = -1

	def isnumeric(self, value):
		return str(value).replace(".", "").replace("-", "").isdigit()

	
	def f(self, klar, x):
		sonuc = 0
		d = len(klar) - 1	
		for i in range (0, d+1):
			sonuc += klar[i] * math.pow(x, i)
		return sonuc

	def ft(self, klar, n, x):
		sonuc = 0
		d = len(klar) - 1
		for i in range (n, d+1):
			katsayi = 1
			for j in range(0, n):
				katsayi *= (i - j)
			sonuc += klar[i] * katsayi * math.pow(x, (i-n))
		return sonuc
	"""
	------------------------------------------------------------
	"""

PyApp()
gtk.main()
