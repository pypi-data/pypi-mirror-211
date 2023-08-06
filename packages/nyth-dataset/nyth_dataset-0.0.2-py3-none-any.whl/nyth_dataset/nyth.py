import os
import json
import pandas as pd
import pickle
from .utils import get_text_between_entities

import logging

logger = logging.getLogger('nyt_dataset')
logger.setLevel(logging.DEBUG)


class NYTHDataset:

    def __init__(self, data_dir, include_na_relation=True):
        self.data_dir = data_dir
        self.rel2id = json.loads(open(os.path.join(data_dir, 'rel2id.json')).read())
        self.id2rel = {val: key for key, val in self.rel2id.items()}

        self.bag_label2id = json.loads(open(os.path.join(data_dir, 'bag_label2id.json')).read())
        self.id2bag_label = {val: key for key, val in self.bag_label2id.items()}

        self.include_na_relation = include_na_relation
        self.train = None
        self.test = None
        self.dev = None

    def get_data(self):
        if self.train is None:
            raise Exception("You must load the data first (load_data function)")
        return self.train, self.dev, self.test

    def _load_data(self, datafile, set_type, reload):
        if os.path.exists(os.path.join(self.data_dir, set_type + '.pkl')) and not reload:
            data = pickle.load(open(os.path.join(self.data_dir, set_type + '.pkl'), 'rb'))
        else:
            path = os.path.join(self.data_dir, datafile)
            data = []
            with open(path, "rt", encoding="utf-8") as fin:
                for line in fin:
                    ins = json.loads(line.strip())
                    if not self.include_na_relation and self.rel2id[ins['relation']] == 0:
                        continue
                    btw = get_text_between_entities(sentence=ins['sentence'],
                                                    entity_1=ins['head']['word'],
                                                    entity_2=ins['tail']['word'],
                                                    )
                    data.append({
                        'instance_id': ins['instance_id'],
                        'bag_id': ins['bag_id'],
                        'sentence': ins['sentence'],
                        'e1_name': ins['head']['word'],
                        'e1_type': ins['head']['type'],
                        'e2_name': ins['tail']['word'],
                        'e2_type': ins['tail']['type'],
                        'relation': self.rel2id[ins['relation']],
                        'bag_label': self.bag_label2id[ins['bag_label']],
                        'noisy': 0 if self.bag_label2id[ins['bag_label']] == 1 else 1 if self.bag_label2id[ins[
                            'bag_label']] == 0 else 2,
                        'text_between_entities_including_them': btw[0],
                        'text_between_entities': btw[1]
                    })
            pickle.dump(data, open(os.path.join(self.data_dir, set_type + '.pkl'), 'wb+'))
        return data

    def load_data(self, reload=False):
        self.train = pd.DataFrame(
            columns=['instance_id', 'bag_id', 'sentence', 'text_between_entities_including_them',
                     'text_between_entities', 'e1_name', 'e1_type', 'e2_name',
                     'e2_type', 'relation', 'bag_label', 'noisy'])
        self.dev = pd.DataFrame(
            columns=['instance_id', 'bag_id', 'sentence', 'text_between_entities_including_them',
                     'text_between_entities', 'e1_name', 'e1_type', 'e2_name',
                     'e2_type', 'relation', 'bag_label', 'noisy'])
        self.test = pd.DataFrame(
            columns=['instance_id', 'bag_id', 'sentence', 'text_between_entities_including_them',
                     'text_between_entities', 'e1_name', 'e1_type', 'e2_name',
                     'e2_type', 'relation', 'bag_label', 'noisy'])

        logger.info('--------------------------------------')
        logger.info('start to load data ...')
        logger.info('test data ...')
        test_dataset = self._load_data('test.json', 'test', reload=reload)
        self.test = pd.concat([self.test, pd.DataFrame.from_records(test_dataset)])
        logger.info(f'len of test: {len(test_dataset)}')

        logger.info('dev data ...')
        dev_dataset = self._load_data('dev.json', 'dev', reload=reload)
        self.dev = pd.concat([self.dev, pd.DataFrame.from_records(dev_dataset)])
        logger.info(f'len of dev: {len(dev_dataset)}')

        logger.info('train data ...')
        train_dataset = self._load_data('train.json', 'train', reload=reload)
        self.train = pd.concat([self.train, pd.DataFrame.from_records(train_dataset)])
        logger.info(f'len of train: {len(train_dataset)}')
        logger.info('finished !')
        logger.info('--------------------------------------')
