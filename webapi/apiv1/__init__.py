import logging

from .resources import *

logger = logging.getLogger(__name__)


def configure_api_v1(api, auth, config):
    BASE = '/api/v1/'

    # dataset operations
    dataset_resource = DatasetResource()
    api.add_route(BASE + 'dataset', dataset_resource)
    api.add_route(BASE + 'dataset/{id}', dataset_resource)

    # list of datasets
    datasets_resource = DatasetsResource()
    api.add_route(BASE + 'datasets', datasets_resource)
    auth.optional_routes.append(BASE + 'datasets')

    dataset_full_resource = DatasetsFullResource()
    api.add_route(BASE + 'datasets/full', dataset_full_resource)
    auth.optional_routes.append(BASE + 'datasets/full')

    dataset_number_resource = DatasetsNumberResource()
    api.add_route(BASE + 'datasets/number', dataset_number_resource)
    auth.optional_routes.append(BASE + 'datasets/number')

    # architecture operations
    architecture_resource = ArchitectureResource()
    api.add_route(BASE + 'architecture', architecture_resource)
    api.add_route(BASE + 'architecture/{id}', architecture_resource)
    auth.optional_routes.append(BASE + 'architecture/{id}')

    # list of architectures
    architectures_resource = ArchitecturesResource()
    api.add_route(BASE + 'architectures', architectures_resource)
    auth.optional_routes.append(BASE + 'architectures')

    architectures_full_resource = ArchitecturesFullResource()
    api.add_route(BASE + 'architectures/full', architectures_full_resource)
    auth.optional_routes.append(BASE + 'architectures/full')

    architectures_number_resource = ArchitecturesNumberResource()
    api.add_route(BASE + 'architectures/number', architectures_number_resource)
    auth.optional_routes.append(BASE + 'architectures/number')

    # model operation
    model_resource = ModelResource()
    api.add_route(BASE + 'model', model_resource)
    api.add_route(BASE + 'model/{id}', model_resource)

    # train
    model_train_resource = ModelTrainResource()
    api.add_route(BASE + 'model/{id}/train', model_train_resource)

    model_train_status_resource = ModelTrainStatusResource()
    api.add_route(BASE + 'model/train/{tid}', model_train_status_resource)

    model_train_result_resource = ModelTrainResult()
    api.add_route(BASE + 'model/train/{tid}/history', model_train_result_resource)

    # test
    model_test_resource = ModelTestResource()
    api.add_route(BASE + 'model/{id}/test', model_test_resource)

    model_test_status_resource = ModelTestStatusResource()
    api.add_route(BASE + 'model/test/{tid}', model_test_status_resource)

    model_test_result_resource = ModelTestResult()
    api.add_route(BASE + 'model/test/{tid}/metrics', model_test_result_resource)

    # predict
    model_predict_resource = ModelPredictResource()
    api.add_route(BASE + 'model/{id}/predict', model_predict_resource)

    model_predict_status_resource = ModelPredictStatusResource()
    api.add_route(BASE + 'model/predict/{tid}', model_predict_status_resource)

    model_predict_result_resource = ModelPredictResult()
    api.add_route(BASE + 'model/predict/{tid}/result', model_predict_result_resource)

    # list of models
    models_resource = ModelsResource()
    api.add_route(BASE + 'models', models_resource)
    auth.optional_routes.append(BASE + 'models')

    models_full_resource = ModelsFullResource()
    api.add_route(BASE + 'models/full', models_full_resource)
    auth.optional_routes.append(BASE + 'models/full')

    models_number_resource = ModelsNumberResource()
    api.add_route(BASE + 'models/number', models_number_resource)
    auth.optional_routes.append(BASE + 'models/number')

    # task operation
    task_resource = TaskResource()
    api.add_route(BASE + 'task/{id}', task_resource)
    api.add_route(BASE + 'task', task_resource)

    # tasks list
    tasks_resource = TasksResource()
    api.add_route(BASE + 'tasks', tasks_resource)

    tasks_full_resource = TasksFullResource()
    api.add_route(BASE + 'tasks/full', tasks_full_resource)

    tasks_number_resource = TasksNumberResource()
    api.add_route(BASE + 'tasks/number', tasks_number_resource)

    # schema resource
    enable_new_layer = config.get('enable_new_layer', True)
    schema_model_layers_resource = SchemaModelLayersResource(enable_new_layer)
    api.add_route(BASE + 'schema/model/layers', schema_model_layers_resource)
    api.add_route(BASE + 'schema/layers', schema_model_layers_resource)  # TODO: delete line

    schema_dataset_resource = SchemaDatasetResource()
    api.add_route(BASE + 'schema/dataset', schema_dataset_resource)

    schema_architecture_resource = SchemaArchitectureResource()
    api.add_route(BASE + 'schema/architecture', schema_architecture_resource)

    schema_model_resource = SchemaModelResource()
    api.add_route(BASE + 'schema/model', schema_model_resource)

    schema_model_train_resource = SchemaModelTrainResource()
    api.add_route(BASE + 'schema/model/train', schema_model_train_resource)

    schema_model_test_resource = SchemaModelTestResource()
    api.add_route(BASE + 'schema/model/test', schema_model_test_resource)

    schema_model_predict_resource = SchemaModelPredictResource()
    api.add_route(BASE + 'schema/model/predict', schema_model_predict_resource)

    schema_task_resource = SchemaTaskResource()
    api.add_route(BASE + 'schema/task', schema_task_resource)

    logger.debug('api v1 initialized')
