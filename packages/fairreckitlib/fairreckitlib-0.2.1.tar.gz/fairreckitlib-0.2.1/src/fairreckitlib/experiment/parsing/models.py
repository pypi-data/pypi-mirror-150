"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from fairreckitlib.events import config_event
from fairreckitlib.experiment.parsing import assertion
from fairreckitlib.pipelines.model.pipeline import ModelConfig
from ..constants import EXP_KEY_MODELS
from ..constants import EXP_KEY_MODEL_NAME
from ..constants import EXP_KEY_MODEL_PARAMS
from .params import parse_config_parameters


def parse_models_config(experiment_config, model_factory, event_dispatcher):
    """Parses all model configurations.

    Args:
        experiment_config(dict): the experiment's total configuration.
        model_factory(ModelFactory): the model factory containing the available models.
        event_dispatcher(EventDispatcher): to dispatch the parse event on failure.

    Returns:
        parsed_config(dict): dictionary of parsed ModelConfig's keyed by API name.
    """
    parsed_config = {}

    # assert EXP_KEY_MODELS is present
    if not assertion.is_key_in_dict(
        EXP_KEY_MODELS,
        experiment_config,
        event_dispatcher,
        'PARSE ERROR: missing experiment key \'' + EXP_KEY_MODELS + '\' (required)',
        default=parsed_config
    ): return parsed_config

    models_config = experiment_config[EXP_KEY_MODELS]

    # assert models_config is a dict
    if not assertion.is_type(
        models_config,
        dict,
        event_dispatcher,
        'PARSE ERROR: invalid experiment value for key \'' + EXP_KEY_MODELS + '\'',
        default=parsed_config
    ): return parsed_config

    # assert models_config has entries
    if not assertion.is_container_not_empty(
        models_config,
        event_dispatcher,
        'PARSE ERROR: experiment \'' + EXP_KEY_MODELS + '\' is empty',
        default=parsed_config
    ): return parsed_config

    # parse models_config entries
    for api_name, models in models_config.items():
        # attempt to parse a list of ModelConfig's for this API
        api_config = parse_api_models(
            api_name,
            models,
            model_factory,
            event_dispatcher
        )

        # skip when no configurations are actually parsed
        if not assertion.is_container_not_empty(
            api_config,
            event_dispatcher,
            'PARSE WARNING: skipping models for API: ' + api_name
        ): continue

        parsed_config[api_name] = api_config

    return parsed_config


def parse_api_models(api_name, model_configs, model_factory, event_dispatcher):
    """Parses the model configurations for the specified API name.

    Args:
        api_name(str): name of the API that will be parsed.
        model_configs(array like): list of model configurations.
        model_factory(ModelFactory): the model factory containing the available models.
        event_dispatcher(EventDispatcher): to dispatch the parse event on failure.

    Returns:
        parsed_models(array like): list of parsed ModelConfig's.
    """
    parsed_models = []

    # assert API is available in the model factory
    if not assertion.is_one_of_list(
        api_name,
        model_factory.get_available_api_names(),
        event_dispatcher,
        'PARSE WARNING: unknown model API \'' + api_name + '\''
    ): return parsed_models

    # assert models is a list
    if not assertion.is_type(
        model_configs,
        list,
        event_dispatcher,
        'PARSE WARNING: invalid models value for API \'' + api_name + '\'',
        default=parsed_models
    ): return parsed_models

    # assert models has list entries
    if not assertion.is_container_not_empty(
        model_configs,
        event_dispatcher,
        'PARSE WARNING: models for API \'' + api_name + '\' is empty'
    ): return parsed_models

    # parse models list entries
    for _, algo_config in enumerate(model_configs):
        model, model_name = parse_model(
            algo_config,
            model_factory.get_algorithm_factory(api_name),
            event_dispatcher
        )
        # skip on failure
        if model is None:
            event_dispatcher.dispatch(
                config_event.ON_PARSE,
                msg='PARSE WARNING: failed to parse model \'' + str(model_name) + '\', skipping...'
            )
            continue

        parsed_models.append(model)

    return parsed_models


def parse_model(model_config, algo_factory, event_dispatcher):
    """Parses the model configuration.

    Args:
        model_config(dict): dictionary with the model's configuration.
        algo_factory(AlgorithmFactory): the algorithm factory related to the model config.
        event_dispatcher(EventDispatcher): to dispatch the parse event on failure.

    Returns:
        parsed_config(ModelConfig): the parsed configuration or None on failure.
        model_name(str): the name of the parsed model or None on failure.
    """
    # assert model_config is a dict
    if not assertion.is_type(
        model_config,
        dict,
        event_dispatcher,
        'PARSE ERROR: ' + algo_factory.get_api_name() +
        ' model invalid value'
    ): return None, None

    # assert model name is present
    if not assertion.is_key_in_dict(
        EXP_KEY_MODEL_NAME,
        model_config,
        event_dispatcher,
        'PARSE ERROR: ' + algo_factory.get_api_name() +
        ' model missing key \'' + EXP_KEY_MODEL_NAME + '\''
    ): return None, None

    model_name = model_config[EXP_KEY_MODEL_NAME]

    # assert model name is available in the algorithm factory
    if not assertion.is_one_of_list(
        model_name,
        algo_factory.get_available_algorithm_names(),
        event_dispatcher,
        'PARSE ERROR: ' + algo_factory.get_api_name() +
        ' model unknown name: \'' + str(model_name) + '\''
    ): return None, model_name

    algo_params = algo_factory.get_algorithm_params(model_name)
    model_params = algo_params.get_defaults()

    # assert EXP_KEY_MODEL_PARAMS is present
    # skip when the model has no parameters at all
    if len(model_params) > 0 and assertion.is_key_in_dict(
        EXP_KEY_MODEL_PARAMS,
        model_config,
        event_dispatcher,
        'PARSE WARNING: model ' + model_name + ' missing key \'' + EXP_KEY_MODEL_PARAMS + '\'',
        default=model_params
    ):
        # parse the model parameters
        model_params = parse_config_parameters(
            model_config[EXP_KEY_MODEL_PARAMS],
            model_name,
            algo_params,
            event_dispatcher
        )

    parsed_config = ModelConfig(
        model_name,
        model_params
    )

    return parsed_config, model_name
