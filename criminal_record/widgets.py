import tkinter as tk
from tkinter import ttk
from datetime import datetime
from .constants import FieldTypes as FT



class ValidatedMixin:
    
    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var=None or tk.StringVar()
        super().__init__(*args, **kwargs)
        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.config(validate='all',
                    validatecommand=(vcmd,'%P', '%s','%S', '%V', '%i', '%d'),
                    invalidcommand=(invcmd,'%P', '%s','%S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.config(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        self._toggle_error(False)
        self.error.set('')
        valid = True
        if event =='focusout':
            valid  = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(proposed=proposed, current=current, char=char, event=event, index=index, action=action)
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(proposed=proposed, current=current, char=char, event=event, index=index, action=action)
        
    def _focusout_invalid(self, **kwargs):
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid
          
class RequiredEntry(ValidatedMixin, ttk.Entry):
    
    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('*A value is required*')
        return valid

class DateEntry(ValidatedMixin, ttk.Entry):

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0':
            valid = True
        elif index in ('0', '1', '2', '3', '5', '6','8', '9'):
            valid = char.isdigit()
        elif index in ('4', '7'):
            valid = char == '-'
        else:
            valid = False
        return valid

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            self.error.set('*A value is required*')
            valid = False
        try:
            datetime.strptime(self.get(), '%Y-%m-%d')
        except ValueError:
            self.error.set('*Invalid Date*')
            valid = False
        return valid

class ValidatedCombobox(ValidatedMixin, ttk.Combobox):

    def _key_validate(self, proposed, action, **kwargs):
        valid = True

        if action == '0':
            self.set('')
            return True
        
        values = self.cget('values')
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.set(matching[0])
            self.icursor(tk.END)
            valid = False
        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set('*A value is required*')
        return valid



class LabelInput(tk.Frame):

    field_types = {
        FT.string: (RequiredEntry, tk.StringVar),
        FT.string_list: (ValidatedCombobox, tk.StringVar),
        FT.iso_date_string: (DateEntry, tk.StringVar),
        FT.long_string: (tk.Text, lambda: None),
        FT.integer: (RequiredEntry, tk.IntVar),
        FT.boolean: (ttk.Checkbutton, tk.BooleanVar),
    }

        
    def __init__(self, parent, label='', input_class=None, input_var=None, input_args=None, label_args=None, field_spec=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        input_args = input_args or {}
        label_args = label_args or {} 

        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)[0]
            var_type = self.field_types.get(field_type)[1]
            self.variable = input_var if input_var else var_type()
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')
            if 'width' in field_spec and 'width' not in input_args:
                input_args['width'] = field_spec.get('width')
            if 'height' in field_spec and 'height' not in input_args:
                input_args['height'] = field_spec.get('height')
        else:
            self.variable = input_var
        
        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = self.variable
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=tk.W, pady=3, padx=5)
            input_args["textvariable"] = self.variable
            

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=tk.W, padx=5, pady=3, columnspan=3)

        self.error = getattr(self.input, 'error', tk.StringVar())
        self.error_label = ttk.Label(self, textvariable=self.error, background='#008ae6', foreground='red')
        self.error_label.grid(row=2, column=0, sticky=(tk.W+tk.E), columnspan=3)
                              
   
    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        elif type(self.input) == tk.Combobox:
            self.input.current(0)
        else:
            self.input.delete('0', tk.END)
            self.input.insert('0', value)
