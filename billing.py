from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql.cursors
import time
import os
import tempfile
class BillClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1600x1200+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.cart_list = []
        self.chk_print =0
        self.purchased_products = []

        def show_bill_window(self):
            """Hiển thị cửa sổ BillClass trong cửa sổ con"""
            bill_window = Toplevel(self.root)  # Sử dụng Toplevel để tạo cửa sổ con
            bill_window.geometry("800x600+400+200")
            bill_window.title("Bill Window")

            # Thêm giao diện BillClass vào bill_window
            label = Label(bill_window, text="Billing Window", font=("Arial", 16))
            label.pack()



        #-----------title-----------
        # self.icon_title = PhotoImage(file="images/logo.png")
        title = Label(self.root,text="Inventory Management System",compound="left",font=("times new roman",40,"bold"),bg="#010c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #----------btn_logout-------
        btn_logout = Button(self.root,text="Logout",command=self.logout,font=("times new roma",15,"bold"),bg="yellow",cursor="hand2").place(x=1400,y=10,height=50,width=150)

        #---------clock------------
        self.lbl_clock = Label(self.root,text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)
        
        #--------Product Name------
        

        ProductFrame1 = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=10,y=110,width=410,height=720)

        pTitle = Label(ProductFrame1,text="All Products",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

        #---------Product Search Frame------------
        self.var_search = StringVar()

        ProductFrame2 = Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=120)

        lbl_search = Label(ProductFrame2,text="Search Product | By Name ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=10)

        lbl_search = Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=5,y=55)
        txt_search = Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=135,y=58,width=150,height=22)
        btn_search = Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=290,y=56,width=100,height=25)
        btn_show_all = Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=290,y=10,width=100,height=25)
        
    
        #---------Product Details Frame------------
        ProductFrame3 = Frame(ProductFrame1,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=150,width=398,height=520)

        scrolly = Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid",text="PID")
        self.product_Table.heading("name",text="Name")
        self.product_Table.heading("price",text="Price")
        self.product_Table.heading("qty",text="QTY")
        self.product_Table.heading("status",text="Status")
        
        self.product_Table["show"] = "headings"

        self.product_Table.column("pid",width=40)
        self.product_Table.column("name",width=100)
        self.product_Table.column("price",width=100)
        self.product_Table.column("qty",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note =Label(ProductFrame1,text="Note:'Enter 0 Quantity to remove product from the cart'",font=("goudy old style",12),anchor="w",bg="white",fg="red").pack(side=BOTTOM,fill=X)

    #----------Customer Frame-------------
        self.var_cname= StringVar()
        self.var_contact = StringVar()
        CustomerFrame = Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=450,y=110,width=600,height=90)

        cTitle = Label(CustomerFrame,text="Customer Details",font=("goudy old style",20,"bold"),bg="lightgray").pack(side=TOP,fill=X)
        lbl_name = Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=10,y=45)
        txt_name = Entry(CustomerFrame,textvariable=self.var_cname,font=("times new roman",13),bg="lightyellow").place(x=80,y=50,width=150)
        
        lbl_contact = Label(CustomerFrame,text="Contact No.",font=("times new roman",15),bg="white").place(x=250,y=45)
        txt_contact = Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=360,y=50,width=150)
    
    #---------Cal Cart Frame------------
        Cal_Cart_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_Cart_Frame.place(x=450,y=220,width=600,height=610)

    #---------Calculator Frame------------
        # self.var_cal_input = StringVar()

        # Cal_Frame = Frame(Cal_Cart_Frame,bd=9,relief=RIDGE,bg="white")
        # Cal_Frame.place(x=10,y=18,width=280,height=380)

        # txt_cal_input = Entry(Cal_Frame,textvariable=self.var_cal_input,font=("arial",19,"bold"),width=17,bd=10,relief=GROOVE,state="readonly",justify=RIGHT)
        # txt_cal_input.grid(row=0,columnspan=4)

        # btn_7 = Button(Cal_Frame,text=7,font=("arial",15,"bold"),command=lambda:self.get_input(7),bd=5,width=4,pady=15).grid(row=1,column=0)
        # btn_8 = Button(Cal_Frame,text=8,font=("arial",15,"bold"),command=lambda:self.get_input(8),bd=5,width=4,pady=15).grid(row=1,column=1)
        # btn_9 = Button(Cal_Frame,text=9,font=("arial",15,"bold"),command=lambda:self.get_input(9),bd=5,width=4,pady=15).grid(row=1,column=2)
        # btn_sum = Button(Cal_Frame,text="+",font=("arial",15,"bold"),command=lambda:self.get_input("+"),bd=5,width=4,pady=15).grid(row=1,column=3)

        # btn_4 = Button(Cal_Frame,text=4,font=("arial",15,"bold"),command=lambda:self.get_input(4),bd=5,width=4,pady=15).grid(row=2,column=0)
        # btn_5 = Button(Cal_Frame,text=5,font=("arial",15,"bold"),command=lambda:self.get_input(5),bd=5,width=4,pady=15).grid(row=2,column=1)
        # btn_6 = Button(Cal_Frame,text=6,font=("arial",15,"bold"),command=lambda:self.get_input(6),bd=5,width=4,pady=15).grid(row=2,column=2)
        # btn_sub = Button(Cal_Frame,text="-",font=("arial",15,"bold"),command=lambda:self.get_input("-"),bd=5,width=4,pady=15).grid(row=2,column=3)

        # btn_1 = Button(Cal_Frame,text=1,font=("arial",15,"bold"),command=lambda:self.get_input(1),bd=5,width=4,pady=15).grid(row=3,column=0)
        # btn_2 = Button(Cal_Frame,text=2,font=("arial",15,"bold"),command=lambda:self.get_input(2),bd=5,width=4,pady=15).grid(row=3,column=1)
        # btn_3 = Button(Cal_Frame,text=3,font=("arial",15,"bold"),command=lambda:self.get_input(3),bd=5,width=4,pady=15).grid(row=3,column=2)
        # btn_mul = Button(Cal_Frame,text="*",font=("arial",15,"bold"),command=lambda:self.get_input("*"),bd=5,width=4,pady=15).grid(row=3,column=3)

        # btn_0 = Button(Cal_Frame,text="0",font=("arial",15,"bold"),command=lambda:self.get_input(0),bd=5,width=4,pady=15).grid(row=4,column=0)
        # btn_c = Button(Cal_Frame,text="c",font=("arial",15,"bold"),command=self.clear_cal,bd=5,width=4,pady=15).grid(row=4,column=1)
        # btn_eq = Button(Cal_Frame,text="=",font=("arial",15,"bold"),command=self.perform_cal,bd=5,width=4,pady=15).grid(row=4,column=2)
        # btn_div = Button(Cal_Frame,text="/",font=("arial",15,"bold"),command=lambda:self.get_input("/"),bd=5,width=4,pady=15).grid(row=4,column=3)


    #---------Cart Frame------------
        cart_Frame = Frame(Cal_Cart_Frame,bd=3,relief=RIDGE)
        cart_Frame.place(x=80,y=18,width=450,height=440)
        self.cartTitle = Label(cart_Frame,text="Cart \t Total Product: [0]",font=("goudy old style",15,"bold"),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)
        

        scrolly = Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.cartTable = ttk.Treeview(cart_Frame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.cartTable.xview)
        scrolly.config(command=self.cartTable.yview)

        self.cartTable.heading("pid",text="PID")
        self.cartTable.heading("name",text="Name")
        self.cartTable.heading("price",text="Price")
        self.cartTable.heading("qty",text="QTY")
        
        self.cartTable["show"] = "headings"

        self.cartTable.column("pid",width=40)
        self.cartTable.column("name",width=100)
        self.cartTable.column("price",width=90)
        self.cartTable.column("qty",width=40)
        self.cartTable.pack(fill=BOTH,expand=1)
        self.cartTable.bind("<ButtonRelease-1>",self.get_data_cart)
    

    #---------Add Cart Widgets Frame------------
        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWWidgetsFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWWidgetsFrame.place(x=450,y=710,width=600,height=120)

        lbl_p_name = Label(Add_CartWWidgetsFrame,text="Product Name",font=("times new roman",15),bg="white").place(x=10,y=5)
        txt_p_name = Entry(Add_CartWWidgetsFrame,textvariable=self.var_pname,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=10,y=35,width=190,height=22)

        lbl_p_price = Label(Add_CartWWidgetsFrame,text="Price Per Qty",font=("times new roman",15),bg="white").place(x=240,y=5)
        txt_p_price = Entry(Add_CartWWidgetsFrame,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state="readonly").place(x=240,y=35,width=150,height=22)

        lbl_p_qty = Label(Add_CartWWidgetsFrame,text="Quantity",font=("times new roman",15),bg="white").place(x=430,y=5)
        txt_p_qty = Entry(Add_CartWWidgetsFrame,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=430,y=35,width=130,height=22)

        self.lbl_inStock = Label(Add_CartWWidgetsFrame,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_inStock.place(x=10,y=75)

        btn_clear_cart = Button(Add_CartWWidgetsFrame,text="Clear",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=75,width=150,height=30)
        btn_add_cart = Button(Add_CartWWidgetsFrame,text="Add | Update Cart",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=75,width=180,height=30)
        
        #------------billing area------------
        billFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=1080,y=300,width=500,height=550)

        BTitle = Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly = Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)

        self.txt_bill_area = Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        #-----------billing buttons----------
        billMenuFrame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=1080,y=110,width=500,height=170)

        self.lbl_amnt = Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",15,"bold"),bg="orange",fg="black")
        self.lbl_amnt.place(x=2,y=5,width=140,height=70)

        self.lbl_discount = Label(billMenuFrame,text="Discount \n[5%]",font=("goudy old style",15,"bold"),bg="orange",fg="black")
        self.lbl_discount.place(x=150,y=5,width=140,height=70)

        self.lbl_net_pay = Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",15,"bold"),bg="orange",fg="black")
        self.lbl_net_pay.place(x=298,y=5,width=190,height=70)

        btn_print = Button(billMenuFrame,text="Print",cursor="hand2",command=self.print_bill,font=("goudy old style",15,"bold"),bg="orange",fg="black")
        btn_print.place(x=2,y=85,width=140,height=70)

        btn_clear_all = Button(billMenuFrame,text="Clear All",cursor="hand2",command=self.clear_all,font=("goudy old style",15,"bold"),bg="orange",fg="black")
        btn_clear_all.place(x=150,y=85,width=140,height=70)

        btn_generate = Button(billMenuFrame,text="Generate/Save Bill",command=self.generate_bill,cursor="hand2",font=("goudy old style",15,"bold"),bg="orange",fg="black")
        btn_generate.place(x=298,y=85,width=190,height=70)


        #-----------------Footer---------
        footer = Label(self.root,text="IMS-Inventory Management System | Developed By DYL ",font=("times new roman",11),bg="#4d636d",fg="white").place(x=0,y=850,width=1650)

        self.show()
        # self.bill_top()
        self.update_date_time()
    #-----------------All Functions----------------
    
    def get_input(self,num):
        xnum = self.var_cal_input.get()+str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    
    def  perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        cur =conn.cursor()
        try:
            #self.product_Table = ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
            cur.execute("Select pid,name,price,qty,status from product where status='Active'")
            rows= cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=tuple(row.values()))
            conn.close()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to: {str(ex)}",parent = self.root)



    def search(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            if self.var_search.get() == "":
                messagebox.showerror("Error", "Search input should be required", parent=self.root)
            else:
                cur.execute("SELECT pid, name, price, qty, status FROM product WHERE name LIKE '%" + self.var_search.get() + "%' AND status='Active'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=tuple(row.values()))
                else:
                    messagebox.showerror("Error", "No record found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def get_data(self,ev):
        f = self.product_Table.focus()
        content =(self.product_Table.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"In Stock[{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set("1")

    def get_data_cart(self,ev):
        f = self.cartTable.focus()
        content =(self.cartTable.item(f))
        row = content['values']
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_inStock.config(text=f"In Stock[{str(row[4])}]")
        self.var_stock.set(row[4])

    
    def get_purchased_products(self):
        """Lấy danh sách sản phẩm đã mua từ bảng temp_sales."""
        purchased_products = []
        try:
            conn = pymysql.connect(
                host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()
            cur.execute("SELECT product_name, quantity_sold, timestamp FROM temp_sales WHERE user_name = %s", 
                        (self.var_cname.get(),))  # Chỉ lấy dữ liệu của người dùng hiện tại
            rows = cur.fetchall()
            for row in rows:
                purchased_products.append({
                    'product_name': row['product_name'],
                    'quantity': row['quantity_sold'],
                    'timestamp': row['timestamp']  # Lấy thời gian giao dịch
                })
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching purchased products: {str(ex)}", parent=self.root)
        finally:
            conn.close()
        return purchased_products



    def add_update_cart(self):
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select product from the list", parent=self.root)
        elif self.var_qty.get() == "":
            messagebox.showerror("Error", "Quantity is required", parent=self.root)
        elif int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror("Error", "Invalid Quantity", parent=self.root)
        else:
            # Tính toán giá trị tổng cho sản phẩm
            price_cal = float(self.var_qty.get()) * float(self.var_price.get())
            cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

            present = "no"
            index_ = 0
            updated = False  # Biến flag để kiểm tra xem có sự thay đổi nào không

            # Kiểm tra xem sản phẩm đã có trong giỏ chưa
            for row in self.cart_list:
                if self.var_pid.get() == row[0]:
                    present = "yes"
                    break
                index_ += 1

            # Nếu sản phẩm đã có trong giỏ thì hỏi người dùng có muốn cập nhật không
            if present == "yes":
                op = messagebox.askyesno("Confirm", "Product already present\n Do you want to Update| Remove from the cart list!", parent=self.root)
                if op == True:
                    if self.var_qty.get() == "0":
                        self.cart_list.pop(index_)
                    else:
                        self.cart_list[index_][3] = self.var_qty.get()  # Cập nhật số lượng mới
                        updated = True  # Đánh dấu có sự thay đổi
            else:
                self.cart_list.append(cart_data)  # Thêm sản phẩm mới vào giỏ hàng
                updated = True  # Đánh dấu có sự thay đổi

            # Hiển thị lại giỏ hàng
            self.show_cart()
            self.bill_update()

            # Lưu thông tin vào bảng temp_sales chỉ khi có sự thay đổi
            
                  # Mỗi lần thêm hoặc cập nhật sản phẩm, lưu giỏ hàng vào cơ sở dữ liệu





# Lưu thông tin vào bảng temp_sales
    import time

    def save_temp_sales(self):
        try:
            with pymysql.connect(
                host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                cur = conn.cursor()

                for item in self.cart_list:
                    # Lấy thời gian hiện tại
                    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Định dạng thời gian: YYYY-MM-DD HH:MM:SS

                    # Kiểm tra xem sản phẩm đã tồn tại trong temp_sales với cùng product_id và user_name không
                    # Tuy nhiên không so sánh timestamp để đảm bảo mỗi lần có timestamp mới sẽ là một bản ghi mới
                    cur.execute("SELECT id FROM temp_sales WHERE product_id = %s AND user_name = %s", 
                                (item[0], self.var_cname.get()))
                    row = cur.fetchone()

                    if row:  # Nếu sản phẩm đã tồn tại
                        # Mặc dù sản phẩm tồn tại, nhưng mỗi lần timestamp khác sẽ thêm mới một bản ghi
                        cur.execute("""
                            INSERT INTO temp_sales (product_id, product_name, quantity_sold, price, user_name, timestamp)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (item[0], item[1], item[3], item[2], self.var_cname.get(), timestamp))
                    else:  # Nếu sản phẩm chưa tồn tại, thêm mới luôn
                        cur.execute("""
                            INSERT INTO temp_sales (product_id, product_name, quantity_sold, price, user_name, timestamp)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (item[0], item[1], item[3], item[2], self.var_cname.get(), timestamp))

                conn.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        except Exception as ex:
            messagebox.showerror("Error", f"Error saving to temp_sales: {str(ex)}", parent=self.root)







    # Cập nhật danh sách sản phẩm đã mua
    def update_inventory(self):
        """Cập nhật kho hàng sau khi mua."""
        self.purchased_products.clear()  # Xóa danh sách cũ

        for item in self.cart_list:
            # Thêm sản phẩm vào danh sách mua
            product_data = {
                'product_id': item[0],
                'product_name': item[1],
                'quantity_sold': int(item[3])  # Đảm bảo số lượng là kiểu int
            }
            self.purchased_products.append(product_data)

        # Cập nhật kho hàng
        self._update_inventory_in_database()

    def _update_inventory_in_database(self):
        """Cập nhật kho hàng trong cơ sở dữ liệu."""
        try:
            # Mở kết nối với cơ sở dữ liệu
            with pymysql.connect(
                host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor
            ) as conn:
                cur = conn.cursor()
                update_query = """
                    UPDATE inventory 
                    SET quantity_out = quantity_out + %s, 
                        current_quantity = quantity_in - quantity_out 
                    WHERE product_id = %s
                """

                # Cập nhật tất cả các sản phẩm trong một lần
                for item in self.purchased_products:
                    cur.execute(update_query, (item['quantity_sold'], item['product_id']))

                # Lưu lại thay đổi
                conn.commit()

            # Hiển thị thông báo thành công
            messagebox.showinfo("Success", "Inventory updated successfully", parent=self.root)

        except Exception as ex:
            # Hiển thị thông báo lỗi nếu có vấn đề
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay =0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt +(float(row[2])*int(row[3]))

        self.discount =(self.bill_amnt*5)/100
        self.net_pay =self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Bill Amnt\n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Net Pay\n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart \t Total Product: [{str(len(self.cart_list))}]")

    def show_cart(self):
        try:
            self.cartTable.delete(*self.cartTable.get_children())
            for row in self.cart_list:
                self.cartTable.insert('', END, values=tuple(row))  # Change here
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


    def generate_bill(self):
        if self.var_cname.get()=="" or self.var_contact.get()=="":
            messagebox.showerror("Error",f'Customer Details are required',parent = self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f'Please Add product to the Cart',parent = self.root)
        
        else:
            #----------Bill Top----------
            self.bill_top()
            #----------Bill Mid----------
            self.bill_middle()
            #----------Bill Bot----------
            self.bill_bottom()
            
            # Open the file in write mode ('w') and use 'utf-8' encoding to handle text properly
            with open(f'bill/{str(self.invoice)}.txt', 'w', encoding='utf-8') as fp:
                # Get the content from the text widget and write it to the file
                bill_content = self.txt_bill_area.get("1.0", "end-1c")  # "end-1c" avoids writing an extra newline
                fp.write(bill_content)
        
            self.save_temp_sales()

# After writing to the file, show a messagebox

            messagebox.showinfo("Saved","Bill has been generated/Save in Backend",parent = self.root)
            self.chk_print=1
        
    def bill_top(self):
        self.invoice = int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp = f'''
\t\t\tXYZ-Inventory 
\t Phone No. 033936*****, Dat-030803
{str("="*56)}
  Customer Name: {self.var_cname.get()}
  Ph no. : {self.var_contact.get()}
  Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*56)}
  Product Name\t\t\t\tQTY\tPrice
{str("="*56)}
        '''
        self.txt_bill_area.delete("1.0",END)
        self.txt_bill_area.insert("1.0",bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp = f'''
{str("="*56)}
  Bill Amount\t\t\t\t\tRs.{self.bill_amnt}
  Discount\t\t\t\t\tRs.{self.discount}
  Net Pay\t\t\t\t\tRs.{self.net_pay}
{str("="*56)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)


    def bill_middle(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            for row in self.cart_list:
                pid = row[0]
                name = row[1]
                qty = int(row[4])-int(row[3])
                if int(row[3]) ==int(row[4]):
                    status = "Inactive"
                if int(row[3])!=int(row[4]):
                    status="Active"

                price = float(row[2])*int(row[3])
                price=str(price)
                self.txt_bill_area.insert(END,"\n   "+name+"\t\t\t\t"+row[3]+"\tRs."+price)
            #--------------Update qty in product table---------    
                cur.execute("Update product set qty=%s,status = %s where pid=%s",(
                    qty,
                    status,
                    pid
                ))
                conn.commit()
            conn.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



    def clear_cart(self):
        self.var_pid.set("")
        self.var_pname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_inStock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set("")
        self.var_contact.set("")
        self.txt_bill_area.delete("1.0",END)
        self.cartTitle.config(text=f"Cart \t Total Product: [0]")
        self.var_search.set("")
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ =time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)


    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent = self.root)
            new_file = tempfile.mktemp(".txt")
            open(new_file,"w").write(self.txt_bill_area.get("1.0",END))
            os.startfile(new_file,"print")
        else:
            messagebox.showerror("Print","Please generate bill, to print the receipt",parent = self.root)
            


    def logout(self):
        self.root.destroy()
        os.system("python login1.py")

if __name__ ==  "__main__":
    root =Tk()
    obj = BillClass(root)
    root.mainloop()