import peewee as pw
base = wiz.model("portal/season/orm").cls("base/dizest")

class Model(base):
    class Meta:
        db_table = 'workflow'

    id = pw.CharField(primary_key=True, max_length=16)
    user_id = pw.CharField(index=True, max_length=32)
    title = pw.CharField(index=True, max_length=96)
    version = pw.CharField(index=True, max_length=24)
    visibility = pw.CharField(index=True, max_length=16)
    category = pw.CharField(index=True, max_length=32)
    favorite = pw.CharField(index=True, max_length=1)
    created = pw.DateTimeField(index=True)
    updated = pw.DateTimeField(index=True)
    
    logo = base.TextField()
    featured = base.TextField()
    description = base.TextField()

    apps = base.JSONObject()
    flow = base.JSONObject()
    extra = base.JSONObject()
