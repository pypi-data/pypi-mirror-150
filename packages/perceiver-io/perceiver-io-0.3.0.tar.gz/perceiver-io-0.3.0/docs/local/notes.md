## Per GPU memory usage

- settings:
  - batch_size=64
  - precision=32
  - num_encoder_layers=2

- baseline: 7635M
- activation checkpointing + DDP: 5895M
- activation checkpointing + DDPSharded: 5895M
- activation checkpointing + FSDP: 5895M

## Distributed training

```shell
python -m torch.distributed.run \
  --nnodes=2 \
  --master_addr 192.168.94.50 \
  --master_port 1234 \
  --node_rank 0 \
  train/train_mlm.py --dataset=imdb --learning_rate=1e-3 --max_epochs=100 --max_seq_len=512 --batch_size=64 --dropout=0.0 --weight_decay=0.0 --accelerator=ddp --gpus=1 --num_nodes=2 --experiment=tmp

python -m torch.distributed.run \
  --nnodes=2 \
  --master_addr 192.168.94.50 \
  --master_port 1234 \
  --node_rank 1 \
  train/train_mlm.py --dataset=imdb --learning_rate=1e-3 --max_epochs=100 --max_seq_len=512 --batch_size=64 --dropout=0.0 --weight_decay=0.0 --accelerator=ddp --gpus=1 --num_nodes=2 --experiment=tmp
```
