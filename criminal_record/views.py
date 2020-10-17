import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import widgets as w
from . import models as m
from .help import Details as h
from .images import ctracker_32
from .images import ctracker_64
from tkinter.simpledialog import Dialog


class MainMenu(tk.Menu):
    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label='New Arrest Form', command=callbacks['new_record'])
        file_menu.add_command(label='New Incidence Form', command=callbacks['new_irecord'])
        file_menu.add_separator()
        file_menu.add_command(label="Save Arrest                     Ctrl+S", command=callbacks['saveAF'])
        file_menu.add_command(label="Save Incidence Form     Ctrl+S", command=callbacks['saveIF'])
        file_menu.add_command(label='Save in CSV                    Ctrl+Shift+S', command=callbacks['savein'])
        file_menu.add_separator()
        file_menu.add_command(label='Exit                                  Ctrl+Q', command=callbacks['quit'])
        self.add_cascade(label='File', menu=file_menu)
        
        edit_menu = tk.Menu(self, tearoff=False)
        edit_menu.add_command(label='Copy', command = '')
        edit_menu.add_command(label='Cut', command='')
        edit_menu.add_command(label='Paste', command='')
        edit_menu.add_command(label='Undo', command='')
        self.add_cascade(label='Edit', menu=edit_menu)
        
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
                variable=settings['theme']
            )
        options_menu.add_cascade(label='Theme       *(requires restart)', menu=themes_menu)

        self.add_cascade(label='Options', menu=options_menu)

        view_menu = tk.Menu(self, tearoff=False)
        view_menu.add_command(label='Arrest Record', command=callbacks['show_recordlist'])
        view_menu.add_command(label='Incidence Record', command=callbacks['show_incidence_list'])
        view_menu.add_command(label='Volent Inmates', command=callbacks['violent_list'])
        view_menu.add_command(label='Crime Occuring Areas', command=callbacks['crime_area'])

        self.add_cascade(label='View', menu=view_menu)

        search_menu = tk.Menu(self, tearoff=False)
        search_menu.add_command(label='Search Arrest Record', command=callbacks['searchAR'])
        search_menu.add_command(label='Search Incidence List', command=callbacks['searchIL'])
        self.add_cascade(label='Search', menu=search_menu)
        
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='View Help', command=self.view_help)
        help_menu.add_command(label='About Criminal Tracker', command=self.show_about)     
        self.add_cascade(label='Help', menu=help_menu)

    def show_about(self):
        about_message = 'CRIMINAL TRACKER \nversion 2.0'
        about_detail = ('For assistance please read the docs \nor contact the developer. '
                        '\n\n\n\t\tpowered by Kurious Geek')

        messagebox.showinfo(title='About... ', message=about_message, detail=about_detail)

    def view_help(self):
        HelpView(self)
        
        
    def on_theme_change(self, *args):
        message = 'Theme change requires restart'
        detail = ('Changing theme requires application restart\n'
                  'Your work progress might be lost\n'
                  'Do you want to continue?')
        messagebox.showwarning(title='Warning', message=message, detail=detail)


class LandingPage(tk.Frame):

    def __init__(self):

        #tk.Toplevel.__init__(self)
        #self.transient(parent)

        #self.title('Home')

        self.result = None

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        #self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        '''self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))'''

        self.initial_focus.focus_set()

        self.wait_window(self)


    def body(self, master):

        pass

    def buttonbox(self):

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()


    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        #self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1 

    def apply(self):

         self.result = 'result'


class SaveDialog(Dialog):

    def __init__(self, parent, title):
        super().__init__(parent, title=title)

    def body(self, parent):
        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)
        
        mf = tk.Frame(self)

        message = tk.Label(mf, text='Select Save options', font=('Droid sans', 9))
        message.grid(pady=20)

        mf.pack()

    def buttonbox(self):

        box = tk.Frame(self)

        sar = tk.Button(box, text="Save to Arrest Record", command=lambda:self.ok('sar'))
        sar.pack(side=tk.LEFT, padx=5, pady=5)

        sir = tk.Button(box, text="Save to Incidence Record", command=lambda:self.ok('sir'))
        sir.pack(side=tk.LEFT, padx=5, pady=5)

        box.pack()

    def ok(self, type):

        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        if type == 'sar':
            self.apply('sar')
        elif type == 'sir':
            self.apply('sir')
        else:
            print('the code has been tampered with')

        self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1
   
    def apply(self, type):
        if type == 'sar':
            self.result = 'saveAF'
        elif type == 'sir':
            self.result = 'saveIF'
        else:
            print('the code has been tampered with')


