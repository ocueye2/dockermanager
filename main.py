from flask import Flask, render_template, request, send_from_directory, make_response, redirect
import os
import docker
import git

def makecontainerdir(dir,name,type):
    os.makedirs(os.path.join(dir,name))
    with open(os.path.join(dir,name,"subpath"),"w") as f:
        f.write("""

""")





app = Flask(__name__, "/static","static")

@app.route('/path', methods=['GET'])
def render_path():
    root = "E:\\workspace\\dockertest\\dockermanager\\containers"
    subpath = request.args.get("path", root)  # Use request.args for GET requests
    mode = request.args.get("mode", "view")
    by = request.args.get("by","")
    if "/.." in subpath or not root in subpath:
        return "canot acsess files beond threshold"
    print(subpath)  # Debugging
    if mode == "view":
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
                    if os.path.isfile(os.path.join(fpath,"sublink") )
                    image = "icons/folder.png"
                else:
                    image = "icons/file.png"
                out.append({"path": fpath, "name": item,"image":image})
            
            return render_template("file.html", files=out,subpath=subpath,by=by,mode="view")
        else:
            return "Invalid path", 400
    elif mode == "delete":
        return Exception
        

@app.route('/new', methods=['GET'])
def new():
    location = request.args.get("path", None)
    match request.args.get("type", False):
        case False:
            responce = make_response(render_template("newfile.html"))
            responce.set_cookie("dir",location)
            return responce
        case "container":
            match request.args.get("source", False):
                case "git":
                    return render_template("create/container/git.html")
                case False:
                    return render_template("create/container.html")
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
        case "container":
            match request.args.get("source", False):
                case "git":
                    os.makedirs(request.cookies.get('dir') + "/" + request.args.get("name", False))
                    git.Repo.clone_from(request.args.get("repo"), request.cookies.get('dir') + "/" + request.args.get("name", False))

                case "zip":
                    print("zip")
                    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8060, debug=True)


