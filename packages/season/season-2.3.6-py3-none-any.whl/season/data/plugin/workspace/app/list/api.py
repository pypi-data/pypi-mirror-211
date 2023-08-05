import git as Git
import os
import zipfile
import tempfile
import time
import shutil
import datetime
import json
import season

def controllers():
    fs = wiz.workspace("service").fs("src", "controller")
    res = []
    try:
        ctrls = fs.list()
        for ctrl in ctrls:
            if fs.isfile(ctrl) and os.path.splitext(ctrl)[-1] == ".py":
                res.append(ctrl[:-3])
    except:
        pass

    wiz.response.status(200, res)

def list():
    res = []
    try:
        workspace = wiz.workspace("service")
        working_dir = wiz.server.path.branch
        fs = workspace.fs(os.path.join(working_dir))

        projects = wiz.branch.list()
        for project in projects:
            info = fs.read.json(os.path.join(project, "wiz.project"), dict())
            info['id'] = project
            res.append(info)
    except:
        pass
    wiz.response.status(200, res)

def create():
    fs = season.util.os.FileSystem(wiz.server.path.branch)
    path = wiz.request.query("path", True)
    ptype = wiz.request.query("type", True)

    if fs.exists(path):
        wiz.response.status(400)

    target_path = fs.abspath(path)

    if ptype == 'copy':
        target = wiz.request.query("target", True)
        fs.copy(target, path)
        wiz.response.status(200)
    elif ptype == 'upload':
        files = wiz.request.files()
        if len(files) == 0:
            wiz.response.status(404)
        files = files[0]
        zippath = os.path.join(tempfile.gettempdir(), 'wizproject', datetime.datetime.now().strftime("%Y%m%d"), str(int(time.time())), files.filename)
        unzippath = fs.abspath(path)
        fs.write.file(zippath, files)
        zipfile.ZipFile(zippath).extractall(unzippath)
    elif ptype == 'git':
        giturl = wiz.request.query("git", True)
        Git.Repo.clone_from(giturl, fs.abspath(path))
    else:
        copyfs = wiz.workspace("ide").fs(os.path.join(season.PATH_LIB, "data"))
        copyfs.copy("sample", target_path)

    if fs.exists(path) == False:
        wiz.response.status(404)

    if fs.exists(os.path.join(path, "config")) == False:
        fs.makedirs(os.path.join(path, "config"))

    current_branch = wiz.branch()
    wiz.branch(path)

    builder = wiz.model("workspace/builder")
    builder.clean()
    builder.build()
    wiz.branch(current_branch)

    wiz.response.status(200)

def git():
    workspace = wiz.workspace("service")
    working_dir = wiz.server.path.branch
    fs = workspace.fs(os.path.join(working_dir))

    path = wiz.request.query("path", True)
    target_path = fs.abspath(os.path.join(path))
    try:
        Git.Repo.init(target_path)
    except:
        pass

    wiz.response.status(200)

def data():
    workspace = wiz.workspace("service")
    working_dir = wiz.server.path.branch
    fs = workspace.fs(os.path.join(working_dir))

    path = wiz.request.query("path", True)
    text = fs.read(path, "")
    wiz.response.status(200, text)

def update():
    workspace = wiz.workspace("service")
    working_dir = wiz.server.path.branch
    fs = workspace.fs(os.path.join(working_dir))
    
    path = wiz.request.query("path", True)
    data = wiz.request.query("data", True)
    fs.write(path, data)
    wiz.response.status(200)