from tkinter import *
import db
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql.cursors
import os
import re
class salesClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1250x700+300+140")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice = StringVar()
    #----------title----------------
        lbl_title = Label(self.root,text="View Customer Bills",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice = Label(self.root,text="Invoice No.",font=("times new roman",15),bg="white").place(x=50,y=100)
        txt_invoice = Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)

        btn_search = Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg = "#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg = "lightgray",cursor="hand2").place(x=500,y=100,width=120,height=28)


        #---------Bill List-------
        sales_Frame = Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=160,width=250,height=450)

        scrolly = Scrollbar(sales_Frame,orient=VERTICAL)
        self.Sales_List = Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.Sales_List.yview)
        self.Sales_List.pack(fill=BOTH,expand=1)

        self.Sales_List.bind("<ButtonRelease-1>",self.get_data)
        #---------Bill Area-------
        bill_Frame = Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=330,y=160,width=450,height=450)

        lbl_title2 = Label(bill_Frame,text="Customer Bills Area",font=("goudy old style",20),bg="orange").pack(side=TOP,fill=X)


        scrolly2 = Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area = Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

    #-----------Image----------
        self.bill_photo = Image.open("images/sales.jpg")
        self.bill_photo = self.bill_photo.resize((450,350))
        self.bill_photo = ImageTk.PhotoImage(self.bill_photo)

        lbl_image = Label(self.root,image=self.bill_photo,bd=0)
        lbl_image.place(x=800,y=350)


         # Calculate Netpay Button and Label
        btn_calculate = Button(self.root, text="Calculate Bill", command=self.calculate_netpay,
                               font=("times new roman", 15, "bold"), bg="#4caf50", fg="white", cursor="hand2")
        btn_calculate.place(x=850, y=100, width=200, height=40)


        self.lbl_bill_total = Label(self.root, text="Total Bill Amount: $0.00", font=("times new roman", 15),
                                    bg="#50ded7", fg="black")
        self.lbl_bill_total.place(x=850, y=170, width=300, height=40)

        self.lbl_discount_total = Label(self.root, text="Total Discount: $0.00", font=("times new roman", 15),
                                        bg="#e15fe8", fg="black")
        self.lbl_discount_total.place(x=850, y=230, width=300, height=40)


        self.lbl_netpay = Label(self.root, text="Netpay total: $0.00", font=("times new roman", 15), bg="#eb5e5e", fg="black")
        self.lbl_netpay.place(x=850, y=290, width=300, height=40)


        self.show()
    #----------------------
    def show(self):
        self.bill_list[:]
        self.Sales_List.delete(0,END)
        #print(os.listdir("../PYTHONBTL"))
        for i in os.listdir("bill"):
            if i.split(".")[-1]=="txt":
                self.Sales_List.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_ = self.Sales_List.curselection()
        file_name = self.Sales_List.get(index_)
        print(file_name)
        self.bill_area.delete('1.0',END)
        fp = open(f'bill/{file_name}',"r")
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice no. should be required",parent = self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                fp = open(f'bill/{self.var_invoice.get()}.txt',"r")
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Invalid Invoice No.",parent = self.root)

    def clear(self):
        self.show()
        self.bill_area.delete('1.0',END)


    

    def calculate_netpay(self):
        total_bill_amount = 0.0
        total_discount = 0.0
        total_netpay = 0.0

        for invoice in self.bill_list:
            try:
                with open(f'bill/{invoice}.txt', "r") as fp:
                    found_netpay = False
                    for line in fp:
                        if "Bill Amount" in line:
                            match = re.search(r'Rs\.(\d+\.\d+)', line)
                            if match:
                                bill_amount_str = match.group(1)
                                try:
                                    bill_amount = float(bill_amount_str.replace(",", ""))
                                    total_bill_amount += bill_amount
                                except ValueError:
                                    print(f"Invalid bill amount value in file {invoice}.txt: {bill_amount_str}")
                        elif "Discount" in line:
                            match = re.search(r'Rs\.(\d+\.\d+)', line)
                            if match:
                                discount_str = match.group(1)
                                try:
                                    discount = float(discount_str.replace(",", ""))
                                    total_discount += discount
                                except ValueError:
                                    print(f"Invalid discount value in file {invoice}.txt: {discount_str}")
                        elif "Net Pay" in line:
                            match = re.search(r'Rs\.(\d+\.\d+)', line)
                            if match:
                                netpay_str = match.group(1)
                                try:
                                    netpay = float(netpay_str.replace(",", ""))
                                    total_netpay += netpay
                                    found_netpay = True
                                except ValueError:
                                    print(f"Invalid netpay value in file {invoice}.txt: {netpay_str}")

                    if not found_netpay:
                        print(f"Net Pay not found in file {invoice}.txt")

            except FileNotFoundError:
                messagebox.showerror("Error", f"File {invoice}.txt not found. Skipping...")

        self.lbl_bill_total.config(text=f"Total Bill Amount: ${total_bill_amount:.2f}")
        self.lbl_discount_total.config(text=f"Total Discount: ${total_discount:.2f}")
        self.lbl_netpay.config(text=f"Netpay total: ${total_netpay:.2f}")





if __name__ ==  "__main__":
    root =Tk()
    obj = salesClass(root)
    root.mainloop()