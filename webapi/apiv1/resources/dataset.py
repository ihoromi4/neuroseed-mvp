import logging
import uuid
import cgi

import falcon
from falcon.media.validators import jsonschema

import metadata
import manager
from ..schema.dataset import DATASET_SCHEMA, CREATE_DATASET_SCHEMA

__all__ = [
    'DatasetResource'
]

logger = logging.getLogger(__name__)

MAX_DATASET_SIZE = 1 * 10**9  # in bytes


class DatasetResource:
    auth = {
        'optional_methods': ['GET']
    }

    def on_get(self, req, resp, id=None):
        if id:
            self.get_dataset_meta(req, resp, id)
        else:
            self.get_description(req, resp)

    def get_dataset_meta(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            dataset_meta = manager.get_dataset(id, context)
        except metadata.DoesNotExist:
            logger.debug('Dataset {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )

        resp.status = falcon.HTTP_200
        dataset_meta_dict = dataset_meta.to_dict()
        result_keys = ['id', 'status', 'is_public', 'owner', 'hash', 'size', 'date', 'title', 'description', 'category', 'labels']
        resp.media = {key: dataset_meta_dict[key] for key in result_keys if key in dataset_meta_dict}
    
    def get_description(self, req, resp):
        raise falcon.HTTPNotFound(
            title="Dataset not found",
            description="Dataset metadata does not exist"
        )

    def on_post(self, req, resp, id=None):
        if id:
            self.upload_dataset(req, resp, id)
        else:
            self.create_dataset_meta(req, resp)

    def save_dataset(self, req, resp, dataset_meta):
        """
        Multipart dataset upload        
        """

        if req.content_length > MAX_DATASET_SIZE:
            raise falcon.HTTPRequestEntityTooLarge(
                title="Dataset is too large",
                description="Dataset size must be less than {size} bytes".format(size=MAX_DATASET_SIZE)
            )

        env = req.env
        env.setdefault('QUERY_STRING', '')

        form = cgi.FieldStorage(fp=req.stream, environ=env)

        file_item = form['file']
        if file_item.file:
            file = file_item.file

            try:
                manager.save_dataset(dataset_meta, file)
            except OSError as err:
                raise falcon.HTTPUnsupportedMediaType(
                    description="Can not open dataset. Invalid type."
                )
            except KeyError as err:
                raise falcon.HTTPUnsupportedMediaType(
                    description="Dataset has not 'x' or 'y' keys"
                )
        else:
            logger.debug('Multipart not contain file item')

            raise falcon.HTTPUnsupportedMediaType(
                description="Multipart must contain 'file' field"
            )

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': dataset_meta.id,
            'date': dataset_meta.base.date,
            'size': dataset_meta.base.size,
            'hash': dataset_meta.base.hash
        }

    def dataset_already_uploaded(self, req, resp, id):
        logger.debug('Dataset {id} alerady uploaded'.format(id=id))

        raise falcon.HTTPMethodNotAllowed(
            title="Method Not Allowed",
            description="Dataset already uploaded")

    def upload_dataset(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            dataset_meta = manager.get_dataset(id, context)
        except metadata.DoesNotExist:
            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )

        if dataset_meta.status == metadata.dataset.PENDING:
            self.save_dataset(req, resp, dataset_meta)
        elif dataset_meta.status == metadata.dataset.RECEIVED:
            self.dataset_already_uploaded(req, resp, id)

    @jsonschema.validate(CREATE_DATASET_SCHEMA)
    def create_dataset_meta(self, req, resp):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        with metadata.DatasetMetadata().save_context() as dataset_meta:
            dataset_meta.from_flatten(req.media)
            dataset_meta.id = str(uuid.uuid4())
            dataset_meta.url = dataset_meta.id
            dataset_meta.base.owner = user_id

        logger.debug('User {uid} create dataset {did}'.format(uid=user_id, did=dataset_meta.id))

        resp.status = falcon.HTTP_200
        resp.media = {
            'id': dataset_meta.id
        }

    @jsonschema.validate(DATASET_SCHEMA)
    def on_patch(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            manager.update_dataset(id, data=req.media, context=context)
        except metadata.DoesNotExist:
            logger.debug('Dataset {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )

        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, id):
        user_id = req.context['user']
        logger.debug('Authorize user {id}'.format(id=user_id))

        try:
            context = {'user_id': user_id}
            manager.delete_dataset(id, context)
        except metadata.DoesNotExist:
            logger.debug('Dataset {id} does not exist'.format(id=id))

            raise falcon.HTTPNotFound(
                title="Dataset not found",
                description="Dataset metadata does not exist"
            )
        except metadata.errors.ResourcePublishedException:
            raise falcon.HTTPConflict(
                title='Dataset already published',
                description='Can not delete dataset. Dataset already published on blockchain'
            )

        resp.status = falcon.HTTP_200
