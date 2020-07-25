import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import widgets as w
from .images import ctracker_32
from .images import ctracker_64
from tkinter.simpledialog import Dialog


class MainMenu(tk.Menu):
    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label='New Record', command=callbacks['new_record'])
        file_menu.add_separator()
        file_menu.add_command(label='Save in CSV', command=callbacks['file->savein'])
        file_menu.add_command(label='Save', command=callbacks['file->save'])
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=callbacks['file->quit'])
        self.add_cascade(label='File', menu=file_menu)

        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(label='Autofill Date', variable=settings['autofill date'])

        font_size_menu = tk.Menu(self, tearoff=False)
        for size in range(6, 17, 1):
            font_size_menu.add_radiobutton(
                label=size, value=size,
                variable=settings['font size']
            )
        options_menu.add_cascade(label='Font size', menu=font_size_menu)

        style = ttk.Style()
        themes_menu = tk.Menu(self, tearoff=False)
        for theme in style.theme_names():
            themes_menu.add_radiobutton(
                label=theme, value=theme,
                variable=settings['theme'].trace('w', self.on_theme_change)
            )
        options_menu.add_cascade(label='Theme', menu=themes_menu)

        self.add_cascade(label='Options', menu=options_menu)

        view_menu = tk.Menu(self, tearoff=False)
        view_menu.add_command(label='Criminal List', command=callbacks['show_recordlist'])
        view_menu.add_command(label='New Record', command=callbacks['new_record'])
        self.add_cascade(label='View', menu=view_menu)

        search_menu = tk.Menu(self, tearoff=False)
        search_menu.add_command(label='Search Options...', command=callbacks['search'])
        self.add_cascade(label='Search', menu=search_menu)
        
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About...', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def show_about(self):
        about_message = 'CRIMINAL TRACKER'
        about_detail = ('by Halima Abati \nFor assistance please read the docs \nor contact the developer. '
                        '\n\n\n\t\tpowered by Kurious Geek')
        messagebox.showinfo(title='About', message=about_message, detail=about_detail)
        
    def on_theme_change(self, *args):
        message = 'Theme change requires restart'
        detail = ('Changing theme requires application restart'
                  'Your work progrss might be lost'
                  'Do you want to continue?')
        messagebox.showwarning(title='Warning', message=message, detail=detail)
        
