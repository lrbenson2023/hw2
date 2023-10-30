from flask import Flask, flash, render_template, request, redirect, url_for, session
import os


# Defining upload folder path
UPLOAD_FOLDER = os.path.join('static', 'images')

# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder='templates', static_folder='static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "your_secret_key"
 
@app.route("/")
def index():
	if len(session) == 0:
		return render_template("login.html", dataToRender="Please sign in")
	else:
		return redirect(url_for("homepage"))

@app.route("/homepage_action",methods = ["POST","GET"])
def homepage_action():
	if request.method == "POST":
	# save entry or image
		wtext = request.form.get("Text")
		wimage = request.form.get("Image")
		inputtext = request.form["inputtext"]
		blogfile = open("blog.txt","a") #append mode
		if wtext is not None:
			if inputtext == "": # if there is no new entry go back to the homepage
				blogfile.close()
				return redirect(url_for("homepage"))
			else:
				blogfile.write(inputtext + "\n")
		elif wimage is not None:
			fname = uploadFile()
			if fname:
				blogfile.write(fname + "\n")
		blogfile.close()
	return redirect(url_for("homepage")) # was just homepage()

def uploadFile():
	# check if the post request has the file part
	if 'uploaded-file' not in request.files:
		flash('No file part')
		return False
	file = request.files['uploaded-file']
	# if user does not select file, browser also
	# submit an empty part without filename
	if file.filename == '':
		flash('No selected file')
		return False
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
	return file.filename

#convert users and passwords to a dictionary
def convert(userslist):
	users_dict = {}
	for i in range(0, len(userslist), 2):
		users_dict[userslist[i]] = userslist[i + 1]
		print(userslist)
	print(users_dict)
	return users_dict

@app.route("/homepage")
def homepage():
	webpage = '''
	<html> 
	<head>
	<title>Home</title>
	</head>
	<body>
	<p style='text-align:left;'>
	<h1>Welcome to the TECH 136 blog by LAM
	<span style='float:right;'>
	Username:{uname}
	<a href= {lout}>
	Logout</a></h1></span></p>
	<form action = 'homepage_action' method = 'post' enctype=multipart/form-data>
	Enter your comment here:
	<br>
	<textarea id='inputtext' name='inputtext' rows='2' cols='100'></textarea>
	<br>
	<button type="submit" name="Text">Post Text</button>
	<input type="file" id="myFile" name="uploaded-file">
	<button type="submit" name="Image">Post Image</button>
	</form>
	<br>
	'''.format(uname=session["username"],lout = url_for("logout") )
       
	with open("blog.txt","a+") as blogfile:
		blogfile.seek(0)
		blog =  blogfile.read().rstrip()
	blogfile.close()
	bloglist = blog.split("\n")
	for i in range(len(bloglist) -1,-1,-1):
		if bloglist[i].endswith(('png', 'jpg', 'gif')):
			image = os.path.join(app.config['UPLOAD_FOLDER'], bloglist[i])
			webpage += '''
			<br>
			<img src= "{user_image}" alt= "Img not found" width="200" height="200">
			'''.format(user_image = image)
		else:
			webpage += '''
			<br>
			<textarea id = {tid1} name= {tid2} rows='2' cols='100'>
			{blist}
			</textarea>
			'''.format(tid1 = 'blogtext' + str(i), tid2 = 'blogtext' + str(i), blist= bloglist[i])
	return webpage


@app.route("/signup_action",methods = ["POST","GET"])
def signup_action():
	if request.form.get("Submit") == "Submit":
		print("got submit")
	else:
		print(request.form.get("Submit"))
	if request.method == "POST":
		return render_template("signup.html")
	else:
		return render_template("login.html", dataToRender="I had some trouble with that, Please try again")
		
@app.route("/get_info",methods = ["POST","GET"])
def get_info():
	if request.method == "POST":
		username = request.form["user"]
		password = request.form["psword"]

		usersfile = open("users.txt","a") #append mode
		usersfile.write(username + "\t" + password + "\n")
		usersfile.close()

	return render_template("login.html", dataToRender="Thank You for signing up to our blog. Please sign in")

@app.route("/login_action",methods = ["POST","GET"])
def login_action():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		# check user id against the users.txt file, create it if it doesn't exist
		with open("users.txt","a+") as usersfile:
			usersfile.seek(0) #go to head of the file
			users =  usersfile.read().rstrip()
		usersfile.close()
		userslist = users.split()

		users_dict = convert(userslist) # convert users and passwords to a dictionary
		print(users_dict)
		if users_dict.get(username) == password:
		# Correct username and password match
				session["username"] = username
				return redirect(url_for("homepage"))
		else:
		# Incorrect username/password match
			return render_template("login.html", dataToRender="I cannot find that user info. Please use the Signup button")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return render_template("login.html", dataToRender="Thank You for using our blog")

# main driver function
if __name__ == "__main__":

        # run() method of Flask class runs the application
        # on the local development server.
        app.run(host="0.0.0.0",port=5000)