class HelpView(tk.Toplevel):

    def __init__(self, parent):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        self.title('Help')
        self.resizable(width=False, height=False)
        self.parent = parent
        self.detail = h.details

        self.initial_focus = self.body()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)
        

    def body(self):
        self.configure(background='#008ae6')
        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        header_frame = tk.Frame(self, bg='#008ae6')
        header_frame.grid(row=0, column=0)

        self.logo = tk.PhotoImage(file=ctracker_64)
        self.logo_label=tk.Label(header_frame, image=self.logo, highlightthickness=0, borderwidth=0)
        self.logo_label.grid(row=0, column=0)

        self.head_label = tk.Label(header_frame, text='Criminal Tracker', font=('Droid sans', 20), background='#008ae6', foreground='white')
        self.head_label.grid(row=0, column=1, pady=20, padx=(10, 0))

        self.head_label1 = tk.Label(header_frame, text='v2.0', background='#008ae6', foreground='white')
        self.head_label1.grid(row=0, column=2)

        self.canvas = tk.Canvas(self, width=700, height=600, highlightthickness=0)
        yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        xscrollbar = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)

        self.detail_frame = tk.Frame(self.canvas, bg='#008ae6')
        self.detail_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.detail_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.detail_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.detail_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)       

        self.canvas.grid(row=1, column=0, sticky='NSEW')
        yscrollbar.grid(row=0, column=3, sticky='NS', rowspan=2, columnspan=2)
        xscrollbar.grid(row=2, column=0, sticky='EW', columnspan=3)
 
        self.detail_label = tk.Label(self.detail_frame, text=self.detail, justify=tk.LEFT, background='#008ae6', foreground='white')
        self.detail_label.grid(row=0, padx=20, pady=(20, 0))


    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units') 


    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

        