class DataRecordForm(tk.Frame):
    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.current_record = None

        style = ttk.Style()
        style.configure('BackgroundCol.TLabel', background='#008ae6', foreground='white')
        style.configure('BackgroundCol.TCheckbutton', background='#008ae6', foreground='white')
        
        #-- canvas --#
        self.canvas = tk.Canvas(self, width=985, height=600, highlightthickness=0, bg='#008ae6')
        yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        xscrollbar = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.scrollable_frame.config(bg='#008ae6')

        self.canvas.grid(row=0, column=0, sticky='NSEW')
        yscrollbar.grid(row=0, column=1, sticky='NS')
        xscrollbar.grid(row=1, column=0, sticky='EW') 

        self.inputs = {}

        self.logo = tk.PhotoImage(file=ctracker_64)
        self.logo_label=tk.Label(self.scrollable_frame, image=self.logo, highlightthickness=0, borderwidth=0)
        self.logo_label.grid(row=0, sticky='E')

        self.record_label = ttk.Label(self.scrollable_frame, style='BackgroundCol.TLabel')
        self.record_label.grid(row=1, sticky='E')
        
        #-- personal information --#
        
        personal_info = tk.LabelFrame(self.scrollable_frame, text = 'PERSONAL INFORMATION', bg='#008ae6', fg='white')
        personal_info.grid(row=2, column=0, padx=5)

        self.inputs['First Name'] = w.LabelInput(personal_info, "First Name:", field_spec=fields['First Name'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['First Name'].configure(background='#008ae6')
        self.inputs['First Name'].grid(row=1, column=0, sticky=tk.W, columnspan=3)

        self.inputs['Last Name'] = w.LabelInput(personal_info, "Last Name:", field_spec=fields['Last Name'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Last Name'].configure(background='#008ae6')
        self.inputs['Last Name'].grid(row=1, column=1, sticky=tk.W, columnspan=3)

        self.inputs['Aliases'] = w.LabelInput(personal_info, "Aliases(other names):", field_spec=fields['Aliases'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Aliases'].configure(background='#008ae6')
        self.inputs['Aliases'].grid(column=0, row=2, sticky=tk.W, columnspan=3)

        birth_info = tk.LabelFrame(personal_info, text = 'Sex/Age:', bg='#008ae6', fg='white')
        birth_info.grid(column=0, row=3, sticky='W', padx=5, pady=5, columnspan=2)
        
        self.inputs['Birth Date'] = w.LabelInput(birth_info, 'Birth Date(YYYY-MM-DD):', field_spec=fields['Birth Date'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Birth Date'].configure(background='#008ae6')
        self.inputs['Birth Date'].grid(column=0, row=4)

        self.inputs['Age'] = w.LabelInput(birth_info, 'Age:', field_spec=fields['Age'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Age'].configure(background='#008ae6')
        self.inputs['Age'].grid(column=1, row=4)
        
        self.inputs['Male'] = w.LabelInput(birth_info, 'Male', field_spec=fields['Male'], input_args={'style':'BackgroundCol.TCheckbutton'})
        self.inputs['Male'].configure(background='#008ae6')
        self.inputs['Male'].grid(column=3, row=4)

        self.inputs['Female'] = w.LabelInput(birth_info, 'Female', field_spec=fields['Female'], input_args={'style':'BackgroundCol.TCheckbutton'})
        self.inputs['Female'].configure(background='#008ae6')
        self.inputs['Female'].grid(column=4, row=4)

        phy_desc = tk.LabelFrame(personal_info, text='Physical Description', bg='#008ae6', fg='white')
        phy_desc.grid(column=0, row=7, sticky='W', pady=5, padx=5, columnspan=3)

        self.inputs['Height'] = w.LabelInput(phy_desc, 'Height(ft):', field_spec=fields['Height'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Height'].configure(background='#008ae6')
        self.inputs['Height'].grid(column=0, row=8, sticky='W')

        self.inputs['Weight'] = w.LabelInput(phy_desc, 'Weight(kg):', field_spec=fields['Weight'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Weight'].configure(background='#008ae6')
        self.inputs['Weight'].grid(column=1, row=8, sticky='W')

        self.inputs['Eye Color'] = w.LabelInput(phy_desc, 'Eye Color:', field_spec=fields['Eye Color'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Eye Color'].configure(background='#008ae6')
        self.inputs['Eye Color'].grid(column=2, row=8, sticky='W')

        self.inputs['Hair Color'] = w.LabelInput(phy_desc, 'Hair Color:', field_spec=fields['Hair Color'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Hair Color'].configure(background='#008ae6')
        self.inputs['Hair Color'].grid(column=3, row=8, sticky='W')

        self.inputs['Body Build'] = w.LabelInput(phy_desc, 'Build(Body type):', field_spec=fields['Body Build'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Body Build'].configure(background='#008ae6')
        self.inputs['Body Build'].grid(column=4, row=8, sticky='W')

        self.inputs['Mutation'] = w.LabelInput(phy_desc, 'Mutation(short description):', field_spec=fields['Mutation'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Mutation'].configure(background='#008ae6')
        self.inputs['Mutation'].grid(column=0, row=10, sticky='W', columnspan=3)

        self.inputs['Scars and Marks'] = w.LabelInput(phy_desc, 'Scars and Marks(short description):', field_spec=fields['Scars and Marks'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Scars and Marks'].configure(background='#008ae6')
        self.inputs['Scars and Marks'].grid(column=3, row=10, sticky='W', columnspan=3)
        
        poa = tk.LabelFrame(personal_info, text='Place of Origin', bg='#008ae6', fg='white')
        poa.grid(column=0, row=11, sticky='W', padx=5, pady=5, columnspan=3)

        self.inputs['Nationality']  = w.LabelInput(poa, 'Nationality:', field_spec=fields['Nationality'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Nationality'].configure(background='#008ae6')
        self.inputs['Nationality'].grid(column=0, row=12)
        
        self.inputs['State'] = w.LabelInput(poa, 'State:', field_spec=fields['State'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['State'].configure(background='#008ae6')
        self.inputs['State'].grid(column=1, row=12)
        
        self.inputs['LGA'] = w.LabelInput(poa, 'LGA:', field_spec=fields['LGA'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['LGA'].configure(background='#008ae6')
        self.inputs['LGA'].grid(column=2, row=12)

        self.inputs['Residence Address'] = w.LabelInput(personal_info, 'Residence Address:', field_spec=fields['Residence Address'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Residence Address'].configure(background='#008ae6')
        self.inputs['Residence Address'].grid(column=0, row=13, sticky='W', columnspan=3)

        #-- official --#

        official = tk.LabelFrame(self.scrollable_frame, text='OFFICIAL', bg='#008ae6', fg='white')
        official.grid(column=1, row=2, sticky=(tk.W+tk.N), padx=5)

        self.inputs['Date of Registration'] = w.LabelInput(official, 'Date of Registration:', field_spec=fields['Date of Registration'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Date of Registration'].configure(background='#008ae6')
        self.inputs['Date of Registration'].grid(column=0, row=0, sticky='W')
        
        self.inputs['Date of Arrest'] = w.LabelInput(official, 'Date of Arrest (YYYY-MM-DD):', field_spec=fields['Date of Arrest'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Date of Arrest'].configure(background='#008ae6')
        self.inputs['Date of Arrest'].grid(column=0, row=2, sticky='w')

        self.inputs['Case Number'] = w.LabelInput(official, 'Case Number:', field_spec=fields['Case Number'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Case Number'].configure(background='#008ae6') 
        self.inputs['Case Number'].grid(column=1, row=2, sticky='w')

        self.inputs['Arresting Officer'] = w.LabelInput(official, 'Arresting Officer:', field_spec=fields['Arresting Officer'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Arresting Officer'].configure(background='#008ae6')
        self.inputs['Arresting Officer'].grid(column=0, row=3, sticky=tk.W, columnspan=3)

        self.inputs['Place of Arrest'] = w.LabelInput(official, 'Place of Arrest:', field_spec=fields['Place of Arrest'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Place of Arrest'].configure(background='#008ae6')
        self.inputs['Place of Arrest'].grid(column=0, row=4, sticky=tk.W, columnspan=3)

        station = tk.LabelFrame(official, text='Station', bg='#008ae6', fg='white')
        station.grid(column=0, row=5, sticky='W', padx=5, pady=5, columnspan=3)

        self.inputs['Area'] = w.LabelInput(station, 'Area:', field_spec=fields['Area'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Area'].configure(background='#008ae6')
        self.inputs['Area'].grid(column=0, row=6)

        self.inputs['Division'] = w.LabelInput(station, 'Division:', field_spec=fields['Division'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Division'].configure(background='#008ae6')
        self.inputs['Division'].grid(column=1, row=6)

        crime = tk.LabelFrame(official, text='Crime', bg='#008ae6', fg='white')
        crime.grid(column=0, row=7, sticky='W', padx=5, pady=5, columnspan=3)

        self.inputs['Class of Crime'] = w.LabelInput(crime, 'Class of Crime:', field_spec=fields['Class of Crime'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Class of Crime'].configure(background='#008ae6')
        self.inputs['Class of Crime'].grid(column=0, row=8, sticky=tk.W)

        self.inputs['Ex-Convict'] = w.LabelInput(crime, 'Ex-Convict', field_spec=fields['Ex-Convict'], input_args={'style':'BackgroundCol.TCheckbutton'})
        self.inputs['Ex-Convict'].configure(background='#008ae6')
        self.inputs['Ex-Convict'].grid(column=1, row=8, sticky=tk.W)
        
        self.inputs['Crime'] = w.LabelInput(crime, 'Crime:', field_spec=fields['Crime'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Crime'].configure(background='#008ae6')
        self.inputs['Crime'].grid(column=0, row=9)

        self.inputs['Known Gang'] = w.LabelInput(crime, 'Known Gang:', field_spec=fields['Known Gang'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Known Gang'].configure(background='#008ae6')
        self.inputs['Known Gang'].grid(column=1, row=9)
        
        self.savebutton = ttk.Button(self.scrollable_frame, text="  Save  ", command=self.callbacks['save'])
        self.savebutton.grid(column=0, row=11, padx=10, pady=10, sticky='E')

        self.clearbutton = ttk.Button(self.scrollable_frame, text="  Clear  ", command=self.callbacks['clear'])
        self.clearbutton.grid(column=1, row=11, sticky='W', pady=10, padx=10)

        self.reset()

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data
        
    def reset(self):
        for widget in self.inputs.values():
            widget.set('')
            
        if self.settings['autofill date'].get():    
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['Date of Registration'].set(current_date)
            self.inputs['First Name'].input.focus()

    def get_errors(self):
        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors

    def load_record(self, rownum, data=None):
        self.current_record = rownum
        if rownum is None:
            self.reset()
            self.record_label.config(text='New Record')
        else:
            self.record_label.config(text='Record #{}'.format(rownum))
            for key, widget in self.inputs.items():
                self.inputs[key].set(data.get(key, ''))
                try:
                    widget.input.trigger_focusout_validation()
                except AttributeError:
                    pass
    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self,event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')     


class RecordList(tk.Frame):
    column_defs = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'Case Number': {'label':'Case Number', 'width':100},
        'Date of Registration': {'label':'Date of Registration', 'width':115},
        'First Name':{'label':'First Name', 'width':150, 'stretch':True},
        'Last Name':{'label':'Last Name', 'width':150, 'stretch':True},
        'Age': {'label':'Age(yrs)', 'width':80},        
        'Date of Arrest': {'label':'Date of Arrest', 'width':150},
        'Arresting Officer': {'label':'Arresting Officer', 'width':150, 'stretch':True},
        'Class of Crime': {'label':'Class of Crime', 'width':100, 'stretch':True},
        'Crime': {'label':'Crime', 'width':150, 'stretch':True}

    }

    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, inserted, updated, *args, **kwargs):

        self.inserted = inserted
        self.updated = updated
        
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks

        #-- canvas --#

        self.canvas = tk.Canvas(self, width=985, height=600, highlightthickness=0)
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)

        self.tree_frame = tk.Frame(self.canvas)
        self.tree_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.tree_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.tree_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.tree_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.yscrollbar.grid(row=0, column=1, sticky='NSW')
        self.xscrollbar.grid(row=1, column=0, sticky='EWS')

        #-- treeview --#

        self.treeview = ttk.Treeview(self.tree_frame, columns=list(self.column_defs.keys())[1:],
                                     selectmode='browse')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.treeview.grid(row=0, column=0, sticky='NSEW')

        self.treeview.config(show = 'headings')

        self.treeview.heading('#0', text='Row')
        self.treeview.heading('Case Number', text='Case Number')
        self.treeview.heading('Date of Registration', text='Date of Registration')
        self.treeview.heading('First Name', text='First Name')
        self.treeview.heading('Last Name', text='Last Name')
        self.treeview.heading('Age', text='Age')
        self.treeview.heading('Date of Arrest', text='Date of Arrest')
        self.treeview.heading('Arresting Officer', text='Arresting Officer')
        self.treeview.heading('Class of Crime', text='Class of Crime')
        self.treeview.heading('Crime', text='Crime')

        self.treeview.column('#0', anchor=tk.CENTER, width=50, stretch=False)
        self.treeview.column('Case Number', anchor=tk.CENTER, width=100, stretch=False)
        self.treeview.column('Date of Registration', anchor=tk.CENTER, width=150, stretch=False)
        self.treeview.column('First Name', anchor=tk.CENTER, width=150, stretch=True)
        self.treeview.column('Last Name', anchor=tk.CENTER, width=150, stretch=True)
        self.treeview.column('Age', anchor=tk.CENTER, width=80, stretch=False)
        self.treeview.column('Date of Arrest', anchor=tk.CENTER, width=100, stretch=False)
        self.treeview.column('Arresting Officer', anchor=tk.CENTER, width=150, stretch=True)
        self.treeview.column('Class of Crime', anchor=tk.CENTER, width=100, stretch=True)
        self.treeview.column('Crime', anchor=tk.CENTER, width=150, stretch=True)
        
        self.treeview.bind('<<TreeviewOpen>>', self.on_open_record)

        self.treeview.tag_configure('insert', background='lightblue')
        self.treeview.tag_configure('update', background='grey') 

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self,event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        

    def populate(self, rows):

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        valuekeys = list(self.column_defs.keys())[1:]
        for rowdata in rows:
            rowkey = (str(rowdata['Case Number']), str(rowdata['Date of Registration']))
            values = [rowdata[key] for key in valuekeys]

            if self.inserted and rowkey in self.inserted:
                tag = 'inserted'
            elif self.updated and rowkey in self.updated:
                tag = 'updated'
            else:
                tag = ''
            stringkey = '{}|{}'.format(*rowkey)
            self.treeview.insert('', 'end', iid=stringkey, text=stringkey,
                                 values=values, tag=tag)

        if len(rows) > 0:
            firstrow = self.treeview.identify_row(0)
            self.treeview.focus_set()
            self.treeview.selection_set(firstrow)
            self.treeview.focus(firstrow)

    def on_open_record(self, *args):
        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_record'](selected_id.split('|'))
        

class LoginDialog(Dialog):

    def __init__(self, parent, title, error=''):
        self.pw = tk.StringVar()
        self.user = tk.StringVar()
        self.error = tk.StringVar(value=error)
        super().__init__(parent, title=title)

    def body(self, parent):
        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        
        self.configure(bg='#008ae6')
        
        lf = tk.Frame(self, bg='#008ae6')
        tk.Label(lf, text='Login to Criminal Tracker', font=('Droid sans', 20), bg='#008ae6', fg='white').grid(padx=10, pady=10, columnspan=2)
        
        if self.error.get():
            tk.Label(lf, textvariable=self.error, bg='darkred', fg='white').grid(pady=7, row=1, columnspan=2) 
        
        tk.Label(lf, text='Username:', font=('Droid sans', 10, 'bold'), bg='#008ae6', fg='white').grid(column=0, row=2, pady=10, padx=10, sticky='e')
        self.username_inp = ttk.Entry(lf, textvariable=self.user)
        self.username_inp.grid(column=1, row=2, pady=10, padx=10, sticky='w')

        tk.Label(lf, text='Password:', font=('Droid sans', 10, 'bold'), bg='#008ae6', fg='white').grid(column=0, row=4, pady=10, padx=10, sticky='e')
        self.password_inp = ttk.Entry(lf, show='*', textvariable=self.pw)
        self.password_inp.grid(column=1, row=4, pady=10, padx=10, sticky='w')

        lf.pack()
        return self.username_inp
   
    def apply(self):
        self.result = (self.user.get(), self.pw.get())


class SearchDialog(Dialog):

    def __init__(self, parent, title, error=''):
        self.selected = tk.StringVar()
        self.search_inp = tk.StringVar()
        self.error = tk.StringVar(value=error)
        super().__init__(parent, title)

    def body(self, parent):
        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        frame = tk.Frame(self)

        self.keyword = tk.Label(frame, text='Keyword:')
        self.keyword.grid(column=0, row=0, pady=10, padx=10)

        self.search_box = tk.Entry(frame, textvariable=self.search_inp, width='22')
        self.search_box.grid(column=1, row=0, pady=10, padx=10)

        self.category = tk.Label(frame, text='Category:')
        self.category.grid(column=0, row=1, pady=10, padx=10)

        self.option_search = ttk.Combobox(frame, textvariable=self.selected,
                                     value=["   --select--", "Case Number", "Date of Registration", "First Name", "Last Name", "Male", "Female", "Age", "Nationality"])
        self.option_search.current(0)
        self.option_search.grid(column=1, row=1, pady=10, padx=10)

        if self.error.get():
            tk.Label(frame, textvariable=error, fg="white", bg="darkred").grid(row=3, pady=10, padx=10, columnspan=3)

        frame.pack()
        
    def buttonbox(self):
        self.search_button = tk.Button(self, text="  Search  ", command=self.search_command)
        self.search_button.pack(side= tk.RIGHT, padx=10, pady=10)

    def search_command(self):
        self.search = (self.selected.get(), self.search_inp.get())
        

        
        









