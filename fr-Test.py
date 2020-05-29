
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import os
from recog import *

app = Flask(__name__)

# This is the path to the upload directory
#app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    json_result={}
   
    uploaded_files = request.files.getlist("file[]")
    output_file=request.form.get("output")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            
            # folder we setup
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            filenames.append(filename)
    #print(filenames)
    json_result,path=Recognize(filenames)
    #print(json_result)
            
    dep_dd = defaultdict(list)

    for filename,text in json_result.items():
        data=eval(text)
        result={}
        for res in data['analyzeResult']['documentResults']:
            result.update(res)
        dep_dd['FileName'].append(filename)
        for i in result['fields']:
            dep_dd[i].append(result['fields'][i]['text'])
    
    df=pd.DataFrame(dep_dd)
    df.to_csv(path+'\\{}.csv'.format(output_file),index=False)
    output_file=output_file+'.csv'
    return render_template('upload.html', filenames=filenames, output_file=output_file)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(path,filename)

if __name__ == '__main__':
    app.run(debug=True)