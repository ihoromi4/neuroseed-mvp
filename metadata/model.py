from mongoengine import Document, EmbeddedDocument
from mongoengine import fields

from .dataset import DatasetMetadata
from .architecture import ArchitectureMetadata

__all__ = [
    'ModelMetadata'
]

PENDING = 1
INITIALIZE = 2
TRAINING = 3
TESTING = 4
READY = 5


class ModelBase(EmbeddedDocument):
    owner = fields.StringField(required=True)
    hash = fields.StringField()
    size = fields.LongField()
    date = fields.LongField()
    title = fields.StringField(required=True)
    description = fields.StringField()
    category = fields.StringField()
    labels = fields.ListField(field=fields.StringField())
    accuracy = fields.FloatField()
    architecture = fields.ReferenceField(ArchitectureMetadata, required=True)
    dataset = fields.ReferenceField(DatasetMetadata)
    # TODO: parent = fields.ReferenceField(Model)
    shape = fields.ListField(field=fields.IntField())


class ModelMetadata(Document):
    id = fields.StringField(primary_key=True)
    url = fields.StringField()
    status = fields.IntField(default=PENDING)
    is_public = fields.BooleanField(default=False)
    hash = fields.StringField()
    base_init = lambda: ModelBase()
    base = fields.EmbeddedDocumentField(ModelBase, default=base_init)

    meta = {
        'db_alias': 'metadata',
        'collection': 'models'
    }
