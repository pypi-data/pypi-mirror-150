import json
import logging
import os
from typing import Dict, Union, Text, Optional, NoReturn, List

from termgraph import termgraph as tg

from dime_xai.shared.constants import (
    DEFAULT_PERSIST_PATH,
    DEFAULT_PERSIST_FILE,
    DEFAULT_PERSIST_EXTENSION,
    DEFAULT_DIME_EXPLANATION_BASE_KEYS,
    DEFAULT_DIME_EXPLANATION_DATA_KEYS,
    DEFAULT_DIME_EXPLANATION_MODEL_KEYS,
    DEFAULT_DIME_EXPLANATION_DIME_KEYS,
    DEFAULT_DIME_EXPLANATION_TIMESTAMP_KEYS,
    DEFAULT_DIME_EXPLANATION_CONFIG_KEYS,
    DEFAULT_DIME_EXPLANATION_NGRAMS_KEYS,
    OUTPUT_MODE_GLOBAL, OUTPUT_MODE_LOCAL,
    OUTPUT_MODE_DIME,
)
from dime_xai.shared.exceptions.dime_core_exceptions import (
    InvalidDIMEExplanationFilePath,
    DIMEExplanationFileLoadException,
    DIMEExplanationDirectoryException,
    DIMEExplanationFileExistsException,
    DIMEExplanationFilePersistException,
    InvalidDIMEExplanationStructure,
)
from dime_xai.utils.io import (
    file_exists,
    get_timestamp_str,
    dir_exists,
)

logger = logging.getLogger(__name__)


