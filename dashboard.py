from tkinter import *
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from billing import BillClass
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from inventory import InventoryManagement
import os
import pymysql.cursors
from tkinter import messagebox
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1600x1200+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="#83d1eb")

        
        
        #-----------title-----------
        self.icon_title = PhotoImage(file="images/logo.png")
        title = Label(self.root, text="Inventory Management System", compound="left", font=("times new roman", 40, "bold"),
                      bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)

        #----------btn_logout-------
        btn_logout = Button(self.root, text="Logout", command=self.logout, font=("times new roman", 15, "bold"),
                            bg="yellow", cursor="hand2").place(x=1400, y=10, height=50, width=150)

        #---------clock------------
        self.lbl_clock = Label(self.root, text="Welcome to Inventory Management System\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #---------Left Menu--------
        self.MenuLogo = Image.open("images/dash.jpg")
        self.MenuLogo = self.MenuLogo.resize((260, 250))
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=260, height=750)

        lbl_MenuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_MenuLogo.pack(side=TOP, fill=X)

        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)

        # Define button height
        button_height = 50  # Set a standard height for all buttons
        button_width = 260  # Set a standard width for all buttons

        btn_employee = Button(LeftMenu, text="Employee", command=self.employee, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_employee.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_supplier = Button(LeftMenu, text="Supplier", command=self.supplier, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_supplier.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_category = Button(LeftMenu, text="Category", command=self.category, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_category.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_product = Button(LeftMenu, text="Products", command=self.product, compound=LEFT, padx=5, anchor="w",
                             font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_product.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_sales = Button(LeftMenu, text="Sales", command=self.sales, compound=LEFT, padx=5, anchor="w",
                           font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_sales.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_inventory = Button(LeftMenu, text="Inventory", command=self.inventory, compound=LEFT, padx=5, anchor="w",
                               font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_inventory.pack(side=TOP, fill=X, padx=10, pady=5)

        btn_exit = Button(LeftMenu, text="Exit", compound=LEFT, padx=5, anchor="w", command=self.exit,
                          font=("times new roman", 20, "bold"), bg="#ebe783", bd=3, cursor="hand2")
        btn_exit.pack(side=TOP, fill=X, padx=10, pady=5)

        #--------- Refresh Button ---------
        btn_refresh = Button(self.root, text="Refresh", command=self.refresh_charts, font=("times new roman", 12, "bold"),
                             bg="yellow", cursor="hand2")
        btn_refresh.place(x=1400, y=105, height=30, width=120)  # Placed right below the clock bar
        
        #--------content------------

        #-----------footer------------
        lbl_footer = Label(self.root, text="DYL-Inventory Management System\n Contact: 0339999999 ",
                           font=("times new roman", 12), bg="#4d636d", fg="white")
        lbl_footer.place(x=0, y=855, relwidth=1, height=40)

        self.show_charts()

    def inventory(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = InventoryManagement(self.new_win)

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_charts(self):
        """Xóa và cập nhật lại biểu đồ với dữ liệu mới."""
        if hasattr(self, 'canvas1'):
            self.canvas1.get_tk_widget().destroy()
        if hasattr(self, 'canvas2'):
            self.canvas2.get_tk_widget().destroy()
        self.show_charts()

    def show_charts(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            # Biểu đồ cột
            cur.execute("SELECT Supplier, COUNT(*) AS product_count FROM product GROUP BY Supplier")
            supplier_data = cur.fetchall()
            supplier_names = [item['Supplier'] for item in supplier_data]
            product_counts = [item['product_count'] for item in supplier_data]

            fig1 = Figure(figsize=(6, 4), dpi=90)
            ax1 = fig1.add_subplot(111)
            ax1.bar(supplier_names, product_counts, color='orange')
            ax1.set_title("Product Count Assigned To Supplier")
            ax1.set_xlabel("Nhà cung cấp")
            ax1.set_ylabel("Số lượng sản phẩm")

            self.canvas1 = FigureCanvasTkAgg(fig1, self.root)
            self.canvas1.get_tk_widget().place(x=300, y=150, width=600, height=350)
            self.canvas1.draw()

            # Biểu đồ tròn
            cur.execute("SELECT Category, SUM(qty) AS total_qty FROM product GROUP BY Category")
            inventory_data = cur.fetchall()
            categories = [item['Category'] for item in inventory_data]
            total_qtys = [item['total_qty'] for item in inventory_data]

            fig2 = Figure(figsize=(6, 4), dpi=100)
            ax2 = fig2.add_subplot(111)
            ax2.pie(total_qtys, labels=categories, autopct='%1.1f%%', startangle=140)
            ax2.set_title("Distribution of inventory by product type")

            self.canvas2 = FigureCanvasTkAgg(fig2, self.root)
            self.canvas2.get_tk_widget().place(x=950, y=150, width=600, height=350)
            self.canvas2.draw()

            # Biểu đồ trạng thái Complete và Pending
            cur.execute("""
                SELECT 
                    SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) AS complete_count,
                    SUM(CASE WHEN status IS NULL OR status = '' THEN 1 ELSE 0 END) AS pending_count
                FROM temp_sales
            """)

            status_data = cur.fetchone()

            complete_count = status_data['complete_count']
            pending_count = status_data['pending_count']

            fig3 = Figure(figsize=(6, 3), dpi=100)
            ax3 = fig3.add_subplot(111)

            # Dữ liệu và nhãn số lượng
            sizes = [complete_count, pending_count]
            labels = [f"Complete ({complete_count})", f"Pending ({pending_count})"]

            ax3.pie(
                sizes,
                labels=labels,
                colors=["pink", "orange"],
                startangle=140
            )
            ax3.set_title("Complete vs Pending Orders")

            self.canvas3 = FigureCanvasTkAgg(fig3, self.root)
            self.canvas3.get_tk_widget().place(x=650, y=525, width=500, height=325)
            self.canvas3.draw()


        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            cur.close()
            conn.close()


    def refresh_charts(self):
        """Cập nhật lại các biểu đồ mà không cần khởi động lại chương trình."""
        # Xóa các biểu đồ hiện tại
        if hasattr(self, 'canvas1'):
            self.canvas1.get_tk_widget().destroy()
        if hasattr(self, 'canvas2'):
            self.canvas2.get_tk_widget().destroy()
        if hasattr(self, 'canvas3'):  # Xóa biểu đồ thứ ba nếu có
            self.canvas3.get_tk_widget().destroy()

        # Hiển thị lại biểu đồ với dữ liệu mới
        self.show_charts()


    def exit(self):
        self.root.destroy()

    def logout(self):
        self.root.destroy()
        os.system("python login1.py")

if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
