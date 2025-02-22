from flask import Flask, render_template, request, send_from_directory, make_response, redirect
import os

app = Flask(__name__, "/static","static")

@app.route('/path', methods=['GET'])
def render_path():
    root = "/config/workspace/dockermanager"
    subpath = request.args.get("path", root)  # Use request.args for GET requests
    by = request.args.get("by","")
    if "/.." in subpath or not root in subpath:
        return "canot acsess files beond threshold"
    print(subpath)  # Debugging

    if os.path.isdir(subpath):
        fullpath = subpath
        filelist = os.listdir(subpath)
        if subpath != root:
            out = [{"path": os.path.dirname(fullpath), "name": "Back","image":"icons/back.png"}]
        else:
            out = []
        for item in filelist:
            fpath = os.path.join(fullpath, item)  # Correct path joining
            if os.path.isdir(fpath):
                image = "icons/folder.png"
            else:
                image = "icons/file.png"
            out.append({"path": fpath, "name": item,"image":image})
        
        return render_template("file.html", files=out,subpath=subpath,by=by)
    else:
        return "Invalid path", 400

@app.route('/new', methods=['GET'])
def new():
    match request.args.get("type", False):
        case False:
            responce = make_response(render_template("newfile.html"))
            responce.set_cookie("dir",request.args.get("path", None))
            return responce
        case "container":
            return "wip"
        case "stack":
            return "wip"
        case "folder":
            return render_template("create/folder.html")


@app.route('/make', methods=['GET'])
def make():
    match request.args.get("type", False):
        case "Folder":
            print(request.cookies.get('dir'))
            os.makedirs(request.cookies.get('dir') + "/" + request.args.get("filename", False))

            return redirect(f"path?path={request.cookies.get('dir')}")
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060, debug=True)


