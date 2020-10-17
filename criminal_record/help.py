class Details:
	details = (
		'Criminal Tracker is a prototype of a data entry software \n'
		'this app works on POSTGRESQL database, for now the databse configurations are done manually \n\n'

		'***before running the app for the first time do the database configuration***\n'
		'   ***but if you are reading this from the app then you should ignore***\n\n'

		'~ Database configuration: \n'
		'	* download and install postgres software \n'
		'	* create a database on the software and name it "criminal_record" \n'
		'	  Alternative: (if you are a developer and you already have a database you are working with, \n' 
		'	  locate the "models.py" file in the directory of installation of this app, \n'
		'	  locate the settings model class and edit it according to your database configuration)\n'
		'	* in the installation directory locate the directory "sql/create_db.sql" and \n' 
		'	  run the script on your databsse query tool \n'
		'	* your application is good to go \n\n'

		'~ Menu bar: \n\n'
		'	Menu bar contains regular menu bar options \n\n'
		'	* File: \n' 
		'		New Arrest Form: this resets the widgets of the arrest record tab to start a new record \n'
		'		New Incidence Form: this resets the widgets of the incidence record tab to start a new record \n'
		'		Save Arrest Form: this saves the data of the arrest form to the database \n'
		'		Save Incidence Form: this saves the data of the incidence form to the database \n'
		'		Save in CSV: this saves the records to a csv file \n'
		'		Exit: Exit the app \n\n'

		'	* Options: \n'
		'		Autofill Date: when ticked it auto fills the "date of registration" column with the current date \n'
		'		Font size: for changing the size of the font for the app for better visualization \n'
		'		Themes: for changing themes of the app "it only contains windows native themes" \n'
		'	 	and the changes only takes effect after restart. \n\n'

		'	* View: \n'
		'		Arrest Record: this creates a tab that shows all records saved \n'
		'	 	from arrest form in the database on some selected columns. \n'
		'		Incidence Record: this creates a tab that shows complete records saved from incidence form in the database. \n'
		'		Violent Inmates: this creates a window that shows the names and case numbers of violent inmates. \n'
		'	 	when a record is selected by double clicking it opens the complete record of the selected field. \n'
		'		Crime Occuring Area: this creates a window that shows arrest areas and their corresponding case numbers.\n\n'

		'	* Search: \n'
		'		Search Arrest Record: this searches for keywords by selected categories these categories are \n'
		'	 	columns on the "data_record_view" which is the arrest record in the database. \n'
		'		Search Incidence Record: this searches for keywords by selected categories these categories are \n'
		'		columns on the "incidence_view" which is the incidence record in the database. \n\n'
			
		'~ Error Handling: \n\n'
		'	* App window can be resized \n'
		'	* Cannot Save Record: this is due to the fact that one or more fields are empty or are field with wrong syntax \n'
		'	* problem saving record: this is due to database error or as stated in the error details \n'
		'	* record not found: this is due to error in search parameters orempty search result \n\n'

		'~ Saving data: \n\n'
		'	* Data can be saved in csv format manually. \n'
		'	* Data is saved to database by default. \n'
		'	* Windows with Extract to csv buttons can extract their records to a csv file \n'

	)