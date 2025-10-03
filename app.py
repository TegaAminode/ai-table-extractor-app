from flask import Flask,render_template,request,flash,send_file
import extractor
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'tega_secret_key'

@app.errorhandler(404)
def page_not_found(error):
    return "Error 404",404

@app.route("/", methods=['GET','POST'])
def file_upload():
    if request.method == 'POST':
       file = request.files['file']
       file.save(f"{secure_filename(file.filename)}")
       output_message = extractor.main(file.filename)
       if output_message:
            flash(output_message)
            #download(f)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)