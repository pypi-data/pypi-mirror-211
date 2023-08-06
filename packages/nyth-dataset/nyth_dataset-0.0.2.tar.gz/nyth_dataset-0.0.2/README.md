# NYT-H dataset

NYT-H dataset package allows the processing of the NYT-H dataset proposed by Zhu _et al._,
2020 [[pdf]](https://www.aclweb.org/anthology/2020.coling-main.566.pdf). NYT-H is based on the New York Times 2010 (
NYT2010) dataset proposed by Riedel _et al._,
2010 [[pdf]](https://link.springer.com/content/pdf/10.1007/978-3-642-15939-8_10.pdf). The advantage of NYT-H dataset is
the manual annotation of the test partition.

Codes to process and read the NYT-H dataset used in the COLING2020 paper: Towards Accurate and Consistent Evaluation: A
Dataset for Distantly-Supervised Relation Extraction [[pdf]](https://www.aclweb.org/anthology/2020.coling-main.566.pdf)

## Dependencies

- python == 3.7
    - pandas

## Dataset

### Download

Download Link (from [NYT-H project](https://github.com/Spico197/NYT-H)):

- Google Drive: [download](https://drive.google.com/file/d/1my4W7O-ioCYWRiP6VCbgGfXTzgdrDep0/view?usp=sharing)

Download the data from the link. Then extract data files from the tarball file.

```bash
$ tar jxvf nyt-h.tar.bz2
```

### Data Example (from [NYT-H project](https://github.com/Spico197/NYT-H))

```python
{
    "instance_id": "NONNADEV#193662",
    "bag_id": "NONNADEV#91512",
    "relation": "/people/person/place_lived",
    "bag_label": "unk",  # `unk` means the bag is not annotated, otherwise `yes` or `no`.
    "sentence": "Instead , he 's the kind of writer who can stare at the wall of his house in New Rochelle -LRB- as he did with '' Ragtime '' -RRB- , think about the year the house was built (1906) , follow his thoughts to the local tracks that once brought trolleys from New Rochelle to New York City and wind up with a book featuring Theodore Roosevelt , Scott Joplin , Emma Goldman , Stanford White and Harry Houdini . ''",
    "head": {
        "guid": "/guid/9202a8c04000641f8000000000176dc3",
        "word": "Stanford White",
        "type": "/influence/influence_node,/people/deceased_person"
        # type for entities, split by comma if one entity has many types
    },
    "tail": {
        "guid": "/guid/9202a8c04000641f80000000002f8906",
        "word": "New York City",
        "type": "/architecture/architectural_structure_owner,/location/citytown"
    }
}
```

### File Structure and Data Preparation (from [NYT-H project](https://github.com/Spico197/NYT-H))

```
data
├── bag_label2id.json : bag annotation labels to numeric identifiers. `unk` label means the bag is not annotated, otherwise `yes` or `no`
├── rel2id.json : relation labels to numeric identifiers
├── na_train.json : NA instances for training to reproduce results in our paper
├── na_rest.json : rest of the NA instances
├── train_nonna.json : Non-NA instances for training (NO ANNOTATIONS)
├── dev.json : Non-NA instances for model selection during training (NO ANNOTATIONS)
└── test.json : Non-NA instances for final evaluation, including `bag_label` annotations
```

To get the full NA set:

```bash
$ cd data && cat na_rest.json na_train.json > na.json
```

To reproduce the results in our paper, combine the sampled NA instances(`na_train.json`) and `train_nonna.json` to get
the train set:

```bash
$ cd data && cat train_nonna.json na_train.json > train.json
```

## How to use the package

```python
from nyth_dataset import NYTHDataset

# Create the object with the data path
dataset = NYTHDataset(data_dir='./data')
# Load the data
dataset.load_data()
# Get the data
train, dev, test = dataset.get_data()
```

Additionally, you can define the parameters:

- **include_na_relation** in the constructor (_default_ **True**). If it is _True_ the NA (Not a Relation) instances are
  loaded, otherwise not.
- **reload** in the method load_data (_default_ **False**). If it is _True_ the method will read the original files;
  otherwise, it will load the *.pkl saved on the first run

```python
from nyth_dataset import NYTHDataset

# Create the object with the data path
dataset = NYTHDataset(data_dir='./data', include_na_relation=False)
# Load the data
dataset.load_data(reload=True)
# Get the data
train, dev, test = dataset.get_data()
```

## Format of the loaded data

The train, dev and test files are dataframes with the following columns:

```
data
├── instance_id : identifier of the instance
├── bag_id : identifier of the bag
├── sentence : full sentence
├── e1_name : name of the head entity
├── e2_name : name of the tail entity
├── e1_type : type of the head entity
├── e2_type : type of the tail entity
├── text_between_entities_including_them : text between the entities including them
├── text_between_entities : text between the entities without them
├── relation : relation
├── bag_label :  2 (unk) means the bag is not annotated, otherwise 1 (yes) or 0 (no).
└── noisy : 2 (unk) means the instance is not annotated, otherwise 1 (noisy) or 0 (not noisy)
```

## License

Apache Software License