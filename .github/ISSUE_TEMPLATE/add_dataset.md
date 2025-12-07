## ✔️ New Dataset Checklist

### Add functionality 
- [ ] If there's no ml domain folder
    - [ ] Create it: `dataset_hub/<domain>/`
    - [ ] Create configs folder: `dataset_hub/<domain>/_configs/`
    - [ ] Create py init file: `dataset_hub/<domain>/__init__.py`
    - [ ] Create py datasets file: `dataset_hub/<domain>/datasets.py`
    - [ ] Fill it out like datasets.py in another folders. Don't foget to change `task_type` var to correct
    - [ ] Add new ml domain into `__all__` var in `dataset_hub/__init__.py`
- [ ] Create and fill out the dataset's config: `dataset_hub/<domain>/_config/<dataset_name>.yml`
- [ ] Create and fill out new function in `dataset_hub/<domain>/datasets.py`, e.g. `get_titanic()`
- [ ] Add that function into `__all__` var in `dataset_hub/<domain>/__init__.py`

### Add documentation logistic
- [ ] If there's no ml domain folder in `docs/datasets/`
    - [ ] Create it: `docs/datasets/<domain>/`
    - [ ] Create: `docs/datasets/<domain>/index.rst`. Add heading, small description by analogy with others
    - [ ] Add link on it into `docs/datasets/index.rst` file
- [ ] Create `docs/datasets/<domain>/<dataset_name>.rst`
- [ ] Add link on it into `docs/datasets/<domain>/index.rst` file
- [ ] Add heading and autofunction link into `docs/datasets/<domain>/<dataset_name>.rst`. 

### Add dataset test
- [ ] Add new function into `AVAILABILITY_DATAFRAME_DATASETS` var(or another a similar one) in `tests/availability/test_datasets.py`

### Add documentation
- [ ] Add docstring for function by analogy with others functions. Don't forget about:
    - [ ] Small desrtiption
    - [ ] Official link
    - [ ] Columns description
    - [ ] Target description with 🚩 symbol 
    - [ ] Args description
    - [ ] Add fast loading Example
    - [ ] Add simple baseline for dataset by analogy with others