# PATTERN-024 · scVI→scANVI 种子注释迁移链（seed annotation 先行 + GPU 确定性）
- 来源: icbi-lab/crc-atlas（LIT-072）相对/路径:行号 — subworkflows/Integrate_datasets.nf:33-38,44-49,68-78；modules/local/scVI.nf:10-76；bin/scVI.py:26-43
- 场景: 百万细胞级多研究整合时，全量人工注释不可行——先用少量高置信"种子"细胞训练标签迁移，再由 scANVI 半监督扩散到全图谱。
- 做法: 分头做种子注释（每样本类型一个 Get_Seeds→Annotate_*_seeds 脚本）→ SCVI 先在种子标签上训练（SCVI_SEED）→ SOLO 双细胞剔除 → 全量 SCVI 整合 → scANVI 加载 scVI 模型做半监督标签迁移 → neighbors/leiden/UMAP。确定性由 bin/scVI.py 的 set_all_seeds 保证：PYTHONHASHSEED+numpy+random+torch.manual_seed+`torch.use_deterministic_algorithms(True)`+CUDA seed。
```python
def set_all_seeds(seed=0):
    scvi.settings.seed = seed
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.use_deterministic_algorithms(True)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed); torch.cuda.manual_seed_all(seed)
# 进程侧: SCANVI 加载 scVI 模型做标签迁移
scANVI.py --input_adata --input_model=${scvi_model} --batch_key --labels_key
```
- 搬运条件: scvi-tools>=1.0；GPU label + cpus 固定（base.config:35 "cpus=12 For scVI reproducibility"）；容器内 torch 版本锁定（envs/2024-scvi-tools.def+yaml 双轨）；README 明示换硬件可能改变标签——引用标签时必须注明硬件。
- 工程评价: 进程/CLI 分离干净（.nf 只做参数拼装与资源，:30-35 拼可选参数的三元写法值得抄）；确定性函数是全链最完整实现；瑕疵=OMP_NUM_cpus 等无效环境变量拼写（scVI.nf:21-24）、路径硬编码在配置层。
- 迭代记录: 2026-09-04 收录(一期精读批次C)
