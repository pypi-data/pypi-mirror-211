import os
import json
import season

config = wiz.model("portal/dizest/config")
fs = config.fs()

class Conda:
    def list(self):
        condapath = self.condapath
        condafs = season.util.os.FileSystem(condapath)
        envs = condafs.list("envs")
        res = []
        for env in envs:
            if env[0] == ".": continue
            if condafs.isdir(os.path.join("envs", env)):
                path = os.path.join("envs", env, "bin", "python")
                path = condafs.abspath(path)
                version = os.popen(path + " --version").read()
                version = version.replace("\n", " ").strip()
                res.append(dict(name=env, version=version, path=path))
        return res

    def create(self):
        condapath = self.condapath
        condacmd = self.condacmd
        name = wiz.request.query("name", True)
        python = wiz.request.query("python", True)
        os.system(f"{condacmd} create -n {name} python={python} -y")
        os.system(f"{condapath}/envs/{name}/bin/python -m pip install dizest")
        wiz.response.status(200)

    def remove(self):
        condacmd = self.condacmd
        name = wiz.request.query("name", True)
        os.system(f"{condacmd} env remove -n {name}")
        wiz.response.status(200)

    def __call__(self, segment):
        config = fs.read.json("config.json", dict(conda="conda"))
        if 'conda' not in config:
            wiz.response.status(404)

        self.condapath = config['conda']
        self.condacmd = os.path.join(config['conda'], "condabin", "conda")

        path = segment.path.split("/")
        if len(path) == 0:
            wiz.response.status(404)

        action = path[0]
        if hasattr(self, action):
            try:
                fn = getattr(self, action)
                res = fn()
            except Exception as e:
                wiz.response.status(500, e)
            wiz.response.status(200, res)

        wiz.response.status(404)

conda = Conda()

def load():
    config = fs.read.json("spec.json", [])
    wiz.response.status(200, config)

def update():
    data = wiz.request.query("data", True)
    data = json.loads(data)
    for i in range(len(data)):
        if 'conda' in data[i]:
            condaenv = data[i]['conda']
            data[i]['executable'] = f"/opt/anaconda3/envs/{condaenv}/bin/python"
    config = fs.write.json("spec.json", data)
    wiz.response.status(200)
