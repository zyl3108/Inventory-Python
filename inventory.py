from tkinter import *
from tkinter import ttk, messagebox
import pymysql.cursors

class InventoryManagement:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1250x700+300+140")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.purchased_products = []  # Lưu trữ sản phẩm đã mua

        # Frame báo cáo
        report_frame = Frame(self.root, bd=2, relief=RIDGE)
        report_frame.place(x=10, y=10, width=1230, height=680)

        title = Label(report_frame, text="Inventory Report", font=("goudy old style", 20), bg="#0f4d7d", fg="white")
        title.pack(side=TOP, fill=X)

        # Tìm kiếm
        search_frame = LabelFrame(report_frame, text="Search Inventory", font=("goudy old style", 12), bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=50, width=1200, height=80)

        cmb_search = ttk.Combobox(search_frame, textvariable=self.var_searchby, values=("Select", "Category", "Supplier", "Product"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmb_search.place(x=10, y=10, width=180)
        cmb_search.current(0)

        txt_search = Entry(search_frame, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow")
        txt_search.place(x=200, y=10)

        btn_search = Button(search_frame, text="Search", command=self.search_inventory, font=("goudy old style", 15), bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=410, y=10, width=150, height=30)

        # Khung hiển thị kết quả
        self.result_frame = Frame(report_frame, bd=3, relief=RIDGE)
        self.result_frame.place(x=10, y=140, width=1200, height=500)

        self.tree = ttk.Treeview(self.result_frame, columns=("Product", "Supplier", "Category", "Quantity In", "Quantity Out", "Current Quantity", "Action"), show="headings")
        self.tree.heading("Product", text="Product")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Quantity In", text="Quantity In")
        self.tree.heading("Quantity Out", text="Quantity Out")
        self.tree.heading("Current Quantity", text="Current Quantity")
        self.tree.heading("Action", text="Action")
        self.tree.pack(fill=BOTH, expand=True)

        # Nút Export Stock
        btn_export_stock = Button(report_frame, text="Export Stock", command=self.open_export_stock, font=("goudy old style", 15), bg="#ff5722", fg="white", cursor="hand2")
        btn_export_stock.place(x=10, y=650, width=200, height=30)

        self.show_inventory()  # Hiển thị tất cả hàng tồn kho khi khởi động

    def search_inventory(self):
        """Tìm kiếm kho theo các tiêu chí đã chọn."""
        search_by = self.var_searchby.get()
        search_text = self.var_searchtxt.get()

        if search_by == "Select" or not search_text:
            messagebox.showwarning("Warning", "Please select a search criteria and enter a search term.", parent=self.root)
            return

        query = ""
        if search_by == "Category":
            query = "SELECT * FROM inventory WHERE category LIKE %s"
        elif search_by == "Supplier":
            query = "SELECT * FROM inventory WHERE supplier LIKE %s"
        elif search_by == "Product":
            query = "SELECT * FROM inventory WHERE product_name LIKE %s"

        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            cur.execute(query, ('%' + search_text + '%',))
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ trong bảng
            if rows:
                for row in rows:
                    quantity_in = int(row['quantity_in']) if row['quantity_in'] else 0
                    quantity_out = int(row['quantity_out']) if row['quantity_out'] else 0
                    current_quantity = quantity_in - quantity_out
                    self.tree.insert('', END, values=(row['product_name'], row['supplier'], row['category'], quantity_in, quantity_out, current_quantity, "Accept"))
            else:
                messagebox.showinfo("Info", "No records found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()

    def open_export_stock(self):
        """Mở cửa sổ Export Stock."""
        export_window = Toplevel(self.root)
        export_window.geometry("1200x400+400+200")
        export_window.title("Export Stock")

        # Tạo bảng Export Stock trong cửa sổ mới
        export_frame = Frame(export_window, bd=2, relief=RIDGE)
        export_frame.place(x=10, y=10, width=1180, height=350)

        Label(export_frame, text="Export Stock", font=("goudy old style", 15), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        self.export_tree = ttk.Treeview(export_frame, columns=("Product", "Quantity", "User Name", "Status", "Time", "Action"), show="headings")
        self.export_tree.heading("Product", text="Product")
        self.export_tree.heading("Quantity", text="Quantity")
        self.export_tree.heading("User Name", text="User Name")
        self.export_tree.heading("Status", text="Status")
        self.export_tree.heading("Time", text="Time")  # Thêm cột 'Time'
        self.export_tree.heading("Action", text="Action")
        self.export_tree.pack(fill=BOTH, expand=True)

        # Hiển thị các sản phẩm cần xuất
        self.load_purchased_products()

    def load_purchased_products(self):
        """Lấy danh sách các sản phẩm đã mua từ bảng temp_sales và hiển thị trong bảng Export Stock."""
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            # Cập nhật truy vấn để lấy 'timestamp'
            cur.execute("SELECT product_name, quantity_sold, user_name, status, timestamp FROM temp_sales")
            rows = cur.fetchall()
            self.purchased_products = rows
            self.show_purchased_products()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()

    def show_purchased_products(self):
        """Hiển thị các sản phẩm đã mua trong bảng Export Stock."""
        self.export_tree.delete(*self.export_tree.get_children())  # Xóa dữ liệu cũ trong bảng

        for item in self.purchased_products:
            product_name = item['product_name']
            quantity = item['quantity_sold']
            user_name = item['user_name']  # Lấy tên người dùng
            status = item['status'] if item['status'] else "Pending"
            timestamp = item['timestamp']  # Lấy thời gian từ trường 'timestamp'

            self.export_tree.insert('', END, values=(product_name, quantity, user_name, status, timestamp, "Accept"))

        # Ràng buộc sự kiện "Accept"
        self.export_tree.bind("<ButtonRelease-1>", self.handle_accept_click)

    def handle_accept_click(self, event):
        """Xử lý sự kiện khi nhấn vào nút 'Accept'."""
        selected_item = self.export_tree.selection()
        if selected_item:
            item_values = self.export_tree.item(selected_item)["values"]
            product_name = item_values[0]
            quantity = item_values[1]
            status = item_values[3]

            if status == "Pending":
                self.accept_export(product_name, quantity)
            else:
                messagebox.showinfo("Info", f"Product '{product_name}' has already been accepted.", parent=self.root)

    def accept_export(self, product_name, quantity_sold):
        """Cập nhật quantity_out và current_quantity trong inventory, trạng thái 'Accepted' trong temp_sales."""
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            # Lấy thông tin từ bảng inventory
            cur.execute("SELECT quantity_in, quantity_out FROM inventory WHERE product_id = (SELECT pid FROM product WHERE name = %s)", (product_name,))
            inventory_data = cur.fetchone()

            if inventory_data:
                quantity_in = inventory_data['quantity_in'] if inventory_data['quantity_in'] else 0
                quantity_out = inventory_data['quantity_out'] if inventory_data['quantity_out'] else 0

                # Kiểm tra tồn kho
                if quantity_in < quantity_out + quantity_sold:
                    messagebox.showwarning("Warning", f"Insufficient stock for product '{product_name}'.", parent=self.root)
                    return

                # Cập nhật số lượng
                new_quantity_out = quantity_out + quantity_sold
                current_quantity = quantity_in - new_quantity_out

                # Cập nhật bảng inventory
                cur.execute("""
                    UPDATE inventory 
                    SET quantity_out = %s, current_quantity = %s 
                    WHERE product_id = (SELECT pid FROM product WHERE name = %s)
                """, (new_quantity_out, current_quantity, product_name))

                # Cập nhật trạng thái trong bảng temp_sales
                cur.execute("UPDATE temp_sales SET status = 'Accepted' WHERE product_name = %s", (product_name,))

                conn.commit()

                messagebox.showinfo("Success", f"Export accepted for product '{product_name}'.", parent=self.root)
                self.update_status_in_export_tree(product_name, "Accepted")

                # Tự động làm mới bảng inventory sau khi cập nhật
                self.show_inventory()
            else:
                messagebox.showerror("Error", f"Product '{product_name}' not found in inventory.", parent=self.root)
        except Exception as ex:
            conn.rollback()
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()


    def update_status_in_export_tree(self, product_name, new_status):
        """Cập nhật trạng thái của sản phẩm trong bảng Export Stock."""
        for row in self.export_tree.get_children():
            values = self.export_tree.item(row)["values"]
            if values[0] == product_name:
                values[3] = new_status  # Cập nhật cột 'Status'
                self.export_tree.item(row, values=values)
                break





    def show_inventory(self):
        """Hiển thị tất cả kho hàng với dữ liệu từ inventory."""
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            cur.execute("""SELECT product.name AS Product, supplier.name AS Supplier, category.name AS Category, 
                                    inventory.quantity_in AS Quantity_In, 
                                    IFNULL(inventory.quantity_out, 0) AS Quantity_Out, 
                                    IFNULL(inventory.current_quantity, inventory.quantity_in) AS Current_Quantity
                            FROM product 
                            JOIN supplier ON product.supplier = supplier.name 
                            JOIN category ON product.category = category.name 
                            JOIN inventory ON product.pid = inventory.product_id""")
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ trong TreeView
            if rows:
                for row in rows:
                    self.tree.insert('', END, values=(
                        row['Product'], 
                        row['Supplier'], 
                        row['Category'], 
                        row['Quantity_In'], 
                        row['Quantity_Out'], 
                        row['Current_Quantity'],
                        ""))  # Dữ liệu cập nhật từ cơ sở dữ liệu
            else:
                messagebox.showinfo("Info", "No records found!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            conn.close()







if __name__ == "__main__":
    root = Tk()
    inventory_obj = InventoryManagement(root)  # Truyền BillClass vào InventoryManagement
    root.mainloop()