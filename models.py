from datetime import datetime
from config import db, ma


class BucketListItem(db.Model):
    __tablename__ = "bucket_list_item"
    item_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=True)
    description = db.Column(db.String(255))
    completed = db.Column(db.Boolean)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class BucketListItemSchema(ma.ModelSchema):
    class Meta:
        model = BucketListItem
        sqla_session = db.session
