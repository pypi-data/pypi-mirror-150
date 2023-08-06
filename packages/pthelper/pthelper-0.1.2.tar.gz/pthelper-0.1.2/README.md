# `pthelper` - PyTorch
A python package containing the basic boilerplate code for training and evaluation of PyTorch models. The main purpose of this package is to remove writing the same code for training/inference again and again for different projects. 

Apart from training and evaluation, it also contains other helper functions to perform logging stats in the console as well as Keras like model summaries using [torchinfo](https://github.com/TylerYep/torchinfo) package.

## Install
```pip install pthelper```

## Usage
**Utility functions**
- Print model details:
```python
from pthelper import utils

model = PyTorchModel()
input_size = (4, 28*28)
device = torch.device('cpu')
utils.model_details(model, input_size, device)
```

![model_summary](assets/model_summary.png)

**Model training and evaluation**
- Train the model:
```python
import torch
import torch.nn as nn
from pthelper import trainer, utils

epochs = 5
model = PyTorchModel()
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
logger = utils.get_logger()
pt_trainer = trainer.PTHelper(model, loss_fn, optimizer, logger, num_classes=1)
for i in range(epochs):
    train_loss = pt_trainer.train(train_dataloader, epoch=i)
    valid_loss, predictions, targets = pt_trainer.evaluate(valid_dataloader)
```

## Scope
Right now, only binary and multi-class classification tasks are supported. In future releases, more functionality will be added like autoencoders, RNNs, GANs, etc.