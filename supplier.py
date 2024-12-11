from tkinter import *
import db
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql.cursors

class supplierClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1250x700+300+140")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        #---------------------------------
        #All Variables
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()


        self.var_sup_invoice = StringVar()

        self.var_contact = StringVar()
        self.var_name = StringVar()
        

        #-----------searchFrame-------------
        # SearchFrame = LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        # #SearchFrame.place(x=300,y=20,width=600,height=70)

        #-----------option-----------------
        lbl_search = Label(self.root,text="Search By Invoice No.",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)


        txt_search = Entry(self.root,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=890,y=80)
        btn_search = Button(self.root,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=1100,y=80,width=100,height=30)

        #title
        title = Label(self.root,text="Supplier Details",font=("goudy old style",20,"bold"),bg="#0f4d7d",fg="white").place(x=80,y=10,width=1100,height=50)

        #---------content----------------
        #---------row1------------------
        lbl_supplier_invoice = Label(self.root,text="Invoice No.",font=("goudy old style",15),bg="white").place(x=80,y=80)      
        txt_supplier_invoice = Entry(self.root,textvariable=self.var_sup_invoice,font=("goudy old style",15),bg="lightyellow").place(x=200,y=80,width=180)
        
        #---------row2------------------
        lbl_name = Label(self.root,text="Name",font=("goudy old style",15),bg="white").place(x=80,y=130)      
        txt_name = Entry(self.root,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=200,y=130,width=180)
        
        #---------row3------------------
        lbl_contact = Label(self.root,text="Contact",font=("goudy old style",15),bg="white").place(x=80,y=180)     
        txt_contact = Entry(self.root,textvariable=self.var_contact,font=("goudy old style",15),bg="lightyellow").place(x=200,y=180,width=180)
        

        #---------row4------------------
        lbl_address = Label(self.root,text="Description",font=("goudy old style",15),bg="white").place(x=80,y=230)
        self.txt_desc = Text(self.root,font=("goudy old style",15),bg="lightyellow")
        self.txt_desc.place(x=200,y=230,width=470,height=120)
        

        #----------button-------------
        btn_add = Button(self.root,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=200,y=400,width=110,height=35)
        btn_update = Button(self.root,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=320,y=400,width=110,height=35)
        btn_delete = Button(self.root,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=440,y=400,width=110,height=35)
        btn_clear = Button(self.root,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=560,y=400,width=110,height=35)

        #---------Supplier Details----

        self.im1 = Image.open("images/sup1.jpg")
        self.im1 = self.im1.resize((550,220))
        self.im1 = ImageTk.PhotoImage(self.im1)

        self.lbl_im1 = Label(self.root,image=self.im1,bd=2,relief=RAISED)
        self.lbl_im1.place(x=400,y=450)

        emp_frame = Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=150,width=500,height=290)

        scrolly = Scrollbar(emp_frame,orient=VERTICAL)
        scrollx = Scrollbar(emp_frame,orient=HORIZONTAL)

        self.supplierTable = ttk.Treeview(emp_frame,columns=("invoice","name","contact","desc"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice",text="Invoice No.")
        self.supplierTable.heading("name",text="Name")
        self.supplierTable.heading("contact",text="Contact")
        self.supplierTable.heading("desc",text="Description")
        
        self.supplierTable["show"] = "headings"

        self.supplierTable.column("invoice",width=90)
        self.supplierTable.column("name",width=100)
        self.supplierTable.column("contact",width=100)
        self.supplierTable.column("desc",width=100)
        self.supplierTable.pack(fill=BOTH,expand=1)
        self.supplierTable.bind("<ButtonRelease-1>",self.get_data)

        self.show()
    #------------------------------------------------------
    
    def add(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            # Kiểm tra tất cả các trường bắt buộc
            if self.var_sup_invoice.get() == "" or self.var_name.get() == "" or self.var_contact.get() == "" or self.txt_desc.get('1.0', END).strip() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                # Kiểm tra trùng lặp Invoice
                cur.execute("SELECT * FROM supplier WHERE invoice=%s", (self.var_sup_invoice.get(),))
                row_invoice = cur.fetchone()
                if row_invoice is not None:
                    messagebox.showerror("Error", "Invoice no. already assigned, try different", parent=self.root)
                    return

                # Kiểm tra trùng lặp Name
                cur.execute("SELECT * FROM supplier WHERE name=%s", (self.var_name.get(),))
                row_name = cur.fetchone()
                if row_name is not None:
                    messagebox.showerror("Error", "Supplier name already exists, try different", parent=self.root)
                    return

                # Kiểm tra trùng lặp Contact
                cur.execute("SELECT * FROM supplier WHERE contact=%s", (self.var_contact.get(),))
                row_contact = cur.fetchone()
                if row_contact is not None:
                    messagebox.showerror("Error", "Contact number already exists, try different", parent=self.root)
                    return

                # Thêm mới
                cur.execute("INSERT INTO supplier (invoice, name, contact, `desc`) VALUES (%s, %s, %s, %s)", (
                    self.var_sup_invoice.get(),
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.txt_desc.get('1.0', END).strip(),
                ))
                conn.commit()
                messagebox.showinfo("Success", "Supplier Added Successfully", parent=self.root)
                self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()


    def show(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            cur.execute("Select * from supplier")
            rows= cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert('',END,values=tuple(row.values()))
            conn.close()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)

    def get_data(self,ev):
        f = self.supplierTable.focus()
        content =(self.supplierTable.item(f))
        row = content['values']
        #print(row)
        self.var_sup_invoice.set(row[0]),
        self.var_name.set(row[1]),
        self.var_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),

    def update(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent = self.root)
            else:
                cur.execute("Select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row ==None:
                    messagebox.showerror("Error","Invalid Invoice",parent = self.root)
                else:
                    cur.execute("Update supplier set name = %s,contact = %s,`desc` = %s where invoice = %s",(

                                        self.var_name.get(),
                                        self.var_contact.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_sup_invoice.get(),
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Supplier Updated Successfully",parent = self.root)
                    self.show()
                    conn.close()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)
    
    def delete(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_sup_invoice.get()=="":
                messagebox.showerror("Error","Invoice no. must be required",parent = self.root)
            else:
                cur.execute("Select * from supplier where invoice=%s",(self.var_sup_invoice.get(),))
                row = cur.fetchone()
                if row ==None:
                    messagebox.showerror("Error","Invalid Invoice",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent = self.root)
                    if op ==True:

                        cur.execute("Delete from supplier where invoice = %s",(self.var_sup_invoice.get()))
                        conn.commit()
                        messagebox.showinfo("Delete","Supplier Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)

    def clear(self):
        self.var_sup_invoice.set(""),
        self.var_name.set(""),
        self.var_contact.set(""),                                       
        self.txt_desc.delete('1.0',END),
        self.var_searchtxt.set("")
        self.show()

    def search(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_searchtxt.get()=="": 
                messagebox.showerror("Error","Invoice no. should be required",parent = self.root)
            else:
                cur.execute("Select * from supplier where invoice = %s ",(self.var_searchtxt.get()))
                row= cur.fetchone()
                if row!=None:
                    self.supplierTable.delete(*self.supplierTable.get_children())
                    self.supplierTable.insert('',END,values=tuple(row.values()))
                else:
                    messagebox.showerror("Error","No record founf!",parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)


if __name__ ==  "__main__":
    root =Tk()
    obj = supplierClass(root)
    root.mainloop()