class DataRecordForm(tk.Frame):
    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.current_record = None
        self.config(background='#008ae6')

        style = ttk.Style()
        style.configure('BackgroundCol.TLabel', background='#008ae6', foreground='white')
        style.configure('BackgroundCol.TCheckbutton', background='#008ae6', foreground='white')
        
        self.inputs = {}

        self.canvas = tk.Canvas(self, width=970, height=600, highlightthickness=0, bg='#008ae6')
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
        yscrollbar.grid(row=0, column=3, sticky='NS', rowspan=2)
        xscrollbar.grid(row=1, column=0, sticky='EW', columnspan=2)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.logo = tk.PhotoImage(file=ctracker_64)
        self.logo_label=tk.Label(self.scrollable_frame, image=self.logo, highlightthickness=0, borderwidth=0, background='#008ae6')
        self.logo_label.grid(row=0, columnspan=2, pady=10)

        self.record_label = ttk.Label(self.scrollable_frame, style='BackgroundCol.TLabel')
        self.record_label.grid(row=1, columnspan=2)
        
        #-- personal information --#
        
        personal_info = tk.LabelFrame(self.scrollable_frame, text = 'PERSONAL INFORMATION', bg='#008ae6', fg='white')
        personal_info.grid(row=2, column=0, padx=(17, 5))

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
        
        self.inputs['Gender'] = w.LabelInput(birth_info, 'Gender:', field_spec=fields['Gender'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Gender'].configure(background='#008ae6')
        self.inputs['Gender'].grid(column=3, row=4)

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

        self.inputs['Violent'] = w.LabelInput(crime, 'Violent', field_spec=fields['Violent'], input_args={'style':'BackgroundCol.TCheckbutton'})
        self.inputs['Violent'].configure(background='#008ae6')
        self.inputs['Violent'].grid(column=2, row=8, sticky=tk.W)
        
        self.inputs['Crime'] = w.LabelInput(crime, 'Crime:', field_spec=fields['Crime'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Crime'].configure(background='#008ae6')
        self.inputs['Crime'].grid(column=0, row=9)

        self.inputs['Known Gang'] = w.LabelInput(crime, 'Known Gang:', field_spec=fields['Known Gang'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Known Gang'].configure(background='#008ae6')
        self.inputs['Known Gang'].grid(column=1, row=9, columnspan=2)
        
        self.savebutton = ttk.Button(self.scrollable_frame, text="  Save  ", command=self.callbacks['saveAF'])
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

    def load_record(self, rownum, data=None, event=None):
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

    def focus(self):
        self.inputs['First Name'].input.focus()    


class RecordList(tk.Frame):
    column_defs = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'Case Number': {'label':'Case Number', 'width':90},
        'Date of Registration': {'label':'Date of Registration', 'width':115},
        'First Name':{'label':'First Name', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Last Name':{'label':'Last Name', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Age': {'label':'Age(yrs)', 'width':70},
        'Gender': {'label': 'Gender', 'width':70}, 
        'Height': {'label':'Height(ft)', 'width':80},
        'Weight': {'label':'Weight(kg)', 'width':80},       
        'Date of Arrest': {'label':'Date of Arrest', 'width':100},
        'Arresting Officer': {'label':'Arresting Officer', 'width':150, 'stretch':True},
        'Class of Crime': {'label':'Class of Crime', 'width':130, 'stretch':True},
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

        self.canvas = tk.Canvas(self, width=970, height=623, highlightthickness=0)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        
        self.tree_frame = tk.Frame(self.canvas)
        self.tree_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.tree_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)

        self.tree_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.tree_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.xscrollbar.grid(row=1, column=0, sticky='EWS')
        


        #-- treeview --#

        self.treeview = ttk.Treeview(self.tree_frame, height=30, columns=list(self.column_defs.keys())[1:],
                                     selectmode='browse')
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='NSW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.treeview.grid(row=0, column=0, sticky='NSWE')

        self.treeview.configure(yscrollcommand=self.yscrollbar.set)
        self.treeview.config(show = 'headings')

        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)

            self.treeview.heading(name, text=label, anchor=self.default_anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)

        self.treeview.bind('<<TreeviewOpen>>', self.on_open_record)

        self.treeview.tag_configure('inserted', background='lightblue')
        self.treeview.tag_configure('updated', background='grey') 

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.treeview.yview_scroll(int(-1*(event.delta/120)), 'units')

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
        tk.Label(lf, text='Sign in to Criminal Tracker', font=('Droid sans', 18), bg='#008ae6', fg='white').grid(padx=10, pady=10, columnspan=2)
        
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

    def buttonbox(self):

        box = tk.Frame(self, bg='#008ae6')

        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        w = tk.Button(box, text="Login", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1
   
    def apply(self):
        self.result = (self.user.get(), self.pw.get())


class SearchDialog(Dialog):

    def __init__(self, parent, title, type):
        self.category = tk.StringVar()
        self.search_inp = tk.StringVar()
        self.type = type
        super().__init__(parent, title)
        
    def body(self, parent):
        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        frame = tk.Frame(self)

        self.keyword = tk.Label(frame, text='Keyword :')
        self.keyword.grid(column=0, row=0, pady=10, padx=10)

        self.search_box = tk.Entry(frame, textvariable=self.search_inp, width='22')
        self.search_box.grid(column=1, row=0, pady=10, padx=10)

        self.Category = tk.Label(frame, text='Category :')
        self.Category.grid(column=0, row=1, pady=10, padx=10)

        if self.type == 'arrest':
            self.option_search = ttk.Combobox(frame, textvariable=self.category,
                                         value=["   --select--", "Case Number", "Date of Registration", "First Name", "Last Name", "Gender", "Age", "Arresting Officer", "Class of Crime", "Known Gang"])
        elif self.type == 'incidence':
            self.option_search = ttk.Combobox(frame, textvariable=self.category,
                                         value=["   --select--", "CaseID", "Registration Date", "Full Name", "Type of Incidence", "Officer in Charge", "District", "Contact"])
        self.option_search.current(0)
        self.option_search.grid(column=1, row=1, pady=10, padx=10)

        frame.pack()

        return self.search_box 
        
    def buttonbox(self):
        self.search_button = tk.Button(self, text="  Search  ", command=self.ok)
        self.search_button.pack(side= tk.RIGHT, padx=10, pady=10)
        self.bind("<Return>", self.ok)

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

    def validate(self):
        return 1
       
    def apply(self):
        self.result = (self.category.get(), self.search_inp.get())
       

class SearchResult(tk.Toplevel):

    column_defs_AR = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'Case Number': {'label':'Case Number', 'width':90},
        'Date of Registration': {'label':'Date of Registration', 'width':115},
        'First Name':{'label':'First Name', 'width':100, 'anchor':tk.W, 'stretch':True},
        'Last Name':{'label':'Last Name', 'width':100, 'anchor':tk.W, 'stretch':True},
        'Aliases':{'label':'Aliases', 'width':100, 'anchor':tk.W, 'stretch':True},
        'Birth Date':{'label':'Birth Date', 'width':100},
        'Age': {'label':'Age(yrs)', 'width':70}, 
        'Gender':{'label':'Gender', 'width':0},
        'Height': {'label':'Height(ft)', 'width':80},
        'Weight': {'label':'Weight(kg)', 'width':80},
        'Eye Color':{'label':'Eye Color', 'width':80, 'anchor':tk.W},
        'Hair Color':{'label':'Hair Color', 'width':80, 'anchor':tk.W},
        'Body Build':{'label':'Build(Body Type)', 'width':100},
        'Mutation':{'label':'Mutation(short description)', 'width':150, 'stretch':True},
        'Scars and Marks':{'label':'Scars & Marks(short description)', 'width':165, 'stretch':True},
        'Nationality':{'label':'Nationality', 'width':115, 'stretch':True},
        'State':{'label':'State', 'width':100, 'stretch':True},
        'LGA':{'label':'LGA', 'width':80, 'stretch':True},
        'Residence Address':{'label':'Residence Address', 'width':150, 'stretch':True},      
        'Date of Arrest':{'label':'Date of Arrest', 'width':100},
        'Arresting Officer': {'label':'Arresting Officer', 'width':150, 'stretch':True},
        'Place of Arrest': {'label':'Place of Arrest', 'width':150, 'stretch':True},
        'Area': {'label':'Area', 'width':70},
        'Division':{'label':'Division', 'width':70, 'anchor':tk.CENTER},
        'Ex-Convict':{'label':'Ex-Convict', 'width':90},
        'Violent':{'label':'Violent', 'width':90},
        'Class of Crime': {'label':'Class of Crime', 'width':130, 'anchor':tk.W, 'stretch':True},
        'Known Gang': {'label':'Known Gang', 'width':120, 'stretch':True},
        'Crime': {'label':'Crime', 'width':150, 'stretch':True}

        }

    column_defs_IL = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'CaseID': {'label':'CaseID', 'width':90},
        'Registration Date': {'label':'Registration Date', 'width':115},
        'Full Name':{'label':'Full Name', 'width':130, 'anchor':tk.W, 'stretch':True},
        'Contact':{'label':'Contact', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Officer in Charge': {'label':'Officer in Charge', 'width':120, 'anchor':tk.W, 'stretch':True},
        'District': {'label': 'District', 'width':90}, 
        'Statement': {'label':'Statement', 'width':150, 'anchor':tk.W, 'stretch':True},
        'Type of Incidence': {'label':'Type of Incidence', 'width':120},       
        'Evidence': {'label':'Evidence', 'width':150, 'anchor':tk.W, 'stretch':True},
        'Witness': {'label':'Witness', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Other Info': {'label':'Other Info', 'width':150, 'anchor':tk.W, 'stretch':True}

    }

    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, results, type, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title(title)

        self.parent = parent
        self.result = None
        self.results = results
        self.type = type

        
        self.initial_focus = self.body()

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self):

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        self.rcanvas = tk.Canvas(self, width=600, height=400, highlightthickness=0)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.rcanvas.xview)

        frame = tk.Frame(self.rcanvas)
        frame.bind('<Configure>', lambda e: self.rcanvas.configure(scrollregion=self.rcanvas.bbox(tk.ALL)))
        self.rcanvas.create_window((0, 0), window=frame, anchor='nw')
        self.rcanvas.configure(xscrollcommand=self.xscrollbar.set)

        self.rcanvas.grid(row=0, column=0, sticky='NSEW')
        self.xscrollbar.grid(row=1, column=0, sticky='EWS', columnspan=2)

        if self.type == 'arrest':
            self.searchview = ttk.Treeview(frame, height=30, columns=list(self.column_defs_AR.keys())[1:], selectmode='browse')
        elif self.type == 'incidence':
            self.searchview = ttk.Treeview(frame, height=30, columns=list(self.column_defs_IL.keys())[1:], selectmode='browse')

        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.searchview.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='NSW')
        
        self.searchview.config(show = 'headings')
        self.searchview.configure(yscrollcommand=self.yscrollbar.set)

        for name, definition in (self.column_defs_AR.items() if self.type == 'arrest' else self.column_defs_IL.items()):
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)

            self.searchview.heading(name, text=label, anchor=self.default_anchor)
            self.searchview.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)
        
        self.searchview.grid(row=0, column=0, sticky='NSEW')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        for row in self.searchview.get_children():
            self.searchview.delete(row)

        if self.type == 'arrest':
            valuekeys = list(self.column_defs_AR.keys())[1:]
            for rowdata in self.results:
                rowkey = (str(rowdata['Case Number']), str(rowdata['Date of Registration']))
                values = [rowdata[key] for key in valuekeys]

                stringkey = '{}|{}'.format(*rowkey)
                self.searchview.insert('', 'end', iid=stringkey, text=stringkey,
                                     values=values)

        elif self.type == 'incidence':
            valuekeys = list(self.column_defs_IL.keys())[1:]
            for rowdata in self.results:
                rowkey = (str(rowdata['CaseID']), str(rowdata['Registration Date']))
                values = [rowdata[key] for key in valuekeys]

                stringkey = '{}|{}'.format(*rowkey)
                self.searchview.insert('', 'end', iid=stringkey, text=stringkey,
                                     values=values)

    def buttonbox(self):
        box = tk.Frame(self)

        csvbtn = tk.Button(box, text='Extract to CSV', command=self.ok)
        csvbtn.pack(side=tk.LEFT, pady=5, padx=5)

        canbtn = tk.Button(box, text=' Close ', command=self.cancel)
        canbtn.pack(side=tk.LEFT, pady=5, padx=5)

        box.grid()

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1 

    def apply(self):

       self.result = self.results


class IncidenceForm(tk.Frame):
    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.settings = settings
        self.callbacks = callbacks
        self.current_record = None
        self.config(background='#008ae6')

        style = ttk.Style()
        style.configure('BackgroundCol.TLabel', background='#008ae6', foreground='white')
        style.configure('BackgroundCol.TCheckbutton', background='#008ae6', foreground='white')
        
        self.inputs = {}

        self.canvas = tk.Canvas(self, width=970, height=600, highlightthickness=0, bg='#008ae6')
        yscrollbar = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        xscrollbar = tk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)

        self.scroll_frame = tk.Frame(self.canvas)
        self.scroll_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.scroll_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scroll_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.scroll_frame.config(bg='#008ae6')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)       

        self.canvas.grid(row=0, column=0, sticky='NSEW', columnspan=2)
        yscrollbar.grid(row=0, column=3, sticky='NS', rowspan=2, columnspan=2)
        xscrollbar.grid(row=1, column=0, sticky='EW', columnspan=2)        

        self.logo = tk.PhotoImage(file=ctracker_64)
        self.logo_label=tk.Label(self.scroll_frame, image=self.logo, highlightthickness=0, borderwidth=0, background='#008ae6')
        self.logo_label.grid(row=0, columnspan=5, pady=10)

        self.form_label = ttk.Label(self.scroll_frame, style='BackgroundCol.TLabel')
        self.form_label.grid(row=1, columnspan=5)

        self.frame = tk.Frame(self.scroll_frame, bg='#008ae6')
        self.frame.grid(row=2, padx=25, pady=10, sticky='NSWE')

        self.inputs['CaseID'] = w.LabelInput(self.frame, "CaseID:", field_spec=fields['CaseID'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['CaseID'].configure(background='#008ae6')
        self.inputs['CaseID'].grid(row=1, column=0, sticky=tk.W) 

        self.inputs['Registration Date'] = w.LabelInput(self.frame, "Registration Date:", field_spec=fields['Registration Date'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Registration Date'].configure(background='#008ae6')
        self.inputs['Registration Date'].grid(row=1, column=1, sticky=tk.W)

        self.inputs['Full Name'] = w.LabelInput(self.frame, "Full Name:", field_spec=fields['Full Name'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Full Name'].configure(background='#008ae6')
        self.inputs['Full Name'].grid(row=1, column=2, sticky=tk.W, columnspan=2)

        self.inputs['Contact'] = w.LabelInput(self.frame, "Contact:", field_spec=fields['Contact'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Contact'].configure(background='#008ae6')
        self.inputs['Contact'].grid(row=1, column=4, sticky=tk.W)

        self.inputs['Officer in Charge'] = w.LabelInput(self.frame, "Officer in Charge:", field_spec=fields['Officer in Charge'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Officer in Charge'].configure(background='#008ae6')
        self.inputs['Officer in Charge'].grid(row=2, column=0, sticky=tk.W, columnspan=5)

        self.inputs['District'] = w.LabelInput(self.frame, "District:", field_spec=fields['District'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['District'].configure(background='#008ae6')
        self.inputs['District'].grid(row=2, column=3, sticky=tk.W, columnspan=2)

        self.inputs['Statement'] = w.LabelInput(self.frame, "Statement:", field_spec=fields['Statement'], label_args={'style': 'BackgroundCol.TLabel'})
        self.inputs['Statement'].configure(background='#008ae6')
        self.inputs['Statement'].grid(row=3, column=0, sticky=tk.W, columnspan=4, rowspan=4)

        self.inputs['Type of Incidence'] = w.LabelInput(self.frame, 'Type of Incidence:', field_spec=fields['Type of Incidence'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Type of Incidence'].configure(background='#008ae6')
        self.inputs['Type of Incidence'].grid(row=3, column=4, sticky=tk.W)

        self.inputs['Evidence'] = w.LabelInput(self.frame, 'Evidence:', field_spec=fields['Evidence'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Evidence'].configure(background='#008ae6')
        self.inputs['Evidence'].grid(row=4, column=4, sticky=tk.W)

        self.inputs['Witness'] = w.LabelInput(self.frame, 'Witness:', field_spec=fields['Witness'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Witness'].configure(background='#008ae6')
        self.inputs['Witness'].grid(row=5, column=4, sticky=tk.W)

        self.inputs['Other Info'] = w.LabelInput(self.frame, 'Other Info:', field_spec=fields['Other Info'], label_args={'style':'BackgroundCol.TLabel'})
        self.inputs['Other Info'].configure(background='#008ae6')
        self.inputs['Other Info'].grid(row=6, column=4, sticky=tk.W)

        butnframe = tk.Frame(self.scroll_frame, bg='#008ae6')
        butnframe.grid(row=7, columnspan=5)

        self.savebuton = ttk.Button(butnframe, text="  Save  ", command=self.callbacks['saveIF'])
        self.savebuton.grid(column=0, row=1, padx=10, pady=10, sticky='E')

        self.clearbuton = ttk.Button(butnframe, text="  Clear  ", command=self.reset )
        self.clearbuton.grid(column=1, row=1, pady=10, padx=10, sticky='W') 

        self.reset() 

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')      

    def reset(self):
        for widget in self.inputs.values():
            widget.set('')
            
        if self.settings['autofill date'].get():    
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['Registration Date'].set(current_date)
            self.inputs['CaseID'].input.focus()

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def get_errors(self):
        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors

    def load_record(self, rownum, data=None, event=None):
        self.current_record = rownum
        if rownum is None:
            self.reset()
            self.form_label.config(text='New Record')
        else:
            self.form_label.config(text='Record #{}'.format(rownum))
            for key, widget in self.inputs.items():
                self.inputs[key].set(data.get(key, ''))
                try:
                    widget.input.trigger_focusout_validation()
                except AttributeError:
                    pass    

    def focus(self):
        self.inputs['CaseID'].input.focus()


class IncidenceList(tk.Frame):

    icolumn_defs = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'CaseID': {'label':'CaseID', 'width':90},
        'Registration Date': {'label':'Registration Date', 'width':115},
        'Full Name':{'label':'Full Name', 'width':130, 'anchor':tk.W, 'stretch':True},
        'Contact':{'label':'Contact', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Officer in Charge': {'label':'Officer in Charge', 'width':120, 'anchor':tk.W, 'stretch':True},
        'District': {'label': 'District', 'width':90}, 
        'Statement': {'label':'Statement', 'width':150, 'anchor':tk.W, 'stretch':True},
        'Type of Incidence': {'label':'Type of Incidence', 'width':120},       
        'Evidence': {'label':'Evidence', 'width':150, 'anchor':tk.W, 'stretch':True},
        'Witness': {'label':'Witness', 'width':120, 'anchor':tk.W, 'stretch':True},
        'Other Info': {'label':'Other Info', 'width':150, 'anchor':tk.W, 'stretch':True}

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

        self.canvas = tk.Canvas(self, width=970, height=623, highlightthickness=0)
        self.xscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        
        self.tree_frame = tk.Frame(self.canvas)
        self.tree_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.tree_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=self.xscrollbar.set)

        self.tree_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.tree_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.canvas.grid(row=0, column=0, sticky='NSEW')
        self.xscrollbar.grid(row=1, column=0, sticky='EWS')
        

        #-- treeview --#

        self.treeview = ttk.Treeview(self.tree_frame, height=30, columns=list(self.icolumn_defs.keys())[1:],
                                     selectmode='browse')
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='NSW')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.treeview.grid(row=0, column=0, sticky='NSWE')

        self.treeview.configure(yscrollcommand=self.yscrollbar.set)
        self.treeview.config(show = 'headings')

        for name, definition in self.icolumn_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)

            self.treeview.heading(name, text=label, anchor=anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)

        self.treeview.bind('<<TreeviewOpen>>', self.on_open_irecord)

        self.treeview.tag_configure('insert', background='lightblue')
        self.treeview.tag_configure('update', background='grey') 

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.treeview.yview_scroll(int(-1*(event.delta/120)), 'units')

    def populate(self, rows):

        for row in self.treeview.get_children():
            self.treeview.delete(row)

        valuekeys = list(self.icolumn_defs.keys())[1:]
        for rowdata in rows:
            rowkey = (str(rowdata['CaseID']), str(rowdata['Registration Date']))
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

    def on_open_irecord(self, *args):
        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_irecord'](selected_id.split('|'))    


class ViolentList(tk.Toplevel):

    column_defs = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'Case Number': {'label':'Case Number', 'width':90},
        'First Name':{'label':'First Name', 'width':150, 'anchor':tk.W, 'stretch':True},
        'Last Name':{'label':'Last Name', 'width':150, 'anchor':tk.W, 'stretch':True}
        }

    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, results, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.resizable(width=False, height=True)
        self.title(title)

        self.parent = parent
        self.callbacks = callbacks
        self.result = None
        self.results = results

        self.initial_focus = self.body()

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self):

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0)

        self.violent_list_view = ttk.Treeview(frame, height=25, columns=list(self.column_defs.keys())[1:], selectmode='browse')
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.violent_list_view.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='NSE')
        
        self.violent_list_view.config(show = 'headings')
        self.violent_list_view.configure(yscrollcommand=self.yscrollbar.set)

        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)

            self.violent_list_view.heading(name, text=label, anchor=self.default_anchor)
            self.violent_list_view.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)
        
        self.violent_list_view.bind('<<TreeviewOpen>>', self.on_open_list)

        self.violent_list_view.grid(row=0, column=0, sticky='NSEW')
        self.rowconfigure(0, weight=1)

        for row in self.violent_list_view.get_children():
            self.violent_list_view.delete(row)
        valuekeys = list(self.column_defs.keys())[1:]
        for rowdata in self.results:
            rowkey = (str(rowdata['Case Number']), str(rowdata['First Name']))
            values = [rowdata[key] for key in valuekeys]

            stringkey = '{}|{}'.format(*rowkey)
            self.violent_list_view.insert('', 'end', iid=stringkey, text=stringkey,
                                 values=values)

    def buttonbox(self):
        box = tk.Frame(self)

        csvbtn = tk.Button(box, text='Extract to CSV', command=self.ok)
        csvbtn.pack(side=tk.LEFT, pady=5, padx=5)

        canbtn = tk.Button(box, text=' Close ', command=self.cancel)
        canbtn.pack(side=tk.LEFT, pady=5, padx=5)

        box.grid()

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1 

    def apply(self):

        self.result = self.results 

    def on_open_list(self, *args):
        selected_id = self.violent_list_view.selection()[0]
        self.callbacks['on_open_vlist'](selected_id.split('|'))
        

class ViolentData(tk.Toplevel):

    def __init__(self, parent, results, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.resizable(width=False, height=False)

        self.parent = parent
        self.result = None
        self.results = results

        body = tk.Frame(self)
        self.initial_focus = self.body(body)
        body.grid(padx=5, pady=5)

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    def body(self, master):

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        value_frame = tk.Frame(self)
        value_frame.grid(row=0, column=1, padx=20, pady=20)
        for index, data in enumerate(self.results):
            num=0
            for field in data:
                label = tk.Label(value_frame, text=str(field).title().replace('\n', ''))
                label.grid(column=index, row=num, sticky=tk.W)
                num +=1

        key_frame = tk.Frame(self)
        key_frame.grid(row=0, column=0, padx=20, pady=20) 
        key = list(m.SQLModel.fields.keys())
        for index, x in enumerate(key):
            num=0
            label = tk.Label(key_frame, text=str(x) + ' :')
            label.grid(column=num, row=index, sticky=tk.W)
            num +=1
            

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()


class CrimeArea(tk.Toplevel):

    column_defs = {
        '#0': {'label':'Row', 'anchor':tk.W},
        'Case Number': {'label':'Case Number', 'width':90},
        'Place of Arrest':{'label':'Areas Crime Occured', 'width':250, 'anchor':tk.W, 'stretch':True},
        }

    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, results, title=None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.resizable(width=False, height=True)
        self.title(title)

        self.parent = parent
        self.callbacks = callbacks
        self.result = None
        self.results= results

        self.initial_focus = self.body()

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    def body(self):

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.tk.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0)

        self.crime_area_view = ttk.Treeview(frame, height=25, columns=list(self.column_defs.keys())[1:], selectmode='browse')
        self.yscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.crime_area_view.yview)
        self.yscrollbar.grid(row=0, column=1, sticky='NSE')
        
        self.crime_area_view.config(show = 'headings')
        self.crime_area_view.configure(yscrollcommand=self.yscrollbar.set)

        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)

            self.crime_area_view.heading(name, text=label, anchor=self.default_anchor)
            self.crime_area_view.column(name, anchor=anchor, minwidth=minwidth, width=width, stretch=stretch)

        self.crime_area_view.grid(row=0, column=0, sticky='NSEW')
        self.rowconfigure(0, weight=1)

        for row in self.crime_area_view.get_children():
            self.crime_area_view.delete(row)
        valuekeys = list(self.column_defs.keys())[1:]
        for rowdata in self.results:
            rowkey = (str(rowdata['Case Number']), str(rowdata['Place of Arrest']))
            values = [rowdata[key] for key in valuekeys]

            stringkey = '{}|{}'.format(*rowkey)
            self.crime_area_view.insert('', 'end', iid=stringkey, text=stringkey,
                                 values=values)

    def buttonbox(self):
        box = tk.Frame(self)

        csvbtn = tk.Button(box, text='Extract to CSV', command=self.ok)
        csvbtn.pack(side=tk.LEFT, pady=5, padx=5)

        canbtn = tk.Button(box, text=' Close ', command=self.cancel)
        canbtn.pack(side=tk.LEFT, pady=5, padx=5)

        box.grid()

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()
        self.cancel()

    def cancel(self, event=None):

        self.parent.focus_set()
        self.destroy()

    def validate(self):

        return 1 

    def apply(self):

        self.result = self.results



