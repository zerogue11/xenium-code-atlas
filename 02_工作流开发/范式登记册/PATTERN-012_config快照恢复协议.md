# PATTERN-012 · config.yaml + outputs.pkl 训练快照/恢复协议
- 来源: ding-lab/mushroom（LIT-019;LIT-071）mushroom/mushroom.py:129-170（from_config）、210-278（save）
- 场景: 长训练/多阶段分析（train→embed→volume→integrate）中断后恢复，或把已训好的结果交给下一阶段/他人，而不重跑上游。
- 做法: save() 把"重建对象所需的全部超参"写 config.yaml、把"重计算才得到的全部产物"（clusters/probs/volumes/positions）写 outputs.pkl（protocol=4）；from_config() 先查 outputs.pkl 是否存在，存在则直接恢复内存态并跳过 embed_sections，不存在才重新训练/嵌入。骨架：
```python
def save(self, output_dir=None):
    config = {'sections': self.sections, 'dtype_to_chkpt': self.dtype_to_chkpt,
              'sae_kwargs': ..., 'trainer_kwargs': ...}
    outputs = {'section_positions': ..., 'dtype_to_volume': ...,
               'dtype_to_clusters': dtype_to_clusters, ...}
    yaml.safe_dump(config, open(f'{output_dir}/config.yaml', 'w'))
    pickle.dump(outputs, open(f'{output_dir}/outputs.pkl', 'wb'), protocol=4)

@staticmethod
def from_config(input, accelerator=None):
    if os.path.exists(os.path.join(input, 'outputs.pkl')):
        outputs = pickle.load(open(os.path.join(input, 'outputs.pkl'), 'rb'))
    # ... 恢复 section_positions/dtype_to_volume/integrated_clusters
```
- 搬运条件: 仅依赖 pyyaml+pickle；改造点：pickle 换安全格式（npz/parquet/h5ad）防任意代码执行；yaml 不支持 Path 对象需先 str()（源码 L272 已处理）；本工程按"结果包不可覆盖"纪律应在文件名加版本号。
- 工程评价: 简洁有效，"超参/产物分离 + 存在即跳过"的思想值得推广；pickle 载入有安全与版本耦合风险。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
