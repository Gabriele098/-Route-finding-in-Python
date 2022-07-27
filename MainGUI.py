import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import datetime
import re
from ListStops import *
import journey_calculator

# initialize the 3 variables
station_from = ""
station_to = ""
time = 0


class MainWindow:

    def __init__(self, master):
        self.master = master

        # get screen width and height
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        # calculate position x and y coordinates
        x = (self.screen_width / 2) - (950 / 2)
        y = (self.screen_height / 2) - (750 / 2) - 30
        self.master.geometry('%dx%d+%d+%d' % (950, 750, x, y))

        self.master.title("Journey Planner")
        # self.master.configure()
        self.master.resizable(width=False, height=False)

        # set a Background
        self.load1 = Image.open("ImagesUnderground/BackGround.jpg")
        self.render1 = ImageTk.PhotoImage(self.load1)
        self.main_label1 = tk.Label(image=self.render1)
        self.main_label1.place(relx=0.5, rely=0.50, anchor="center")

        # Buttons underground
        self.bakerloo_button = tk.Button(text="Bakerloo", font=("Corbel", "12", "bold"), height="1", width=23,
                                         background="#7E3817", fg="#ffffff", border=0, command=self.route_bakerloo)
        self.bakerloo_button.place(relx=0.02, rely=0.42)
        self.central_button = tk.Button(text="Central", font=("Corbel", "12", "bold"), height="1", width=23,
                                        background="#E42217", fg="#ffffff", border=0, command=self.route_central)
        self.central_button.place(relx=0.26, rely=0.42)
        self.circle_button = tk.Button(text="Circle", font=("Corbel", "12", "bold"), height="1", width=11,
                                       background="#FFD801", border=0, command=self.route_circle)
        self.circle_button.place(relx=0.50, rely=0.54)
        self.district_button = tk.Button(text="District", font=("Corbel", "12", "bold"), height="1", width=23,
                                         background="#347C2C", fg="#ffffff", border=0, command=self.route_district)
        self.district_button.place(relx=0.74, rely=0.42)
        self.ham_city_button = tk.Button(text="Hammersmith & City", font=("Corbel", "12", "bold"), height="1", width=23,
                                         background="#E7A1B0", border=0, command=self.route_ham_city)
        self.ham_city_button.place(relx=0.02, rely=0.48)
        self.jubilee_button = tk.Button(text="Jubilee", font=("Corbel", "12", "bold"), height="1", width=23,
                                        background="#848482", fg="#ffffff", border=0, command=self.route_jubilee)
        self.jubilee_button.place(relx=0.26, rely=0.48)
        self.metropolitan_button = tk.Button(text="Metropolitan", font=("Corbel", "12", "bold"), height="1", width=23,
                                             background="#7D0552", fg="#ffffff", border=0,
                                             command=self.route_metropolitan)
        self.metropolitan_button.place(relx=0.50, rely=0.48)
        self.northern_button = tk.Button(text="Northern", font=("Corbel", "12", "bold"), height="1", width=23,
                                         background="#000000", fg="#ffffff", border=0, command=self.route_northern)
        self.northern_button.place(relx=0.74, rely=0.48)
        self.piccadilly_button = tk.Button(text="Piccadilly", font=("Corbel", "12", "bold"), height="1", width=23,
                                           background="#0000A0", fg="#ffffff", border=0, command=self.route_piccadilly)
        self.piccadilly_button.place(relx=0.02, rely=0.54)
        self.victoria_button = tk.Button(text="Victoria", font=("Corbel", "12", "bold"), height="1", width=23,
                                         background="#38ACEC", border=0, command=self.route_victoria)
        self.victoria_button.place(relx=0.26, rely=0.54)
        self.waterloo_city_button = tk.Button(text="Waterloo & City", font=("Corbel", "12", "bold"), height="1",
                                              width=23,
                                              background="#ADDFFF", border=0, command=self.route_waterloo_city)
        self.waterloo_city_button.place(relx=0.50, rely=0.42)
        self.DLR_button = tk.Button(text="DLR", font=("Corbel", "12", "bold"), height="1",
                                    width=11,
                                    background="#00CED1", border=0, command=self.route_DLR)
        self.DLR_button.place(relx=0.74, rely=0.54)

        self.TFL_button = tk.Button(text="TFL", font=("Corbel", "12", "bold"), height="1",
                                    width=10,
                                    background="#0000FF", fg="#ffffff", border=0, command=self.route_TFL)
        self.TFL_button.place(relx=0.863, rely=0.54)

        self.Overground_button = tk.Button(text="Overground", font=("Corbel", "12", "bold"), height="1",
                                           width=10,
                                           background="#ec7b12", fg="#000000", border=0, command=self.route_Overground)
        self.Overground_button.place(relx=0.622, rely=0.54)

        # Label for the information below
        self.label = tk.Label(root,
                              text="Click the specific underground line" + "\n" + " to get its information",
                              font=("Helvetica", "19", "bold"), bg="#488AC7", fg="#000000", border=0,
                              width=54)
        self.label.place(relx=0.07, rely=0.74)

        # Map Button
        self.map_button = tk.Button(text="MAP", font=("Corbel", "14", "bold"), height=1,
                                    width=8,
                                    background="#4c82be", fg="#ffffff", border=0, command=self.map_window)
        self.map_button.place(relx=0.472, rely=0.2956)

        # Search Button
        self.search_button = tk.Button(text="SEARCH", font=("Corbel", "14", "bold"), height=1,
                                       width=8,
                                       background="#4c82be", fg="#ffffff", border=0, command=self.search_journey)
        self.search_button.place(relx=0.8041, rely=0.2956)

        # Quit Button
        self.quit_button = tk.Button(text="QUIT", font=("Corbel", "14", "bold"), height=1,
                                     width=19,
                                     background="#4c82be", fg="#ffffff", border=1, command=self.quit)
        self.quit_button.place(relx=0.774, rely=0.950)
        # Help Button
        self.help_button = tk.Button(text="i", font=("Times New Roman", "16", "italic"), height=1,
                                     width=3,
                                     background="#4c82be", fg="#ffffff", border=1, command=self.help)
        self.help_button.place(relx=0.005, rely=0.005)

        # Select Time
        self.now = datetime.datetime.now()
        # Set the time of the journey (hours, minutes)
        self.hour_str = tk.StringVar(root, self.now.hour)
        self.hour = tk.Spinbox(root, from_=0, to=23, font=("Helvetica", "18"), bg="#4c82be", fg="#233247", border=0,
                               wrap=True, textvariable=self.hour_str, width=3)
        self.label = tk.Label(root, text=":", font=("Helvetica", "16", "bold"), bg="#4c82be", fg="#233247", border=0,
                              width=1)
        self.label.place(relx=0.555, rely=0.206)
        self.min_str = tk.StringVar(root, self.now.minute)
        self.min = tk.Spinbox(root, from_=0, to=59, font=("Helvetica", "18"), bg="#4c82be", fg="#233247", border=0,
                              wrap=True, textvariable=self.min_str, width=3)
        self.hour.place(relx=0.49, rely=0.205)
        self.min.place(relx=0.5762, rely=0.205)

        def matches(fieldValue, acListEntry):
            pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
            return re.match(pattern, acListEntry)

        # ListBox From and To
        self.station_from_text = AutocompleteEntry(all_stations, root, listboxLength=6, width=32,
                                                   matchesFunction=matches)
        self.station_from_text.place(relx=0.43, rely=0.16)

        self.station_to_text = AutocompleteEntry(all_stations, root, listboxLength=6, width=32, matchesFunction=matches)
        self.station_to_text.place(relx=0.74, rely=0.16)

    def search_journey(self):
        # globals variables that takes the from station and to station
        global station_from, station_to, time
        time = self.hour.get()
        station_from = self.station_from_text.get()
        station_to = self.station_to_text.get()
        # Check if the station exist and check the correct time to travel
        if station_from in all_stations and station_to in all_stations:
            if 5 <= int(time) > 0:
                self.list = root.place_slaves()
                for l in self.list:
                    l.destroy()
                # new window
                self.new_window = SecondWindow(self.master)
            else:
                messagebox.showerror("Error Message", "There is no train service between midnight and 5:00 am")
        else:
            messagebox.showerror("Error Message", "Insert valid information!")

    # All the functions that shows the images of the Lines
    def route_bakerloo(self):
        self.load = Image.open("ImagesUnderground/Bakerloo_Line.png")  # 968x262
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=-0.001, rely=0.60)

    def route_central(self):
        self.load = Image.open("ImagesUnderground/Central_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=-0.001, rely=0.60)

    def route_circle(self):
        self.load = Image.open("ImagesUnderground/Circle_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_district(self):
        self.load = Image.open("ImagesUnderground/District_Line .png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_ham_city(self):
        self.load = Image.open("ImagesUnderground/Hammersmith_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_jubilee(self):
        self.load = Image.open("ImagesUnderground/Jubilee_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=-0.001, rely=0.60)

    def route_metropolitan(self):
        self.load = Image.open("ImagesUnderground/Met_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_northern(self):
        self.load = Image.open("ImagesUnderground/Northern_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=-0.006, rely=0.60)

    def route_piccadilly(self):
        self.load = Image.open("ImagesUnderground/Piccadilly_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_victoria(self):
        self.load = Image.open("ImagesUnderground/Victoria_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_waterloo_city(self):
        self.load = Image.open("ImagesUnderground/Waterloo_Line.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_DLR(self):
        self.load = Image.open("ImagesUnderground/DLR.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_TFL(self):
        self.load = Image.open("ImagesUnderground/TFL RAIL.png")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0.60)

    def route_Overground(self):
        # delete everything inside the window and show the image of the overground
        self.list = root.place_slaves()
        for l in self.list:
            l.destroy()

        self.load = Image.open("ImagesUnderground/Overground.jpg")
        self.render = ImageTk.PhotoImage(self.load)
        self.main_label3 = tk.Label(image=self.render, border=0)
        self.main_label3.place(relx=0, rely=0)

        #Back Button
        self.back_button = tk.Button(text="Back", font=("Corbel", "14", "bold"), height=1,
                                     width=19,
                                     background="#4c82be", fg="#ffffff", border=1, command=self.back_to_main_button)
        self.back_button.place(relx=0.774, rely=0.950)

    def help(self):
        messagebox.showinfo("Info", "- The trains operate from 05:00 until midnight each day.\n\n"
                                    "- The trains run every 5 minutes with a 1 minute\n   stop at each station.\n\n"
                                    "- Bakerloo line travels at twice the original speed\n   from 9am-4pm and from "
                                    "7pm-midnight.")

    def back_to_main_button(self):
        self.list = root.place_slaves()
        for l in self.list:
            l.destroy()

        # next window
        self.map_window = MainWindow(root)


    def quit(self):
        self.master.destroy()

    # Function for the Map button that calls the Map class
    def map_window(self):
        self.list = root.place_slaves()
        for l in self.list:
            l.destroy()

        # next window
        self.map_window = Map(root)


# Second interface window
class SecondWindow:
    def __init__(self, master):
        self.master = master

        # set a Background
        self.load1 = Image.open("ImagesUnderground/BackGround2.png")
        self.render1 = ImageTk.PhotoImage(self.load1)
        self.main_label1 = tk.Label(image=self.render1)
        self.main_label1.place(relx=0.5, rely=0.50, anchor="center")
        # make the 2 main variables global
        global station_from, station_to, time
        journey = journey_calculator.Journey(station_from, station_to, int(time))
        data, summary, change = journey.calculate_journey()

        self.style = ttk.Style(root)
        # set ttk theme to "clam" which support the fieldbackground option
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#000000",
                             fieldbackground="#ffffff", foreground="#000000", border=0)
        # MAIN Table create
        self.table1 = ttk.Treeview(root, style="Treeview", columns=(1, 2, 3, 4), height=27, show="headings")
        self.table1.place(relx=0.688, rely=0.507, anchor="center")
        self.style.configure("Treeview", highlightthickness=2, bd=0, background='#E8E8E8', font=("Helvetica", 12))
        # head font
        self.style.configure("Treeview.Heading", background='#E8E8E8', font=('Calibri', 14, 'bold'))

        # Table column
        self.table1.heading(1, text="Line")
        self.table1.heading(2, text="Station")
        self.table1.heading(3, text="Time to next")
        self.table1.heading(4, text="Total time")
        # Table column size
        self.table1.column(1, width=130)
        self.table1.column(2, width=180)
        self.table1.column(3, width=110)
        self.table1.column(4, width=89)

        # Fill the table
        for val in data:
            self.table1.insert('', 'end', values=(val[0], val[1], val[2], val[3]))

        # Back Button
        self.quit_button = tk.Button(text="Back", font=("Corbel", "14", "bold"), height=1,
                                     width=19,
                                     background="#4c82be", fg="#ffffff", border=1, command=self.back_second)
        self.quit_button.place(relx=0, rely=0.950)

        # Summary
        self.table2 = ttk.Treeview(root, style="Treeview", columns=(1, 2), height=13, show="headings")
        self.table2.place(relx=0.20, rely=0.70, anchor="center")

        # Table column
        self.table2.heading(1, text="---")
        self.table2.heading(2, text="---")

        # Table column size
        self.table2.column(1, width=165)
        self.table2.column(2, width=165)

        # Fill the table2
        for val in summary:
            self.table2.insert('', 'end', values=(val[0], val[1]))

        for val in change:
            self.table2.insert('', 'end', values=(val[0], val[1]))

    # Back to main windows
    def back_second(self):
        self.list = root.place_slaves()
        for l in self.list:
            l.destroy()

        # next window
        self.main_window = MainWindow(root)


class AutoScrollbar(ttk.Scrollbar):
    ''' A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager '''

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')


class Map(ttk.Frame):

    def __init__(self, mainframe):
        '''
        Initialize the main Frame
        '''
        ttk.Frame.__init__(self, master=mainframe)
        self.master.title('Zoom with mouse wheel')
        # Vertical and horizontal scrollbars for canvas
        vbar = AutoScrollbar(self.master, orient='vertical')
        hbar = AutoScrollbar(self.master, orient='horizontal')
        vbar.grid(row=0, column=1, sticky='ns')
        hbar.grid(row=1, column=0, sticky='we')
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.show_image)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>', self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>', self.wheel)  # only with Linux, wheel scroll up
        self.image = Image.open("ImagesUnderground/standard-tube-map.jpg")  # open image
        self.width, self.height = self.image.size
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3  # zoom magnitude
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle(0, 0, self.width, self.height, width=0)
        # Plot some optional random rectangles for the test purposes
        minsize, maxsize, number = 5, 20, 10
        for n in range(number):
            x0 = random.randint(0, self.width - maxsize)
            y0 = random.randint(0, self.height - maxsize)
            x1 = x0 + random.randint(minsize, maxsize)
            y1 = y0 + random.randint(minsize, maxsize)
            color = ('red', 'orange', 'yellow', 'green', 'blue')[random.randint(0, 4)]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, activefill='black')
        self.show_image()

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.show_image()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            pass  # Ok! Inside the image
        else:
            return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()

    def show_image(self, event=None):
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)  # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

            # Back Button
            self.back_button = tk.Button(text="BACK", font=("Corbel", "14", "bold"), height=1,
                                         width=19,
                                         background="#000000", fg="#ffffff", border=0, command=self.back_to_main)
            self.back_button.place(relx=0.756, rely=0.929)

    def back_to_main(self):
        self.list = root.grid_slaves()
        for l in self.list:
            l.destroy()

        # next window
        self.main_window = MainWindow(root)


class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches

        Entry.__init__(self, *args, **kwargs)
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        return [w for w in self.lista if self.matchesFunction(self.var.get(), w)]


if __name__ == '__main__':
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
