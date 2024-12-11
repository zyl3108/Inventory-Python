from tkinter import *
import db
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import pymysql.cursors
import os

class Login_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1250x700+300+140")
        self.root.title("Login System")
        self.root.config(bg="#fafafa")
    #---------images--------
        self.phone_image = ImageTk.PhotoImage(file="images/inventory.png")
        self.lbl_Phone_image = Label(self.root,image=self.phone_image,bd=0).place(x=100,y=150)



    #-------Login Frame
        self.employee_id = StringVar()
        self.password = StringVar()

        login_Frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_Frame.place(x=650,y=90,width=350,height=460)

        # Add title text at the top
        self.title_lbl = Label(self.root, text="Inventory Management System", font=("Times New Roman", 40, "bold"), bg="#fafafa", fg="red")
        self.title_lbl.place(x=0, y=0, relwidth=1, height=70)


        title = Label(login_Frame,text="Login System",font=("Elephant",30,"bold"),bg="white").place(x=20,y=30)

        lbl_user = Label(login_Frame,text="User ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        
        txt_employee_id = Entry(login_Frame,textvariable=self.employee_id,font=("times new roman",15),bg="lightgray",fg="black").place(x=50,y=150,width=250)

        lbl_pass = Label(login_Frame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass = Entry(login_Frame,textvariable=self.password,show="*",font=("times mew roman",15),bg="lightgray",fg="black").place(x=50,y=250,width=250)

        btn_login=Button(login_Frame,text="Login",command=self.login,font=("Arial Rounded MT Bold",15,"bold"),bg="#286ede",fg="white")
        btn_login.place(x=50,y=300,width=250)

        hr = Label(login_Frame,bg="lightgray").place(x=50,y=370,width=250,height=2)
        or_ = Label(login_Frame,text="OR",bg="white",fg="lightgray",font=("times new roman",15,"bold"))

        btn_forget = Button(login_Frame,text="Forget Password?",command=self.forget_window,font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=50,y=400,width=250)

        #-------------Frame2-------------
        register_frame = Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        lbl_reg = Label(register_frame,text="Dont't have an account ?",font=("times new roman",13),bg="white").place(x=40,y=20)
        btn_signup = Button(register_frame,text="Sign Up",command=self.signup_window,font=("times new roman",13,"bold"),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=230,y=15)

        #----------Animation Images------------
        # self.im1 = ImageTk.PhotoImage(file="images/login1.png")
        # self.im2 = ImageTk.PhotoImage(file="images/login2.png")
        # self.im3 = ImageTk.PhotoImage(file="images/login3.jpg")

        # self.lbl_change_image = Label(self.root,bg="white")
        # self.lbl_change_image.place(x=400,y=140,width=200,height=350)

        # self.animate()

    #-----------------------All Functions--------------



    # def animate(self):
    #     self.im = self.im1
    #     self.im1 = self.im2
    #     self.im2 = self.im3
    #     self.im3 = self.im
    #     self.lbl_change_image.config(image=self.im)
    #     self.lbl_change_image.after(2000,self.animate)

    def login(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT utype FROM employee WHERE eid=%s AND pass=%s", (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror("Error", "Invalid USERNAME/PASSWORD", parent=self.root)
                else:
                    utype = user['utype']
                    if utype == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            cur.close()
            conn.close()

    def forget_window(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()

        try:
            if self.employee_id.get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=self.root)
            else:
                cur.execute("SELECT pass FROM employee WHERE eid=%s", (self.employee_id.get(),))
                user = cur.fetchone()

                if user is None:
                    messagebox.showerror("Error", "Invalid Employee ID, try again", parent=self.root)
                else:
                    # Forget Window
                    self.current_password = user['pass']
                    self.var_otp = StringVar()  # Define the variable here
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()

                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title("RESET PASSWORD")
                    self.forget_win.geometry("400x350+500+100")
                    self.forget_win.focus_force()

                    title = Label(self.forget_win, text="Reset Password", font=("goudy old style", 15, "bold"), bg="#3f51b5", fg="white")
                    title.pack(side=TOP, fill=X)

                    lbl_current = Label(self.forget_win, text="Current Password", font=("times new roman", 15))
                    lbl_current.place(x=20, y=60)

                    txt_current = Entry(self.forget_win, show="*", font=("times new roman", 15), textvariable=self.var_otp, bg="lightyellow")
                    txt_current.place(x=20, y=100, width=250, height=30)

                    lbl_new_pass = Label(self.forget_win, text="New Password", font=("times new roman", 15))
                    lbl_new_pass.place(x=20, y=160)

                    txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, show="*", font=("times new roman", 15), bg="lightyellow")
                    txt_new_pass.place(x=20, y=190, width=250, height=30)

                    lbl_c_pass = Label(self.forget_win, text="Confirm Password", font=("times new roman", 15))
                    lbl_c_pass.place(x=20, y=225)

                    txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, show="*", font=("times new roman", 15), bg="lightyellow")
                    txt_c_pass.place(x=20, y=255, width=250, height=30)

                    self.btn_update = Button(self.forget_win, text="UPDATE", font=("times new roman", 15), bg="lightblue", command=self.update_password)
                    self.btn_update.place(x=150, y=300, width=100, height=30)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            cur.close()
            conn.close()

    def update_password(self):
        current_password = self.var_otp.get()
        new_password = self.var_new_pass.get()
        confirm_password = self.var_conf_pass.get()

        if current_password != self.current_password:
            messagebox.showerror("Error", "Current password does not match", parent=self.forget_win)
        elif new_password != confirm_password:
            messagebox.showerror("Error", "New passwords do not match", parent=self.forget_win)
        else:
            conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
            cur = conn.cursor()

            try:
                cur.execute("UPDATE employee SET pass=%s WHERE eid=%s", (new_password, self.employee_id.get()))
                conn.commit()
                messagebox.showinfo("Success", "Password updated successfully", parent=self.forget_win)
                self.forget_win.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Error updating password: {str(ex)}", parent=self.forget_win)
            finally:
                cur.close()
                conn.close()

    def signup_window(self):
        self.signup_win = Toplevel(self.root)
        self.signup_win.title("Sign Up")
        self.signup_win.geometry("400x550+500+100")  # Increase height to accommodate the new field
        self.signup_win.focus_force()

        # Variables
        self.var_name = StringVar()  # Variable for name
        self.var_email = StringVar()  # New variable for email
        self.var_eid = StringVar()
        self.var_pass = StringVar()
        self.var_utype = StringVar()

        title = Label(self.signup_win, text="Sign Up", font=("goudy old style", 20, "bold"), bg="#3f51b5", fg="white")
        title.pack(side=TOP, fill=X)

        lbl_eid = Label(self.signup_win, text="Employee ID", font=("times new roman", 15))
        lbl_eid.place(x=20, y=60)
        txt_eid = Entry(self.signup_win, textvariable=self.var_eid, font=("times new roman", 15), bg="lightyellow")
        txt_eid.place(x=20, y=100, width=250, height=30)

        lbl_name = Label(self.signup_win, text="Name", font=("times new roman", 15))
        lbl_name.place(x=20, y=140)
        txt_name = Entry(self.signup_win, textvariable=self.var_name, font=("times new roman", 15), bg="lightyellow")
        txt_name.place(x=20, y=180, width=250, height=30)

        lbl_email = Label(self.signup_win, text="Email", font=("times new roman", 15))  # Label for email
        lbl_email.place(x=20, y=220)
        txt_email = Entry(self.signup_win, textvariable=self.var_email, font=("times new roman", 15), bg="lightyellow")  # Entry for email
        txt_email.place(x=20, y=260, width=250, height=30)


        lbl_pass = Label(self.signup_win, text="Password", font=("times new roman", 15))
        lbl_pass.place(x=20, y=300)
        txt_pass = Entry(self.signup_win, textvariable=self.var_pass, show="*", font=("times new roman", 15), bg="lightyellow")
        txt_pass.place(x=20, y=340, width=250, height=30)

        lbl_utype = Label(self.signup_win, text="User Type", font=("times new roman", 15))
        lbl_utype.place(x=20, y=380)
        combo_utype = ttk.Combobox(self.signup_win, textvariable=self.var_utype, font=("times new roman", 15), state='readonly')
        combo_utype['values'] = ("Admin", "User")
        combo_utype.place(x=20, y=420, width=250)
        combo_utype.current(0)

        btn_signup = Button(self.signup_win, text="Sign Up", font=("times new roman", 15), bg="lightblue", command=self.signup)
        btn_signup.place(x=150, y=490, width=100, height=30)

    def signup(self):
        conn = pymysql.connect(host="127.0.0.1", user="root", password="123@dat", db="ims", cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()

        try:
            if self.var_name.get() == "" or self.var_email.get() == "" or self.var_eid.get() == "" or self.var_pass.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.signup_win)
                return
            
            # Check if the employee ID already exists
            cur.execute("SELECT * FROM employee WHERE eid=%s", (self.var_eid.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Employee ID already exists", parent=self.signup_win)
                return

            # Insert new user into the database including the name and email
            cur.execute("INSERT INTO employee (name, email, eid, pass, utype) VALUES (%s, %s, %s, %s, %s)", 
                        (self.var_name.get(), self.var_email.get(), self.var_eid.get(), self.var_pass.get(), self.var_utype.get()))
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully", parent=self.signup_win)
            self.signup_win.destroy()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.signup_win)
        finally:
            cur.close()
            conn.close()


    


    



if __name__ ==  "__main__":
    root =Tk()
    obj = Login_System(root)
    root.mainloop()