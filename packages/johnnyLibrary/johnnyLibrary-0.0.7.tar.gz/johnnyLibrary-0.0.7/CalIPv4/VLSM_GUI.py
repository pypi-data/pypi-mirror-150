from tkinter import *

class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()
#widget
    def create_widgets(self):
        self.inst_lbl1 = Label(self, text = "Wprowadź ilość hostów:")
        self.inst_lbl1.grid(row = 0, column = 0, columnspan = 2, sticky = W)
        self.inst_lbl2 = Label(self, text = "Wprowadź adres IP:")
        self.inst_lbl2.grid(row = 2, column = 0, columnspan = 2, sticky = W)
        #wpis liczby
        self.pw_ent1 = Entry(self)
        self.pw_ent1.grid(row = 1, column = 0, sticky = W)
        self.pw_ent2 = Entry(self)
        self.pw_ent2.grid(row = 3, column = 0, sticky = W)
        #button run
        self.submit_bttn = Button(self, text = "Run", command = self.reveal)
        self.submit_bttn.grid(row = 4, column = 0, sticky = W)
        #rozwiazania
        self.secret_txt1 = Text(self, width=60, height=2, wrap=WORD)
        self.secret_txt1.grid(row=5, column=0, columnspan=2, sticky=W)

    def reveal(self):
        ile_host1 = self.pw_ent1.get()
        lista = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        y = []
        for i in ile_host1:
            if i not in lista:
                y.append('nie ma')
            else:
                y.append('siema')

        ile = y.count('nie ma')
        if ile >= 1:
            raise ValueError("zle wpisanie w ilosci hostow")

        ile_host = int(ile_host1)
        adres_IP = self.pw_ent2.get()

        lista2 = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        x = []
        for i in adres_IP:
            if i not in lista2:
                x.append('nie ma')
            else:
                x.append('siema')

        ile = x.count('siema')
        if ile <= 8:
            raise ValueError("zle wpisanie w IP")

        zakre_host_1 = range(2147483647, 99999999999999999999999999)
        zakre_host_2 = range(1073741823, 2147483647)
        zakre_host_3 = range(536870911, 1073741823)
        zakre_host_4 = range(268435456, 536870911)
        zakre_host_5 = range(134217726, 268435455)
        zakre_host_6 = range(67108862, 134217726)
        zakre_host_7 = range(33554430, 67108862)
        zakre_host_8 = range(16777214, 33554430)
        zakre_host_9 = range(8388606, 16777214)
        zakre_host_10 = range(4194302, 8388606)
        zakre_host_11 = range(2097150, 4194302)
        zakre_host_12 = range(1048574, 2097150)
        zakre_host_13 = range(524286, 1048574)
        zakre_host_14 = range(262142, 524286)
        zakre_host_15 = range(131070, 262142)
        zakre_host_16 = range(65534, 131070)
        zakre_host_17 = range(32766, 65534)
        zakre_host_18 = range(16382, 32766)
        zakre_host_19 = range(8190, 16382)
        zakre_host_20 = range(4094, 8190)
        zakre_host_21 = range(2046, 4094)
        zakre_host_22 = range(1022, 2046)
        zakre_host_23 = range(510, 1022)
        zakre_host_24 = range(254, 510)
        zakre_host_25 = range(126, 254)
        zakre_host_26 = range(62, 126)
        zakre_host_27 = range(30, 62)
        zakre_host_28 = range(14, 30)
        zakre_host_29 = range(6, 14)
        zakre_host_30 = range(2, 6)
        zakre_host_31 = range(0, 2)
        zakre_host_32 = range(0)
        zakre_host_33 = range(0)

        oktet1 = []
        oktet2 = []
        oktet3 = []
        oktet4 = []

        if ile_host in zakre_host_1:
            oktet1.append('0')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_2:
            oktet1.append('128')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_3:
            oktet1.append('192')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_4:
            oktet1.append('224')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_5:
            oktet1.append('240')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_6:
            oktet1.append('248')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_7:
            oktet1.append('252')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_8:
            oktet1.append('254')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_9:
            oktet1.append('255')
            oktet2.append('0')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_10:
            oktet1.append('255')
            oktet2.append('128')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_11:
            oktet1.append('255')
            oktet2.append('192')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_12:
            oktet1.append('255')
            oktet2.append('224')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_13:
            oktet1.append('255')
            oktet2.append('240')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_14:
            oktet1.append('255')
            oktet2.append('248')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_15:
            oktet1.append('255')
            oktet2.append('252')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_16:
            oktet1.append('255')
            oktet2.append('254')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_17:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('0')
            oktet4.append('0')
        elif ile_host in zakre_host_18:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('128')
            oktet4.append('0')
        elif ile_host in zakre_host_19:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('192')
            oktet4.append('0')
        elif ile_host in zakre_host_20:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('224')
            oktet4.append('0')
        elif ile_host in zakre_host_21:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('240')
            oktet4.append('0')
        elif ile_host in zakre_host_22:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('248')
            oktet4.append('0')
        elif ile_host in zakre_host_23:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('252')
            oktet4.append('0')
        elif ile_host in zakre_host_24:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('254')
            oktet4.append('0')
        elif ile_host in zakre_host_25:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('0')
        elif ile_host in zakre_host_26:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('128')
        elif ile_host in zakre_host_27:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('192')
        elif ile_host in zakre_host_28:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('224')
        elif ile_host in zakre_host_29:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('240')
        elif ile_host in zakre_host_30:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('248')
        elif ile_host in zakre_host_31:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('252')
        elif ile_host in zakre_host_32:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('254')
        elif ile_host in zakre_host_33:
            oktet1.append('255')
            oktet2.append('255')
            oktet3.append('255')
            oktet4.append('255')

        oktet1a = ''.join(map(str, oktet1))
        oktet1b = int(oktet1a)
        oktet2a = ''.join(map(str, oktet2))
        oktet2b = int(oktet2a)
        oktet3a = ''.join(map(str, oktet3))
        oktet3b = int(oktet3a)
        oktet4a = ''.join(map(str, oktet4))
        oktet4b = int(oktet4a)

        # oktety
        ip = adres_IP.split('.')

        x1 = (int(ip[0]))
        x2 = (int(ip[1]))
        x3 = (int(ip[2]))
        x4 = (int(ip[3]))

        # ERROR
        if x1 > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif x2 > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif x3 > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif x4 > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif oktet1b > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif oktet2b > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif oktet3b > 255:
            raise ValueError("Liczba jest zbyt wysoka")
        elif oktet4b > 255:
            raise ValueError("Liczba jest zbyt wysoka")

        and1 = x1 & oktet1b
        and2 = x2 & oktet2b
        and3 = x3 & oktet3b
        and4 = x4 & oktet4b

        adres_sieci_int = (f"{and1}.{and2}.{and3}.{and4}")
        adres_sieci_bin = ('{0:08b}.{1:08b}.{2:08b}.{3:08b}'.format(int(and1), int(and2), int(and3), int(and4)))

        ip_bin = ('{0:08b}.{1:08b}.{2:08b}.{3:08b}'.format(x1, x2, x3, x4))
        maska_bin = ('{0:08b}.{1:08b}.{2:08b}.{3:08b}'.format(oktet1b, oktet2b, oktet3b, oktet4b))

        oktet_neg = []
        for i1 in maska_bin:
            if i1 == '1':
                x1 = i1.replace('1', '0')
            else:
                x1 = i1.replace('0', '1')
            oktet_neg.append(x1)

        negacja1 = ''.join(map(str, oktet_neg))
        negacja_ = negacja1.split('.')

        liczenie_jedynek1 = (negacja_[0].count(str(1)))
        liczenie_jedynek2 = (negacja_[1].count(str(1)))
        liczenie_jedynek3 = (negacja_[2].count(str(1)))
        liczenie_jedynek4 = (negacja_[3].count(str(1)))

        oktet_liczenie1 = []
        oktet_liczenie2 = []
        oktet_liczenie3 = []
        oktet_liczenie4 = []

        if liczenie_jedynek1 == 0:
            oktet_liczenie1.append(0)
        elif liczenie_jedynek1 == 1:
            oktet_liczenie1.append(1)
        elif liczenie_jedynek1 == 2:
            oktet_liczenie1.append(3)
        elif liczenie_jedynek1 == 3:
            oktet_liczenie1.append(7)
        elif liczenie_jedynek1 == 4:
            oktet_liczenie1.append(15)
        elif liczenie_jedynek1 == 5:
            oktet_liczenie1.append(31)
        elif liczenie_jedynek1 == 6:
            oktet_liczenie1.append(63)
        elif liczenie_jedynek1 == 7:
            oktet_liczenie1.append(127)
        elif liczenie_jedynek1 == 8:
            oktet_liczenie1.append(255)

        if liczenie_jedynek2 == 0:
            oktet_liczenie2.append(0)
        elif liczenie_jedynek2 == 1:
            oktet_liczenie2.append(1)
        elif liczenie_jedynek2 == 2:
            oktet_liczenie2.append(3)
        elif liczenie_jedynek2 == 3:
            oktet_liczenie2.append(7)
        elif liczenie_jedynek2 == 4:
            oktet_liczenie2.append(15)
        elif liczenie_jedynek2 == 5:
            oktet_liczenie2.append(31)
        elif liczenie_jedynek2 == 6:
            oktet_liczenie2.append(63)
        elif liczenie_jedynek2 == 7:
            oktet_liczenie2.append(127)
        elif liczenie_jedynek2 == 8:
            oktet_liczenie2.append(255)

        if liczenie_jedynek3 == 0:
            oktet_liczenie3.append(0)
        elif liczenie_jedynek3 == 1:
            oktet_liczenie3.append(1)
        elif liczenie_jedynek3 == 2:
            oktet_liczenie3.append(3)
        elif liczenie_jedynek3 == 3:
            oktet_liczenie3.append(7)
        elif liczenie_jedynek3 == 4:
            oktet_liczenie3.append(15)
        elif liczenie_jedynek3 == 5:
            oktet_liczenie3.append(31)
        elif liczenie_jedynek3 == 6:
            oktet_liczenie3.append(63)
        elif liczenie_jedynek3 == 7:
            oktet_liczenie3.append(127)
        elif liczenie_jedynek3 == 8:
            oktet_liczenie3.append(255)

        if liczenie_jedynek4 == 0:
            oktet_liczenie4.append(0)
        elif liczenie_jedynek4 == 1:
            oktet_liczenie4.append(1)
        elif liczenie_jedynek4 == 2:
            oktet_liczenie4.append(3)
        elif liczenie_jedynek4 == 3:
            oktet_liczenie4.append(7)
        elif liczenie_jedynek4 == 4:
            oktet_liczenie4.append(15)
        elif liczenie_jedynek4 == 5:
            oktet_liczenie4.append(31)
        elif liczenie_jedynek4 == 6:
            oktet_liczenie4.append(63)
        elif liczenie_jedynek4 == 7:
            oktet_liczenie4.append(127)
        elif liczenie_jedynek4 == 8:
            oktet_liczenie4.append(255)

        potegi1 = ''.join(map(str, oktet_liczenie1))
        potegi1a = int(potegi1)
        potegi2 = ''.join(map(str, oktet_liczenie2))
        potegi2a = int(potegi2)
        potegi3 = ''.join(map(str, oktet_liczenie3))
        potegi3a = int(potegi3)
        potegi4 = ''.join(map(str, oktet_liczenie4))
        potegi4a = int(potegi4)

        wynik_not1 = and1 + potegi1a
        wynik_not2 = and2 + potegi2a
        wynik_not3 = and3 + potegi3a
        wynik_not4 = and4 + potegi4a

        wynik_not = (f"{wynik_not1}.{wynik_not2}.{wynik_not3}.{wynik_not4}")
        wynik_not_str = wynik_not.split('.')
        wynik_not_bin = ("{0:08b}.{1:08b}.{2:08b}.{3:08b}".format(wynik_not1, wynik_not2, wynik_not3, wynik_not4))

        wynikkk = (f"\nPodsieć: {adres_sieci_int}-{wynik_not}")

        self.secret_txt1.delete(0.0, END)
        self.secret_txt1.insert(0.0, wynikkk)


root = Tk()
root.title("VLSM")
root.geometry("430x400")
app = Application(root)
root.mainloop()
