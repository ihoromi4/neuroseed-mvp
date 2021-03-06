import uuid

from mongoengine import Document, EmbeddedDocument
from mongoengine import fields
from mongoengine.queryset.visitor import Q

from .mixin import MetadataMixin
from .errors import ResourcePublishedException

__all__ = [
    'DatasetMetadata',
    'get_dataset',
    'update_dataset',
    'delete_dataset',
    'get_datasets'
]


PENDING = 'PENDING'
RECEIVED = 'RECEIVED'
FAILURE = 'FAILURE'
PUBLISHED = 'PUBLISHED'

DATASET_STATUS_CODES = [
    PENDING,
    RECEIVED,
    FAILURE,
    PUBLISHED
]

CLASSIFICATION = 'classification'
REGRESSION = 'regression'

DATASET_CATEGORIES = [
    CLASSIFICATION,
    REGRESSION
]


class DatasetBase(EmbeddedDocument):
    owner = fields.StringField(required=True)
    hash = fields.StringField()
    size = fields.LongField()
    date = fields.LongField()
    title = fields.StringField(required=True)
    description = fields.StringField()
    category = fields.StringField(choices=DATASET_CATEGORIES)
    labels = fields.ListField(fields.StringField())
    shape = fields.ListField(fields.IntField())


class DatasetMetadata(Document, MetadataMixin):
    id = fields.StringField(primary_key=True, default=lambda: str(uuid.uuid4()))
    url = fields.StringField()
    status = fields.StringField(default=PENDING, choices=DATASET_STATUS_CODES, required=True)
    is_public = fields.BooleanField(default=False)
    hash = fields.StringField()
    base = fields.EmbeddedDocumentField(DatasetBase, default=lambda: DatasetBase())

    meta = {
        'allow_inheritance': True,
        'db_alias': 'metadata',
        'collection': 'datasets'
    }

    def __init__(self, *args, **kwargs):
        flatten = None
        if 'flatten' in kwargs:
            flatten = kwargs['flatten']
            del kwargs['flatten']

        super().__init__(*args, **kwargs)

        if flatten:
            self.from_flatten(flatten)

        self.url = self.id

    def flatten(self):
        """Return dataset in flatten representation"""

        meta = self.to_mongo().to_dict()

        if '_id' in meta:
            meta['id'] = meta['_id']
            del meta['_id']

        meta.update(meta['base'])
        del meta['base']
        del meta['_cls']

        return meta

    to_dict = flatten

    def from_flatten(self, meta):
        """Restore dataset metadata from flatten representation"""

        for name in self._fields:
            if not name is 'base' and name in meta:
                setattr(self, name, meta[name])

        for name in self.base._fields:
            if name in meta:
                setattr(self.base, name, meta[name])

    from_dict = from_flatten


def get_dataset(id, context):
    if not isinstance(id, str):
        raise TypeError('Type of id must be str')

    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = Q(id=id) & (Q(base__owner=user_id) | Q(is_public=True))
        meta = DatasetMetadata.from_id(query)
    else:
        kwargs = {'id': id, 'is_public': True}
        meta = DatasetMetadata.from_id(**kwargs)

    return meta


def update_dataset(dataset, data, context=None):
    """Delete dataset by id or directly
    Args:
        dataset (str or DatasetMetadata): dataset to delete
        data (dict): update fields data
        context (None or dict): context for delete
        
    Returns:
        None
        
    Raises:
        TypeError - invalid argument type
        DoesNotExist - dataset does not exist
        KeyError - context not contain user_id key
        ValueError - invalid access rights
    """

    if not isinstance(dataset, (str, DatasetMetadata)):
        raise TypeError('type of dataset must be str or DatasetMetadata')

    if not isinstance(data, dict):
        raise TypeError('type of data must be dict')

    if not isinstance(context, (dict, type(None))):
        raise TypeError('type of context must be dict or None')

    if isinstance(dataset, str):
        if isinstance(context, type(None)):
            raise ValueError('to access to dataset need user_id')

        user_id = context.get('user_id', None)

        if user_id:
            query = Q(id=dataset) & Q(base__owner=user_id)
            dataset = DatasetMetadata.from_id(query)
        else:
            raise KeyError('context must contain user_id key')

    with dataset.save_context():
        dataset.from_flatten(data)


def delete_dataset(dataset, context=None):
    """Delete dataset by id or directly
    Args:
        dataset (str or DatasetMetadata): dataset to delete
        context (None or dict): context for delete
        
    Returns:
        None
        
    Raises:
        TypeError - invalid argument type
        DoesNotExist - dataset does not exist
        KeyError - context not contain user_id key
        ValueError - invalid access rights
        ResourcePublishedException - can not delete published dataset
    """

    if not isinstance(dataset, (str, DatasetMetadata)):
        raise TypeError('Type of dataset must be str or DatasetMetadata')

    if not isinstance(context, (dict, type(None))):
        raise TypeError('Type of context must be dict or None')

    if isinstance(dataset, str):
        if isinstance(context, type(None)):
            raise ValueError('to access to dataset need user_id')

        user_id = context.get('user_id', None)

        if user_id:
            query = Q(id=dataset) & Q(base__owner=user_id)
            dataset = DatasetMetadata.from_id(query)
        else:
            raise KeyError('context must contain user_id key')

    if dataset.status == PUBLISHED:
        raise ResourcePublishedException('can not delete published dataset')

    dataset.delete()


def get_datasets(context, filter=None):
    if not isinstance(context, dict):
        raise TypeError('Type of context must be dict')

    if not isinstance(filter, (dict, type(None))):
        raise TypeError('Type of context must be dict')

    query = Q(is_public=True)

    if 'user_id' in context and context['user_id']:
        user_id = context['user_id']
        query = query | (Q(is_public=False) & Q(base__owner=user_id))

    metas = DatasetMetadata.objects(query)

    if filter:
        if 'from' in filter:
            from_ = filter['from']
            metas = metas.skip(from_)

        if 'number' in filter:
            number = filter['number']
            metas = metas.limit(number)

    return metas
