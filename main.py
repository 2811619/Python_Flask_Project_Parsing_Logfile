from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename

#UPLOAD_FOLDER = os.getcwd
UPLOAD_FOLDER = 'uploads_dir'

cwd = os.getcwd()

app = Flask(__name__)   
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.config["IMAGE_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads"
app.config["ALLOWED_TEXT_EXTENSIONS"] = ["TXT"]
# app.config["MAX_TEXT_FILESIZE"] = 0.5 * 1024 * 1024

def allowed_text(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_TEXT_EXTENSIONS"]:
        return True
    else:
        return False


# def allowed_text_filesize(filesize):

#     if int(filesize) <= app.config["MAX_TEXT_FILESIZE"]:
#         return True
#     else:
#         return False

@app.route("/")
@app.route("/upload-text-file", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            # if "filesize" in request.cookies:
				
                # if not allowed_text_filesize(request.cookies["filesize"]):
                #     print("Filesize exceeded maximum limit")
                #     return render_template("index.html")

                txt = request.files["txt"]

                if txt.filename == "":
                    print("No filename")
                    return render_template("index.html",outpu1 = 'No File Name')

                if allowed_text(txt.filename):
                    #filename = secure_filename(txt.filename)

                    #txt.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    txt.save(os.path.join(os.getcwd(),UPLOAD_FOLDER, txt.filename))
                    print(cwd)
                    #output = parserProgram(txt.save(os.path.join(app.config["UPLOAD_FOLDER"], filename)))
                    output = parserProgram(os.path.join(os.getcwd(),UPLOAD_FOLDER, txt.filename))
                    return render_template("index.html",output=output)

                else:
                    print("That file extension is not allowed")
                    return render_template("index.html")

    return render_template("index.html")

def parserProgram(txt) -> str:
	# opening the file with the name
	with open(txt, 'r') as file:
		logfile = file.read()
		#print (logfile)
		file.close()
  
		# Creating hours, minutes to calculate time taken and print the output
		hours = 0
		minutes = 0
		logfile = logfile.splitlines()
		#print (logfile)
  
		# Creating for loop for searching Line By Line
		for l in logfile:
		# Finding AM and PM in log file
			if 'am' in l or 'pm' in l:
				f = 0
				for i in range(len(l)):
					if f > 2:
						break
					# Spliting with using colon and get the start time
					if f == 0 and (l[i:i+2]=='am' or l[i:i+2] == 'pm'):
						start = l[i-5:i]
						#print (start)
						f += 1
					# Spliting with using colon and get the end time
					elif f == 1 and (l[i:i+2]=='am' or l[i:i+2] == 'pm'):
						end = l[i-5:i]
						#print (end)
						f += 1
					elif f == 2:
						minute_start = int(start[-2:])
						minute_end = int(end[-2:])
						hour_start = int(start[:2].strip())
						hour_end = int(end[:2].strip())
	
						minute = 0
						hour = 0

						if minute_start > minute_end:
							minute = 60 - (minute_start-minute_end)
							hour = hour - 1
						else:
							minute = minute_end - minute_start

						if hour_start > hour_end:
							hour = hour + (12 - (hour_start - hour_end))
						else:
							hour = hour + hour_end - hour_start
      
						# Hours = Hours+ Hour(Assignment operator to calculate the hours)
						hours += hour
						# Minutes = Minutes+ Minute (Assignment operator to add the minutes)
						minutes += minute

						f = 0
						break

		# Using assignment operator for changing minutes to hours
		hours += (minutes//60)
		# Using Mod to get the left over minutes
		minutes = (minutes%60)
		# Printing hours and minutes taken to complete the file
		print(hours,'hours', minutes,'minutes')

		return (str(hours) + ' hours'+','+ str(minutes) +' minutes')

if __name__ =='__main__':		
        app.run(debug=True)