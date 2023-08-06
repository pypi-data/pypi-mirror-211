from flask import Response
import requests
import pypugjs
from pypugjs.ext import jinja
import sass

fs = wiz.workspace().fs("src/assets")
jquery = fs.read("jquery.js")

HEADJS = '''
<script type="text/javascript">
let _log = console.log;

let Style = {
    base: [
        "color: #fff",
        "background-color: #444",
        "padding: 2px 4px",
        "border-radius: 2px"
    ],
    warning: [
        "color: #eee",
        "background-color: red"
    ],
    success: [
        "background-color: green"
    ]
}

console.log = function() {
    let style = Style.base.join(';') + ';';
    style += Style.base.join(';');
    _log(`%cdizest.js`, style, ...arguments);
}

window.API = (()=> {
    let obj = {};
    obj.url = (fnname)=> "{url}/" + fnname;
    obj.async = obj.function = obj.call = async(fnname, data, opts = {})=> {
        let _url = obj.url(fnname);
        
        let ajax = {
            url: _url,
            type: "POST",
            data: data,
            ...opts
        };

        return new Promise((resolve) => {
            $.ajax(ajax).always(function (a, b, c) {
                resolve(a, b, c);
            });
        });
    };
    return obj;
})();
</script>
'''

def getKernel(**kwargs):
    config = wiz.model("portal/dizest/config")
    KernelClass = wiz.model("portal/dizest/kernel")
    kernel = KernelClass.getInstance(config.kernel_id(**kwargs))
    if kernel is None:
        wiz.response.status(401)
    return kernel

def render(segment):
    segment = segment.path.split("/")
    namespace = segment[0]
    workflow_id = segment[1]
    flow_id = segment[2]
    kernel_id = wiz.request.query("kernel_id", None)

    kernel = getKernel(kernel_id=kernel_id)
    workflow = kernel.workflow(workflow_id)

    wfdata = workflow.get(workflow_id)
    if wfdata is None:
        wiz.response.abort(404)

    app_id = wfdata['flow'][flow_id]['app_id']
    app = wfdata['apps'][app_id]

    def app_get(key, default=None):
        try:
            if app[key] is not None:
                return app[key]
        except:
            pass
        return default

    url = "/".join(wiz.request.uri().split("/")[:4] + ['api', namespace, flow_id])
    headjs = HEADJS.replace('{url}', url)

    pugconfig = dict()
    pugconfig['variable_start_string'] = '{[#$'
    pugconfig['variable_end_string'] = '$#]}'

    pug = app_get("pug", "")

    if len(pug) == 0:
        wiz.response.abort(404)

    pug = pypugjs.Parser(pug)
    pug = pug.parse()
    pug = jinja.Compiler(pug, **pugconfig).compile()

    head = app_get("head", "")
    if len(head) > 0:
        head = pypugjs.Parser(head)
        head = head.parse()
        head = jinja.Compiler(head, **pugconfig).compile()

    js = app_get("js", "")
    js = jquery + "\n" + js
    if js is None or len(js) == 0:
        js = ""
    else:
        js = f"<script type='text/javascript'>{js}</script>"

    css = app_get("css")
    try:
        css = sass.compile(string=css)
        css = str(css)
        css = f"<style>{css}</style>"
    except Exception as e:
        css = ""

    view = f"<!DOCTYPE html><html><head>{head}{headjs}{css}</head><body>{pug}{js}</body></html>"
    wiz.response.send(view, content_type="text/html")

def api(segment):
    segment = segment.path.split("/")
    namespace = segment[0]
    flow_id = segment[1]
    fnname = "/".join(segment[2:])
    kernel_id = wiz.request.query("kernel_id", None)

    kernel = getKernel(kernel_id=kernel_id)

    kernel_uri = kernel.uri()
    request = wiz.request.request()

    kwargs = dict(
        method=request.method,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.values,
        cookies=request.cookies,
        files=request.files)

    kwargs["url"] = kernel_uri + "/flow/api/" + namespace + "/" + flow_id + "/" + fnname
    kwargs["allow_redirects"] = False
    
    resp = requests.request(**kwargs)
    
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    
    wiz.response.response(response)