from tkinter import *
import db
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql.cursors

class productClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1250x700+300+140")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
    #---------------------------------
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list=[]
        self.sup_list = []
        self.fetch_cat_sup()

        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()


        product_Frame = Frame(self.root,bd=2,relief=RIDGE)
        product_Frame.place(x=10,y=10,width=500,height=680)

    #--------------title--------------
        title = Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        #----------column1-------------
        lbl_category = Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=90)
        lbl_supplier = Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_product_name = Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=230)
        lbl_price = Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=300)
        lbl_qty = Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=370)
        lbl_status = Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=440)

        #txt_category = Entry(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=80)
        
        #----------column2-------------
        cmb_cat = ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=90,width=200)
        cmb_cat.current(0)

        cmb_sup = ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=160,width=200)
        cmb_sup.current(0)

        txt_name = Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=230,width=200)
        txt_price = Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=300,width=200)
        txt_qty = Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=370,width=200)
        
        cmb_status = ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=440,width=200)
        cmb_status.current(0)

        #----------button-------------
        btn_add = Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=20,y=550,width=100,height=40)
        btn_update = Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=130,y=550,width=100,height=40)
        btn_delete = Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=240,y=550,width=100,height=40)
        btn_clear = Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=350,y=550,width=100,height=40)

        #-----------searchFrame-------------
        SearchFrame = LabelFrame(self.root,text="Search Employee",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=550,y=10,width=600,height=80)

        
        #-----------option-----------------
        cmb_search = ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search = Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search = Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #---------Product Details----

        p_frame = Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=550,y=100,width=600,height=590)

        scrolly = Scrollbar(p_frame,orient=VERTICAL)
        scrollx = Scrollbar(p_frame,orient=HORIZONTAL)

        self.product_table = ttk.Treeview(p_frame,columns=("pid","Supplier","Category","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)
        self.product_table.heading("pid",text="P ID")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("name",text="name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Qty")
        self.product_table.heading("status",text="Status")

        self.product_table["show"] = "headings"

        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("status",width=100)
        self.product_table.pack(fill=BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)

        self.show()
        

    #------------------------------------------------------

    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            cur.execute("Select name from category" )
            cat = cur.fetchall()      
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i["name"])
                    
            cur.execute("Select name from supplier" )
            sup = cur.fetchall()
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i["name"])

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)


    def add(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            # Kiểm tra các trường cần thiết
            if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return
            
            # Kiểm tra nếu sản phẩm đã tồn tại
            cur.execute("SELECT * FROM product WHERE name = %s", (self.var_name.get(),))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Product already present, try different", parent=self.root)
                return
            
            # Thêm sản phẩm vào bảng product
            cur.execute("INSERT INTO product (Category, Supplier, name, price, qty, status) VALUES (%s, %s, %s, %s, %s, %s)", 
                        (self.var_cat.get(), self.var_sup.get(), self.var_name.get(), self.var_price.get(), self.var_qty.get(), self.var_status.get()))
            
            # Lấy pid của sản phẩm vừa thêm
            cur.execute("SELECT LAST_INSERT_ID()")
            pid = cur.fetchone()["LAST_INSERT_ID()"]

            # Cập nhật bảng inventory với quantity_in và product_name
            cur.execute("INSERT INTO inventory (product_id, product_name, quantity_in) VALUES (%s, %s, %s)", 
                        (pid, self.var_name.get(), self.var_qty.get()))
            
            conn.commit()
            messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
            self.show()
            self.clear()
            
        except Exception as ex:
            conn.rollback()
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()



    def show(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            cur.execute("Select * from product")
            rows= cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=tuple(row.values()))
            conn.close()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)

    def get_data(self,ev):
        f = self.product_table.focus()
        content =(self.product_table.item(f))
        row = content['values']
        self.var_pid.set(row[0]),
        self.var_cat.set(row[2]),
        self.var_sup.set(row[1]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),                                       
        self.var_status.set(row[6]),

    def update(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Please select product from list",parent = self.root)
            else:
                cur.execute("Select * from product where pid=%s",(self.var_pid.get(),))
                row = cur.fetchone()
                if row ==None:
                    messagebox.showerror("Error","Invalid Product",parent = self.root)
                else:
                    cur.execute("Update product set Category = %s,Supplier = %s,name = %s,price = %s,qty = %s,status = %s where pid = %s",(

                                        self.var_cat.get(),
                                        self.var_sup.get(),
                                        self.var_name.get(),
                                        self.var_price.get(),
                                        self.var_qty.get(),                                       
                                        self.var_status.get(),
                                        self.var_pid.get()
                    ))
                    conn.commit()
                    messagebox.showinfo("Success","Product Updated Successfully",parent = self.root)
                    self.show()
                    conn.close()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)
    
    def delete(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error","Select Product from the list",parent = self.root)
            else:
                cur.execute("Select * from product where pid=%s",(self.var_pid.get(),))
                row = cur.fetchone()
                if row ==None:
                    messagebox.showerror("Error","Invalid Product",parent = self.root)
                else:
                    op = messagebox.askyesno("Confirm","Do you really want to delete?",parent = self.root)
                    if op ==True:

                        cur.execute("Delete from product where pid = %s",(self.var_pid.get()))
                        conn.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)

    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),                                       
        self.var_status.set("Active"),
        self.var_pid.set("")    
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

    def search(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            if self.var_searchby.get() =="Select":
                messagebox.showerror("Error","Select Search By option",parent = self.root)
            elif self.var_searchtxt.get()=="": 
                messagebox.showerror("Error","Search input should be required",parent = self.root)
            else:
                cur.execute("Select * from product where "+self.var_searchby.get()+" Like '%"+self.var_searchtxt.get()+"%'")
                rows= cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=tuple(row.values()))
                else:
                    messagebox.showerror("Error","No record founf!",parent = self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)



if __name__ ==  "__main__":
    root =Tk()
    obj = productClass(root)
    root.mainloop()