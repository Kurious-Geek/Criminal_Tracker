import tkinter as tk
import os
import csv
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
        self.resizable(width=True, height=True)

        self.taskbar_icon = tk.PhotoImage(file=ctracker_32)
        self.call('wm', 'iconphoto', self._w, self.taskbar_icon)

        #-- Shortcut keys --#

        self.bind_all("<Control-Key-s>", self.on_save)
        #self.bind_all("<Control-Key-n>", self.new_record)
        self.bind_all("<Control-Key-q>", self.close)
        self.bind_all("<Control-Shift-Key-S>", self.save_in_csv)

        self.inserted_rows = []
        self.updated_rows = []

                                    
        self.settings_model = m.SettingsModel()
        self.load_settings()

        style = ttk.Style()
        theme = self.settings.get('theme').get()
        if theme in style.theme_names():
            style.theme_use(theme)

        self.database_login()
        if not hasattr(self, 'data_model'):
            self.destroy()
            return
            
        self.callbacks = {'savein':self.save_in_csv,
                          'saveAF':lambda:self.on_save('arrest'),
                          'saveIF':lambda:self.on_save('incidence'),
                          'quit':self.close,
                          'clear':self.clear,
                          'show_recordlist':self.show_recordlist,
                          'on_open_record':self.open_record,
                          'on_open_irecord':self.open_irecord,
                          'new_record':self.open_record,
                          'new_irecord':self.open_irecord,
                          'searchAR': lambda:self.search_options('arrest'),
                          'searchIL': lambda:self.search_options('incidence'),
                          'show_incidence_list':self.show_incidence_list,
                          'violent_list':self.violent_list,
                          'on_open_vlist':self.open_vlist,
                          'crime_area':self.crime_areas,
                          #'extract_to_csv':self.extract_to_csv
                          
        }  

        #-- Menu --#

        menu = v.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu)

        #-- Arrest Form Tab --#
   
        self.tabs = ttk.Notebook(self)   
        self.tab1 = tk.Frame(self.tabs, bg='#008ae6')
        self.tabs.add(self.tab1, text='  Arrest Form  ')
        self.tabs.pack(expand=1, fill='both')

        self.canvas = tk.Canvas(self.tab1, width=970, height=600, highlightthickness=0, bg='#008ae6')
        yscrollbar = tk.Scrollbar(self.tab1, orient='vertical', command=self.canvas.yview)
        xscrollbar = tk.Scrollbar(self.tab1, orient='horizontal', command=self.canvas.xview)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL)))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        self.scrollable_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbound_to_mousewheel)

        self.scrollable_frame.config(bg='#008ae6')

        self.canvas.grid(row=0, column=0, sticky='NSEW')#, columnspan=2)
        yscrollbar.grid(row=0, column=3, sticky='NS', rowspan=2)
        xscrollbar.grid(row=1, column=0, sticky='EW', columnspan=2) 

        self.recordform = v.DataRecordForm(self.scrollable_frame, self.data_model.fields, self.settings, self.callbacks)
        self.recordform.grid(row=1, padx=10)

        drf = tk.Frame(self.tab1, bg='#008ae6')
        drf.grid(row=2, sticky=tk.W)

        self.status_label = tk.Label(drf, text= 'Status:', font=('Droid sans', 8), background='#008ae6', foreground='white')
        self.status_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.status = tk.StringVar()
        self.statusbar = tk.Label(drf, textvariable=self.status,  font=('Droid sans', 8), background='#008ae6', foreground='white')
        self.statusbar.grid(row=0, column=1, sticky=tk.W, padx=5)

        self.canvas.columnconfigure(0, weight=1)
        self.canvas.rowconfigure(0, weight=1)
    
        self.tab1.rowconfigure(0, weight=1)
        self.tab1.columnconfigure(0, weight=1)

        #-- Incidence Form Tab --#

        self.tab2 = tk.Frame(self.tabs, bg='#008ae6')
        self.tabs.add(self.tab2, text=' Incidence Form ')
        self.tabs.pack(expand=1, fill='both')

        self.incidence_form = v.IncidenceForm(self.tab2, self.data_model.fields1, self.settings, self.callbacks)
        self.incidence_form.grid(row=0, sticky='NSWE')
        
        frame = tk.Frame(self.tab2, bg='#008ae6')
        frame.grid(row=1, sticky=tk.W)

        self.ifstatus_label = tk.Label(frame, text= 'Status:', font=('Droid sans', 8), background='#008ae6', foreground='white')
        self.ifstatus_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.ifstatus = tk.StringVar()
        self.ifstatusbar = tk.Label(frame, textvariable=self.ifstatus,  font=('Droid sans', 8), background='#008ae6', foreground='white')
        self.ifstatusbar.grid(row=1, column=1, sticky=tk.W, padx=10)
        #self.incidence_form.tkraise()

        self.tab2.rowconfigure(0, weight=1)
        self.tab2.columnconfigure(0, weight=1)

        #-- Arrest Record Tab --#

        self.tab3 = tk.Frame(self.tabs)
        self.recordlist = v.RecordList(self.tab3, self.callbacks, self.inserted_rows, self.updated_rows)
        self.tab3.rowconfigure(0, weight=1)
        self.tab3.columnconfigure(0, weight=1)
        
        #-- Incidence Record Tab --#

        self.tab4 = tk.Frame(self.tabs)
        self.incidencelist = v.IncidenceList(self.tab4, self.callbacks, self.inserted_rows, self.updated_rows)
        self.tab4.rowconfigure(0, weight=1)
        self.tab4.columnconfigure(0, weight=1)

        self.records_saved = 0
        self.records_saved_to_csv = 0
        self.records_on_incidence_form_saved = 0

    def _bound_to_mousewheel(self, event):
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canvas.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
    def show_recordlist(self):
        self.tabs.add(self.tab3, text=' Arrest Record ')
        self.tabs.pack(expand=1, fill='both')
        self.recordlist.grid(row=0, sticky='NSWE')
        self.populate_recordlist()

    def show_incidence_list(self):
        self.tabs.add(self.tab4, text=' Incidence Record ')
        self.tabs.pack(expand=1, fill='both')
        self.incidencelist.grid(row=0, sticky='NSWE')
        self.populate_incidencelist()


    def on_save(self, form, event=None):

        if form == 'arrest':

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

        elif form == 'incidence':

            errors = self.incidence_form.get_errors()
            if errors:
                message = "Cannot Save Record"
                detail = "The following fields have errors: \n * {}".format('\n * '.join(errors.keys()))
                
                messagebox.showerror(title='Error', message=message, detail=detail)
                    
                return False

            data = self.incidence_form.get()
            rownum = self.incidence_form.current_record
            try:
                self.data_model.save_i_record(data)
            
            except Exception as e:
                messagebox.showerror(title='Error',
                                     message='Problem saving record',
                                     detail=str(e)
                )
            else:           
                self.records_on_if_saved += 1
                self.ifstatus.set(" *****{} record(s) saved in this session*****".format(self.records_on_incidence_form_saved))

            key = (data['CaseID'], data['Registration Date'])
            if self.data_model.last_write == 'update':
                self.updated_rows.append(key)
            else:
                self.inserted_rows.append(key)
            self.populate_incidencelist()
            if self.data_model.last_write == 'insert':
                self.incidence_form.reset()

    def save_in_csv(self, event=None):
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
        self.status.set("*****{} record(s) saved to csv in this session*****".format(self.records_saved_to_csv))
        self.recordform.reset()

    def close(self, event=None):
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

    def populate_incidencelist(self):
        try:
            rows = self.data_model.get_incidence_records()
        except Exception as e:
            messagebox.showerror(title='Error',
                                 message='Problem reading file',
                                 detail=str(e)
            )
        else:
            self.incidencelist.populate(rows)

    def open_record(self, rowkey=None):
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
        self.recordform.focus()

    def open_irecord(self, rowkey=None):
        if rowkey is None:
            record = None
        else:
            rowkey = rowkey
            try:
                record = self.data_model.get_irecord(*rowkey)
            except Exception as e:
                messagebox.showerror(title='Error',
                                     message='Problem reading file',
                                     detail=str(e)
                )
                return
        self.incidence_form.load_record(rowkey, record)
        self.incidence_form.focus()

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

    def search_options(self, type):
        self.type = type
        path='~'

        if self.type == 'arrest':

            title = 'Search Arrest Record'
            search_result = v.SearchDialog(self, title, self.type)

            if not search_result.result:
                error = 'Something went wrong'
            else:
                category, search_inp = search_result.result
                if category == "   --select--" and search_inp == '' or category == "   --select--" and search_inp == '{}'.format(search_inp) or category == '{}'.format(category) and search_inp == '':
                    messagebox.showerror(title='Input Error', message= 'Empty Field', detail='Select a value for Keyword and Category')
                else: 
                    try:
                        results = self.data_model.searchAR_query(category, search_inp)
                    except m.pg.OperationalError as e:
                        error = e

                        message = 'Database Error'
                        detail = error
                        messagebox.showerror(title='Search Error', message=message, detail=detail)
                    else:
                        if results == {}:
                            message = "Record not found"
                            detail = ("One of the following might have been the issue\n\n"
                                     "* Field(s) are case sensitive\n"
                                     "* Field(s) does not exist\n"
                                     )
                    
                            messagebox.showerror(title='Search Error', message=message, detail=detail)
                        else:
                            title = 'Search Result for "{}" by {}'.format(search_inp, category)

                            while True:

                                searchResult = v.SearchResult(self, results, self.type, title)
                                if not searchResult.result:
                                    break
                                else:
                                    data = searchResult.result
                                    datestring = datetime.today().strftime("%Y-%m-%d")
                                    self.filename = "search_result_for_'{}'_by_'{}'_on_{}.csv".format(search_inp, category, datestring)
                                    header = list(m.SQLModel.fields.keys())
                                    
                                    self.filepath = os.path.join(os.path.expanduser(path), self.filename)
                                    newfile = not os.path.exists(self.filepath)

                                    with open(self.filepath, 'a', newline='') as fh:
                                        csvwriter = csv.DictWriter(fh, fieldnames=header)
                                        if newfile:
                                            csvwriter.writeheader()
                                        writer = csv.writer(fh, dialect='excel')
                                        writer.writerows(data)
                                    break
            
        elif self.type == 'incidence':
            title = 'Search Incidence Record'
            search_result = v.SearchDialog(self, title, self.type)

            if not search_result.result:
                error = 'Something went wrong'
            else:
                category, search_inp = search_result.result
                if category == "   --select--" and search_inp == '' or category == "   --select--" and search_inp == '{}'.format(search_inp) or category == '{}'.format(category) and search_inp == '':
                    messagebox.showerror(title='Input Error', message= 'Empty Field', detail='Select a value for Keyword and Category')
                else: 
                    try:
                        results = self.data_model.searchIR_query(category, search_inp)
                    except m.pg.OperationalError as e:
                        error = e

                        message = 'Database'
                        detail = error
                        messagebox.showerror(title='Search Error', message=message, detail=detail)
                    else:
                        if results == {}:
                            message = "Record not found"
                            detail = ("One of the following might have been the issue\n\n"
                                     "* Field(s) are case sensitive\n"
                                     "* Field(s) does not exist\n"
                                     )
                    
                            messagebox.showerror(title='Search Error', message=message, detail=detail)
                        else:
                            title = 'Search Result for "{}" by {}'.format(search_inp, category)
                            
                        while True:
                            searchResult = v.SearchResult(self, results, self.type, title)
                            if not searchResult.result:
                                break
                            else:
                                data = searchResult.result
                                datestring = datetime.today().strftime("%Y-%m-%d")
                                self.filename = "search_result_for_'{}'_by_'{}'_on_{}.csv".format(search_inp, category, datestring)
                                header = list(m.SQLModel.fields1.keys())

                                self.filepath = os.path.join(os.path.expanduser(path), self.filename)
                                newfile = not os.path.exists(self.filepath)

                                with open(self.filepath, 'a', newline='') as fh:
                                    csvwriter = csv.DictWriter(fh, fieldnames=header)
                                    if newfile:
                                        csvwriter.writeheader()
                                    writer = csv.writer(fh, dialect='excel')
                                    writer.writerows(data)
                                break

    def violent_list(self):
        path='~'
        try:
            results = self.data_model.sort_violent()
        except m.pg.OperationalError as e:
            error = e
            messagebox.showerror(title='Error', message='Database Error', detail=error)
        else:
            if results == {}:
                message = "No Record Here"
                detail = ("Record of violent inmates seems to be empty \n"
                          "must have something to do with the database")
        
                messagebox.showinfo(title='Violent Inmates', message=message, detail=detail)
            else:
                title = 'Violent Inmates'
                while True:
                    violent_inmates_list = v.ViolentList(self, self.callbacks, results, title)
                    if not violent_inmates_list.result:
                        break
                    else:
                        data = violent_inmates_list.result
                        datestring = datetime.today().strftime("%Y-%m-%d")
                        self.filename = "violent_inmates_record_{}.csv".format(datestring)
                        header = list(violent_inmates_list.column_defs.keys())[1:]
                        
                        self.filepath = os.path.join(os.path.expanduser(path), self.filename)
                        newfile = not os.path.exists(self.filepath)


                        with open(self.filepath, 'a', newline='') as fh:
                            csvwriter = csv.DictWriter(fh, fieldnames=header)
                            if newfile:
                                csvwriter.writeheader()
                            writer = csv.writer(fh, dialect='excel')
                            writer.writerows(data)
                        break

    def open_vlist(self, rowkey=None):
        if rowkey is None:
            record = None
        else:
            rowkey = rowkey
            try:
                record = self.data_model.get_violent_data(*rowkey)
            except Exception as e:
                messagebox.showerror(title='Error',
                                     message='Problem reading file',
                                     detail=str(e)
                )
                return
        title = 'Data of Selected Inmate'
        violent_data = v.ViolentData(self, record, title)

    def crime_areas(self):
        try:
            results = self.data_model.sort_crime_areas()
        except m.pg.OperationalError as e:
            error = e
            messagebox.showerror(title='Error', message='Database Error', detail=error)
        else:
            if results == {}:
                message = "No Record Here"
                detail = ("Record of crime occuring areas seems to be empty \n"
                          "must have something to do with the database")
        
                messagebox.showinfo(title='Crime Occuring Areas', message=message, detail=detail)
            else:
                title = 'Crime Occuring Areas'  
                while True:
                    crime_occuring_area = v.CrimeArea(self, self.callbacks, results, title)
                    if not crime_occuring_area.result:
                        break
                    else:
                        data = crime_occuring_area.result
                        datestring = datetime.today().strftime("%Y-%m-%d")
                        self.filename = "crime_occuring_areas_record_{}.csv".format(datestring)
                        header = list(crime_occuring_area.column_defs.keys())[1:]

                        path='~'
                        self.filepath = os.path.join(os.path.expanduser(path), self.filename)
                        newfile = not os.path.exists(self.filepath)


                        with open(self.filepath, 'a', newline='') as fh:
                            csvwriter = csv.DictWriter(fh, fieldnames=header)
                            if newfile:
                                csvwriter.writeheader()
                            writer = csv.writer(fh, dialect='excel')
                            writer.writerows(data)
                        break


                
