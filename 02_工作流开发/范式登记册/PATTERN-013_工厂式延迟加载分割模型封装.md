# PATTERN-013 · 工厂式延迟加载分割模型封装（import 零副作用）
- 来源: vqdang/hover_net（LIT-081）infer/base.py:56-78（__load_model）；反面教材 Moldia/ISS_postprocessing（LIT-017）ISS_postprocessing/segmentation.py:10,124
- 场景: 整合 pipeline 的分割模块需要加载深度模型权重——要求 import 包不触发权重下载/GPU 占用，模型只在显式调用时初始化。
- 做法: 模型加载全部收进 Manager 的私有方法：import_module 拿网络定义模块 → 工厂函数 create_model(**args) 建网 → torch.load 取 state_dict → convert 后 strict=True 加载 → DataParallel 上卡 → 再动态挂推理步与后处理函数。任何重型操作都在 __load_model 内，模块顶层只有轻量 import。骨架：
```python
# hover_net infer/base.py:56-74
def __load_model(self):
    model_desc = import_module("models.hovernet.net_desc")
    net = getattr(model_desc, "create_model")(**self.method["model_args"])
    saved = torch.load(self.method["model_path"])["desc"]
    net.load_state_dict(convert_pytorch_checkpoint(saved), strict=True)
    net = torch.nn.DataParallel(net).to("cuda")
    run_step = getattr(import_module("models.hovernet.run_desc"), "infer_step")
    self.run_step = lambda batch: run_step(batch, net)
    self.post_proc_func = getattr(import_module("models.hovernet.post_proc"), "process")
```
- 搬运条件: 依赖 torch；对 Xenium/cellpose/stardist 同样适用——Moldia 的反面做法（顶层 `model = models.Cellpose(gpu=False, model_type='nuclei')` 且重复两处、经 __init__ 导出链 import 即加载）必须避免；改造点：DataParallel 换 device 显式管理（配套 zoro-spatial 的 strict GPU 校验，意外 CPU fallback 应报错）。
- 工程评价: hover_net 是教科书式实现（strict 校验+工厂+动态挂载）；Moldia segmentation.py 同文件里 stardist 段（L46 函数内 from_pretrained）反而是对的，说明作者知道正解但未贯彻。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
