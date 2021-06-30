# HOMEPAGE WINDOW
from tkinter import *
from PIL import Image, ImageTk
import replicate as r
import mysql.connector as my
from tkinter import messagebox
from tkinter import font


# -------------------Resize image based on frame size----------------#
def resize(event):
    new_width = event.width                       # change width
    new_height = event.height                     # change height
    # applying change on image
    img = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(img)
    background.config(image=photo)
    background.image = photo            # setting image as background


# -----------------Functions for respective window-------------------#
def books():        # books window
    import Books
    screen.destroy()
    Books.book(a)


def members():      # members window
    import Members
    screen.destroy()
    Members.members(a)


def fund():         # fund window
    import Funds
    screen.destroy()
    Funds.funds(a)


# ------------------------main window--------------------------------#
def main_page(b):     # homepage window
    global background
    global copy_of_image
    global screen
    global a

    a = b + 1
    screen = Tk()                      # creating window called screen
    screen.iconbitmap("images/main_icon.ico")
    screen.title("MENU")               # title for screen
    screen.state('zoomed')        # keeping screen zoomed when entered
    screen.resizable(0, 0)           # disabling changing screen size

    # setting background on whole screen
    image = Image.open("images"
                       "/bg 5.jpeg")
    copy_of_image = image.copy()
    bg = ImageTk.PhotoImage(image)
    background = Label(screen, image=bg)
    background.bind('<Configure>', resize)  # calling 'resize'
    background.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    background.image = bg
    r.menubar(screen, 'screen', "", a)              # setting menu bar

    # -----------------------images-----------------------------------
    image1 = ImageTk.PhotoImage(Image.open("images/books label"
                                           " image.png"))
    image2 = ImageTk.PhotoImage(Image.open("images/members label "
                                           "image.png"))
    image3 = ImageTk.PhotoImage(Image.open("images/funds label "
                                           "image.png"))

    # ---------------------label--------------------------------------
    label1 = Label(screen, image=image1, padx=50, pady=50, bg='black')
    label1.place(x=500, y=295, height=57, width=48)
    label2 = Label(screen, image=image2, padx=50, pady=50, bg='black')
    label2.place(x=500, y=355, height=57, width=48)
    label3 = Label(screen, image=image3, padx=50, pady=50, bg='black')
    label3.place(x=500, y=415, height=57, width=48)

    # -------------------buttons--------------------------------------
    book_button = Button(screen, text="BOOKS", font='bold',
                         command=books, width=30, height=2,
                         bg='black', fg='white',
                         activebackground='black')
    book_button.place(x=550, y=295, height=57, width=350)

    members_button = Button(screen, text="MEMBERS", font='bold',
                            command=members, width=30, height=2,
                            bg='black', fg='white',
                            activebackground='black')
    members_button.place(x=550, y=355, height=57, width=350)

    funds = Button(screen, text="FUNDS", font='bold',
                   command=fund, width=30, height=2, bg='black',
                   fg='white', activebackground='black')
    funds.place(x=550, y=415, height=57, width=350)

    #-----------------------------------------------------------------
    # defining the note button
    def note():                                        # note for user
        note_frame = LabelFrame(screen, text="Notes", bg='white')
        note_frame.place(relx=0.03, rely=0.05,
                         relwidth=0.20, relheight=0.85)

        note_listbox = Listbox(note_frame, bg="black", fg='white',
                               font=(font.Font(size=25)), height=20)
        note_listbox.place(relx=0.01, rely=0.04, relwidth=0.92,
                           relheight=0.95)     # list of notes created

        scroll1 = Scrollbar(note_frame, orient=VERTICAL,
                            command=note_listbox.yview)
        scroll1.place(relx=0.91, rely=0.04, relheight=0.95)
        note_listbox.configure(yscrollcommand=scroll1.set)

        close_button = Button(note_frame, text='Close', bg='black',
                              command=lambda: note_frame.destroy(),
                              activebackground='black', fg='white')
        close_button.place(relx=0.7, rely=0.0)

        my_con = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
        cur = my_con.cursor()
        query = 'select title from note'
        cur.execute(query)
        data = cur.fetchall()
        n = len(data)
        my_con.close()

        #-------------------------------------------------------------
        # defining new button function
        def new():                              # create a new note
            create_window = Toplevel(screen)
            create_window.title("Create")
            create_window.iconbitmap("images/main_icon.ico")
            create_window.config(bg='white')
            create_window.geometry("450x150+525+300")

            title_label = Label(create_window, text="Enter the title")
            title_label.place(relx=0.25, rely=0.25, relwidth=0.47)

            title_entry = Entry(create_window)
            title_entry.place(relx=0.25, rely=0.45, relwidth=0.47)

            title_entry.focus()

            #---------------------------------------------------------
            # defining the create the function
            def create():
                title = title_entry.get()
                if title == '':            # not allowing empty title
                    messagebox.showerror('ERROR',
                                         'Please enter a title')
                else:
                    my_con1 = my.connect(host='sql11.freemysq'
                                              'lhosting.net',
                                         user='sql11422143',
                                         passwd='pq3EcPFj4e',
                                         db='sql11422143')
                    cur1 = my_con1.cursor()
                    query1 = 'select title from note'
                    cur1.execute(query1)
                    data1 = cur1.fetchall()
                    for head in data1:
                        if title == head[0]:  # noduplicate title
                            messagebox.showerror("Duplicate",
                                                 "This title exists")
                            create_window.destroy()
                            break
                    else:                         # creating new note
                        query1 = 'insert into note(title)' \
                                 ' values("%s")' % (title,)
                        cur1.execute(query1)
                        my_con1.commit()
                        note_listbox.insert(n + 1, title)  # updating
                        create_window.destroy()
                    my_con1.close()

            title_save_button = Button(create_window, text="Create",
                                       command=create)
            title_save_button.place(relx=0.45, rely=0.65)
            #---------------------------------------------------------
        create_page_button = Button(note_frame, text="Create Page",
                                    command=new, bg='black',
                                    fg='white',
                                    activebackground='black')
        create_page_button.place(relx=0.03, rely=0.0)
        #-------------------------------------------------------------

        #-------------------------------------------------------------
        # defining page button
        def page(event):                     # opening nd editing note
            page_screen = Toplevel(screen)
            page_screen.iconbitmap("images/main_icon.ico")
            index = note_listbox.curselection()
            select = note_listbox.get(index)
            page_screen.title(select)
            page_screen.config(bg='white')
            page_screen.geometry("330x150")
            page_screen.resizable(0, 0)

            text = Text(page_screen, height=6, width=40)
            text.place(relx=0.0, rely=0.0, relwidth=1)

            text.focus()

            my_con2 = my.connect(host='sql11.freemysqlhosting.net',
                                 user='sql11422143',
                                  passwd='pq3EcPFj4e',
                                 db='sql11422143')
            cur2 = my_con2.cursor()
            query2 = 'select text from note where title= "%s" ' % \
                     (select,)         # deriving the saved text
            cur2.execute(query2)
            data2 = cur2.fetchall()

            if data2 != [(None,)]:
                text.insert("1.0", data2[0][0])
            my_con2.close()

            #---------------------------------------------------------
            # defining the count function
            def count(event1):
                x = len(text.get('1.0', END))
                if x >= 250:
                    messagebox.showerror('!',
                                         'Maximum word limit reached')
            #---------------------------------------------------------
            text.bind('<Key>', count)  # limit the number of character

            #---------------------------------------------------------
            # defining the save function
            def save():
                if len(text.get('1.0', END)) > 250:
                    messagebox.showerror("Error",
                                         "Excess character"
                                         "(Greater than 250)")
                else:
                    insert_text = text.get('1.0', END)
                    text_list = list(insert_text)
                    insert_text = ""
                    for strings in text_list:   # changing all " to '
                        if strings == '"':
                            post = text_list.index(strings)
                            text_list[post] = " '"
                            strings = " '"
                        insert_text += strings

                    my_con3 = my.connect(host='sql11.freemysql'
                                              'hosting.net',
                                          user='sql11422143',
                                           passwd='pq3EcPFj4e',
                                         db='sql11422143')
                    cur3 = my_con3.cursor()
                    # saving the text
                    query3 = 'update note set text="%s" where' \
                             ' title= "%s" ' % (insert_text, select)
                    cur3.execute(query3)
                    my_con3.commit()
                    my_con3.close()
                    page_screen.destroy()
            #---------------------------------------------------------
            save_button = Button(page_screen, text="Save",
                                 command=save, bg='black',
                                 activebackground='black', fg='white')
            save_button.place(relx=0.1, rely=0.78)

            #---------------------------------------------------------
            # defining delete function
            def delete():
                if messagebox.askyesno('?', 'Do You want to delete '
                                            'the note?') == TRUE:
                    my_con4 = my.connect(host='sql11.freemysql'
                                              'hosting.net',
                                          user='sql11422143',
                                           passwd='pq3EcPFj4e',
                                         db='sql11422143')
                    cur4 = my_con4.cursor()
                    query4 = 'delete from note where title= "%s" '\
                             % (select,)   # deleting the note
                    cur4.execute(query4)
                    my_con4.commit()
                    my_con4.close()
                    page_screen.destroy()
                    note_listbox.delete(index, index)
                else:
                    return
            #---------------------------------------------------------
            cancel_button = Button(page_screen, text='Delete',
                                   command=delete, bg='black',
                                   activebackground='black',
                                   fg='white')
            cancel_button.place(relx=0.7, rely=0.78)
        #-------------------------------------------------------------
        # calling page function on double clicking
        note_listbox.bind("<Double-1>", page)

        if n == 0:
            return
        else:
            for i in range(n):
                note_listbox.insert(i, data[i][0])   # insert list
    #-----------------------------------------------------------------
    note_button = Button(screen, text="Notes", command=note, width=15,
                         height=2, bg='black', fg='white',
                         activebackground='black')
    note_button.place(relx=0.03, rely=0.05)

    # message when return running late
    my_con5 = my.connect(host='sql11.freemysqlhosting.net',
                             user='sql11422143',
                             passwd='pq3EcPFj4e', db='sql11422143')
    cur5 = my_con5.cursor()
    cur5.execute('select no_of_days_left from issue_books where '
                 'no_of_days_left<0')
    data5 = cur5.fetchall()
    if len(data5) > 0:
        if a == 1:
            messagebox.showwarning('Notification', "'%s' book's "
                                                   "return"
                                                   " running late!" %
                                   (len(data5),))
        else:
            info = ImageTk.PhotoImage(Image.open("images/"
                                                 "info.png"))
            label4 = Label(bg='white')
            label4.place(relx=0.015, rely=0)

            def ent(event):
                label4.config(text='"%s" book(s) return running late'
                                   % (len(data5, )), bg='gray')

            def ext(event):
                label4.config(text='', bg='white')

            label5 = Label(bg='white', image=info)
            label5.place(relx=0.00, rely=0.00)
            label5.bind('<Enter>', ent)
            label5.bind('<Leave>', ext)

    screen.mainloop()
