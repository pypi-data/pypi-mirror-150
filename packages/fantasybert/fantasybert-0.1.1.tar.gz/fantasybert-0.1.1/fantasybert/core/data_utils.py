import torch
from torch.utils.data import Dataset
from itertools import chain
from torch.utils.data.dataloader import _SingleProcessDataLoaderIter, _MultiProcessingDataLoaderIter
from torch.utils.data import DataLoader
from torch.utils.data import Sampler, SequentialSampler
import random, abc
from typing import Union


class DataSetGetter(Dataset):
    def __init__(self, file_path=None, datas=None):
        if isinstance(file_path, (str, list)):
            self.datas, self.total_labels = self.load_data(file_path)
        elif isinstance(datas, list):
            self.datas = datas
        else:
            raise ValueError('The input args shall be str format file_path / list format datas')
        print(f'Num samples of {file_path} is {len(self.datas)}')

    def __len__(self):
        return len(self.datas)

    def __getitem__(self, idx):
        return self.datas[idx]

    @staticmethod
    def load_data(file_path):
        return file_path

    @property
    def data(self):
        return self.datas

    @property
    def num_labels(self):
        return len(list(set(self.total_labels))) if self.total_labels is not None and self.total_labels != [] else None

    @property
    def label2id(self):
        return {l:i for i,l in enumerate(sorted(list(set(self.total_labels))))}\
            if self.total_labels is not None and self.total_labels != [] else None

    @property
    def id2label(self):
        return {i:l for i,l in enumerate(sorted(list(set(self.total_labels))))}\
            if self.total_labels is not None and self.total_labels != [] else None

    @property
    def labels_distribution(self):
        if self.total_labels is not None and self.total_labels != []:
            labels_dic = {}
            for label in self.total_labels:
                labels_dic[label] = labels_dic.get(label, 0) + 1
            total_num = sum(list(labels_dic.values()))
            label_distribution = dict((x, round((y/total_num)*100, 3)) for x, y in labels_dic.items())
            sorted_label_distribution = dict(sorted(label_distribution.items(), key=lambda x: -float(x[1])))
            final_label_distribution = {k: str(v) + '%' for k, v in sorted_label_distribution.items()}
            return final_label_distribution
        else:
            return None


class BatchIter(DataLoader):
    def __init__(self,
                 dataset: Union[DataSetGetter, Dataset],
                 sort_bs_num=None,
                 sort_key=None,
                 use_block_shuffle: bool = False,
                 batch_in_shuffle: bool = False,
                 batch_size=1, sampler=None,
                 num_workers=0, pin_memory=False, drop_last=False,
                 timeout=0, worker_init_fn=None, collate_fn=None,
                 batch_sampler=None, shuffle=False,
                 **kwargs,
                 ):
        batch_sampler = batch_sampler
        if batch_sampler is not None:
            kwargs['batch_size'] = 1
            kwargs['sampler'] = None
            kwargs['drop_last'] = False

        super().__init__(dataset=dataset, batch_size=batch_size, sampler=sampler,
            collate_fn=collate_fn, num_workers=num_workers,
            pin_memory=pin_memory, drop_last=drop_last,
            timeout=timeout, worker_init_fn=worker_init_fn,
            batch_sampler=batch_sampler, shuffle=shuffle)

        assert len(dataset) > 0, 'dataset cannot be None'
        assert isinstance(dataset.datas, list), "the data attribute of DatasetGetter object must be a list"

        self.use_block_shuffle = use_block_shuffle
        self.sort_bs_num = sort_bs_num
        self.sort_key = sort_key
        self.batch_in_is_shuffle = batch_in_shuffle

    def __iter__(self):
        if self.use_block_shuffle is False:
            if self.num_workers == 0:
                return _SingleProcessDataLoaderIter(self)
            else:
                return _MultiProcessingDataLoaderIter(self)

        if self.use_block_shuffle is True:
            # self.dataset is the attribute in torch DataLoader
            self.dataset.datas = self.block_shuffle(self.dataset.datas, self.batch_size, self.sort_bs_num,
                                                       self.sort_key, self.batch_in_is_shuffle)
            if self.num_workers == 0:
                return _SingleProcessDataLoaderIter(self)
            else:
                return _MultiProcessingDataLoaderIter(self)

    @staticmethod
    def block_shuffle(data, batch_size, sort_bs_num, sort_key, batch_in_shuffle):
        random.shuffle(data)
        # 将数据按照batch_size大小进行切分
        tail_data = [] if len(data) % batch_size == 0 else data[-(len(data) % batch_size):]
        data = data[:len(data) - len(tail_data)]
        assert len(data) % batch_size == 0
        # 获取真实排序范围
        sort_bs_num = len(data) // batch_size if sort_bs_num is None else sort_bs_num
        # 按照排序范围进行数据划分
        data = [data[i:i + sort_bs_num * batch_size] for i in range(0, len(data), sort_bs_num * batch_size)]
        # 在排序范围，根据排序函数进行降序排列
        data = [sorted(i, key=sort_key, reverse=True) for i in data]
        # 将数据根据batch_size获取batch_data
        data = list(chain(*data))
        data = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]
        # 判断是否需要对batch_data序列进行打乱
        if batch_in_shuffle:
            random.shuffle(data)
        # 将tail_data填补回去
        data = list(chain(*data)) + tail_data
        return data