class DIMEExplanation:
    def __init__(self, explanation: Union[Dict, Text]):
        if isinstance(explanation, Text):
            full_file_path = os.path.join(DEFAULT_PERSIST_PATH, explanation)
            if not file_exists(full_file_path):
                raise InvalidDIMEExplanationFilePath(f"The provided explanation file name is invalid. "
                                                     f"Make sure that it is available in the "
                                                     f"dime_explanations directory")

            self.file_name = explanation

            try:
                with open(full_file_path, encoding='utf8', mode='r') as file:
                    self.explanation = json.load(file)
            except Exception as e:
                raise DIMEExplanationFileLoadException(f"Error occurred while reading "
                                                       f"the explanation file specified. {e}")
        else:
            self.file_name = DEFAULT_PERSIST_FILE + "_" + \
                             get_timestamp_str(sep="_") + \
                             DEFAULT_PERSIST_EXTENSION
            self.explanation = explanation

        if not self._validate():
            raise InvalidDIMEExplanationStructure(f"The structure of the provided DIME "
                                                  f"explanation file is invalid.")

    def persist(
            self,
            name: Text = None,
            overwrite: bool = False
    ) -> Optional[Text]:
        if not dir_exists(DEFAULT_PERSIST_PATH):
            logger.warning("The default explanation directory does not exist. "
                           "A new directory will be created to persist the "
                           "DIME explanations.")
            try:
                os.mkdir(DEFAULT_PERSIST_PATH)
            except OSError:
                raise DIMEExplanationDirectoryException(f"Error occurred while attempting "
                                                        f"to create the explanations "
                                                        f"directory")

        if not name:
            name = self.file_name

        full_file_path = os.path.join(
            DEFAULT_PERSIST_PATH,
            name
        )

        if file_exists(full_file_path):
            if overwrite:
                logger.warning("A file with the same name is available in the specified "
                               "location and will be overwritten.")
            else:
                raise DIMEExplanationFileExistsException("A file with the same name is "
                                                         "available in the specified "
                                                         "location. Explanations will not "
                                                         "be persisted.")

        try:
            with open(full_file_path, encoding='utf8', mode='w') as file:
                json.dump(self.explanation, file, indent=4, ensure_ascii=False)

            logger.info(f"DIME explanations were persisted in dime_explanations directory under "
                        f"{self.file_name}")
            return self.file_name

        except Exception as e:
            raise DIMEExplanationFilePersistException(f"Failed to persist "
                                                      f"DIME explanations in "
                                                      f"the given destination: "
                                                      f"{full_file_path}. {e}")

    def _validate(self) -> bool:
        for key in list(self.explanation.keys()):
            if key not in DEFAULT_DIME_EXPLANATION_BASE_KEYS:
                return False

        for key in list(self.explanation['data'].keys()):
            if key not in DEFAULT_DIME_EXPLANATION_DATA_KEYS:
                return False

        for key in list(self.explanation['model'].keys()):
            if key not in DEFAULT_DIME_EXPLANATION_MODEL_KEYS:
                return False

        for key in list(self.explanation['timestamp'].keys()):
            if key not in DEFAULT_DIME_EXPLANATION_TIMESTAMP_KEYS:
                return False

        for key in list(self.explanation['config'].keys()):
            if key not in DEFAULT_DIME_EXPLANATION_CONFIG_KEYS:
                return False

        if isinstance(self.explanation['config']['ngrams'], Dict):
            for key in list(self.explanation['ngrams'].keys()):
                if key not in DEFAULT_DIME_EXPLANATION_NGRAMS_KEYS:
                    return False

        if self.explanation['config']['output_mode'] == OUTPUT_MODE_DIME:
            for key in DEFAULT_DIME_EXPLANATION_DIME_KEYS:
                for instance in self.explanation['dime']:
                    if key not in instance:
                        return False

        return True

    def inspect(self) -> NoReturn:
        exp_json = json.dumps(self.explanation, indent=4, ensure_ascii=False).encode('utf8')
        print(f"\nDIME Explanations [Raw]: \n\n{exp_json.decode()}\n")

    @staticmethod
    def _visualize_cli(
            title: Text,
            description: Text,
            labels: List,
            data: List[List],
            width: int = 50,
            color: int = 97,
    ) -> NoReturn:
        print(f"\n{title}\n")
        print(f"{description}\n") if description else None
        normal_data = tg.normalize(data, width=width)
        len_cats = 1
        args = {'filename': '', 'title': '', 'width': width,
                'format': '{:<}', 'suffix': '', 'no_labels': False,
                'color': None, 'vertical': True, 'stacked': False,
                'different_scale': False, 'calendar': False,
                'start_dt': None, 'custom_tick': '', 'delim': '',
                'verbose': False, 'version': False}
        colors = [color]
        tg.stacked_graph(labels=labels, data=data, normal_data=normal_data,
                         len_categories=len_cats, colors=colors, args=args)

    def visualize(self, token_limit: int = None) -> NoReturn:
        output_mode = self.explanation['config']['output_mode']

        if output_mode == OUTPUT_MODE_GLOBAL:
            if token_limit is None:
                logger.warning(f"The token limit has not been specified and was "
                               f"set to 10. To visualize global feature importance of "
                               f"all tokens, specify '--limit' as 0")
                token_limit = 10
            elif token_limit == 0:
                logger.warning(f"Token limit will be ignored and all tokens "
                               f"will be visualized")

            max_token_limit = len(self.explanation['global']['softmax_score'].keys())
            if token_limit > max_token_limit or token_limit == 0:
                token_limit = max_token_limit

            title = f"GLOBAL FEATURE IMPORTANCE SCORES"
            description = f"Explanation Type: {self.explanation['config']['output_mode']}\n" \
                          f"Case Sensitive: {self.explanation['config']['case_sensitive']}\n" \
                          f"Global Metric: {self.explanation['config']['global_metric']}\n" \
                          f"N-grams: {self.explanation['config']['ngrams']}\n"
            labels = list(self.explanation['global']['softmax_score'].keys())[0:token_limit]
            data = [[score] for score
                    in list(self.explanation['global']['softmax_score'].values())[0:token_limit]]
            DIMEExplanation._visualize_cli(
                title=title,
                description=description,
                labels=labels,
                data=data,
            )

        elif output_mode == OUTPUT_MODE_LOCAL:
            if token_limit:
                logger.warning(f"Token limit specified will be ignored "
                               f"while visualizing Local and DIME explanations")

            for instance in self.explanation['local']:
                print(f"\n\tDATA INSTANCE: {instance['instance']}\n")
                pass  # TODO :visualize local tokens

        elif output_mode == OUTPUT_MODE_DIME:
            if token_limit:
                logger.warning(f"Token limit specified will be ignored "
                               f"while visualizing Local and DIME explanations")

            for instance in self.explanation['dime']:
                title = f"DIME SCORES\nDATA INSTANCE: {instance['instance']}"
                description = f"Explanation Type: {self.explanation['config']['output_mode']}\n" \
                              f"Case Sensitive: {self.explanation['config']['case_sensitive']}\n" \
                              f"Global Metric: {self.explanation['config']['global_metric']}\n" \
                              f"N-grams: {self.explanation['config']['ngrams']}\n" \
                              f"Ranking Length: {self.explanation['config']['ranking_length']}"
                labels = list(instance['global']['softmax_score'].keys())
                data = [[score] for score in list(instance['global']['softmax_score'].values())]
                DIMEExplanation._visualize_cli(
                    title=title,
                    description=description,
                    labels=labels,
                    data=data,
                )
        else:
            logger.error(f"The output_mode specified for the explanation "
                         f"is invalid. Could not visualize the given DIME "
                         f"explanation")
