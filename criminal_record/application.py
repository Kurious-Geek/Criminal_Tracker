import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
from . import views as v
from . import models as m
from .images import ctracker_32
from .images import ctracker_64
from tkinter.font import nametofont


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Criminal Tracker')
        self.resizable(width=False, height=True)

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        # Shortcut keys
        self.bind_all("<Control-Key-s>", self.on_save)
        self.bind_all("<Control-Key-n>", self.open_record)

        self.inserted_rows = []
        self.updated_rows = []

        #self.filename = tk.StringVar(value=default_filename)
                                    
        self.settings_model = m.SettingsModel()
        self.load_settings()

        self.database_login()
        if not hasattr(self, 'data_model'):
            self.destroy()
            return

        style = ttk.Style()
        theme = self.settings.get('theme').get()
        if theme in style.theme_names():
            style.theme_use(theme)
            
        self.callbacks = {'file->savein':self.save_in_csv,
                          'file->save':self.on_save,
                          'save':self.on_save,
                          'file->quit':self.close,
                          'clear':self.clear,
                          'show_recordlist':self.show_recordlist,
                          'on_open_record':self.open_record,
                          'new_record':self.open_record,
                          'search': self.search_options
                          
        }  

        menu = v.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu)

        #-- Tabs --#
        
        self.tabs = ttk.Notebook(self)
        self.tab1 = tk.Frame(self.tabs, bg='#008ae6')
        self.tab2 = tk.Frame(self.tabs)

        self.tabs.add(self.tab1, text='  Home  ')
        self.tabs.pack(expand=1, fill='both')

        #-- canvas --#

        self.canvas = tk.Canvas(self.tab1, width=985, height=600, highlightthickness=0, bg='#008ae6')
        yscrollbar = tk.Scrollbar(self.tab1, orient='vertical', command=self.canvas.yview)
        xscrollbar = tk.Scrollbar(self.tab1, orient='horizontal', command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.scrollable_frame.config(bg='#008ae6')

        self.canvas.grid(row=0, column=0, sticky='NSEW', columnspan=2)
        yscrollbar.grid(row=0, column=3, sticky='NS', rowspan=2, columnspan=2)
        xscrollbar.grid(row=1, column=0, sticky='EW', columnspan=2) 
        
        self.recordform = v.DataRecordForm(self.scrollable_frame, self.data_model.fields, self.settings, self.callbacks)
        self.recordform.grid(row=1, padx=10)

        #self.recordlist = v.RecordList(self.tab2, self.callbacks, self.inserted_rows, self.updated_rows)

        #-- status bar --#

        self.status_label = tk.Label(self.tab1, text= 'Status:', font=('Droid sans', 7), background='#008ae6', foreground='white')
        self.status_label.grid(row=3, column=0, sticky=tk.W, pady=4)
        
        self.status = tk.StringVar()
        self.statusbar = tk.Label(self.tab1, textvariable=self.status, background='#008ae6', foreground='white')
        self.statusbar.grid(sticky=tk.W, row=3, column=1, padx=5)

        self.records_saved = 0
        self.records_saved_to_csv = 0

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self,event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
    def show_recordlist(self):
        self.tabs.add(self.tab2, text=' Criminal List ')
        self.tabs.pack(expand=1, fill='both')
        self.recordlist = v.RecordList(self.tab2, self.callbacks, self.inserted_rows, self.updated_rows)
        self.recordlist.grid(row=0, sticky='W')
        self.recordlist.tkraise()
        self.populate_recordlist()

    def on_save(self, event=None):

        errors = self.recordform.get_errors()
        if errors:
            message = "Cannot Save Record"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            
            messagebox.showerror(title='Error', message=message, detail=detail)
                
            return False

        data = self.recordform.get()
        rownum = self.recordform.current_record
        try:
            self.data_model.save_record(data)
        
        except Exception as e:
            messagebox.showerror(title='Error',
                                 message='Problem saving record',
                                 detail=str(e)
            )
        else:           
            self.records_saved += 1
            self.status.set(" *****{} record(s) saved in this session*****".format(self.records_saved))

        key = (data['Case Number'], data['Date of Registration'])
        if self.data_model.last_write == 'update':
            self.updated_rows.append(key)
        else:
            self.inserted_rows.append(key)
        self.populate_recordlist()
        if self.data_model.last_write == 'insert':
            self.recordform.reset()


    def save_in_csv(self):
        errors = self.recordform.get_errors()
        if errors:
            message = "Cannot Save record"
            detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
            
            messagebox.showerror(title='Error', message=message, detail=detail)
                
            return False

        datestring = datetime.today().strftime("%Y-%m-%d")
        default_filename = "criminal_record_{}.csv".format(datestring)
        self.filename = tk.StringVar(value=default_filename)
        filename = self.filename.get()
        model = m.CSVModel(filename)
        data = self.recordform.get()
        model.save_record(data)     
                    
        self.records_saved_to_csv += 1
        self.status.set("*****{} record(s) saved to csv in this session".format(self.records_saved_to_csv))
        self.recordform.reset()
        '''filename = filedialog.asksaveasfilename(
            title='Select the file for saving records',
            defaultextension='csv',
            filetypes=[('Comma-Separated Values (csv)', '*.csv *.CSV')]
        )
        if filename:
            self.filename.set(filename)
            self.data_model = m.CSVModel(filename=self.filename.get())
            '''



    def close(self):
        self.quit()
        self.destroy()
        exit()
        
    def load_settings(self):
        vartypes = {
            'bool':tk.BooleanVar,
            'str':tk.StringVar,
            'int':tk.IntVar,
            'float':tk.DoubleVar
        }

        self.settings = {}
        
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        for var in self.settings.values():
            var.trace('w', self.save_settings)

        self.set_font()
        self.settings['font size'].trace('w', self.set_font)

    def save_settings(self, *args):
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

    def clear(self):
        self.recordform.reset()

    def populate_recordlist(self):
        try:
            rows = self.data_model.get_all_records()
        except Exception as e:
            messagebox.showerror(title='Error',
                                 message='Problem reading file',
                                 detail=str(e)
            )
        else:
            self.recordlist.populate(rows)

    def open_record(self, rowkey=None, event=None):
        if rowkey is None:
            record = None
        else:
            rowkey = rowkey
            try:
                record = self.data_model.get_record(*rowkey)
            except Exception as e:
                messagebox.showerror(title='Error',
                                     message='Problem reading file',
                                     detail=str(e)
                )
                return
        self.recordform.load_record(rowkey, record)
        self.recordform.tkraise()

    def set_font(self, *args):
        font_size = self.settings['font size'].get()
        font_names = ('TkDefaultFont', 'TkMenuFont', 'TkTextFont')
        for font_name in font_names:
            tk_font = nametofont(font_name)
            tk_font.config(size=font_size)
            
    def database_login(self):
        error = ''
        db_host = self.settings['db_host'].get()
        db_name = self.settings['db_name'].get()
        title = 'Login to {} at {}'.format(db_name, db_host)

        while True:
            login = v.LoginDialog(self, title, error)
            if not login.result:
                break
            else:
                username, password = login.result
                try:
                    self.data_model = m.SQLModel(
                        db_host, db_name, username, password)
                except m.pg.OperationalError:
                    error = "Login Failed"
                else:
                    break

    def search_options(self):
        error = ''
        db_name = self.settings['db_name'].get()
        title = 'Search {} database'.format(db_name)

        search_result = v.SearchDialog(self, title, error)
        if not search_result.result:
            error = 'Something went wrong'
        else:
            category, search_inp = search_result.result
            if category == "   --select--" and search_inp == '' or category == "   --select--" and search_inp == '{}'.format(search_inp) or category == '{}'.format(category) and search_inp == '':
                messagebox.showerror(title='Input Error', message= 'Empty Field', detail='Select a value for Keyword and Category')
            else: 
                try:
                    results = self.data_model.search_query(category, search_inp)
                except m.pg.OperationalError as e:
                    error = e
                else:
                    if results == {}:
                        message = error if error else "Record not found"
                        detail = ("One of the following might have been the issue\n\n"
                                 "* Field(s) are case sensitive\n"
                                 "* Field(s) does not exist\n"
                                 )
                
                        messagebox.showerror(title='Error', message=message, detail=detail)
                    else:
                        title = 'Search Result for "{}" by {}'.format(search_inp, category)
                        #v.SearchResult(self, title).searchview_populate(results)
                        v.SearchResult(self, title)
                        

                
                
