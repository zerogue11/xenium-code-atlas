# PATTERN-015 · HoVer 梯度谷分水岭实例分离后处理
- 来源: vqdang/hover_net（LIT-081）models/hovernet/post_proc.py:26-90（__proc_np_hv）、94-186（process）
- 场景: 密集核分割中粘连实例的分离——不依赖 marker 人工标注，用网络回归的水平/垂直距离图（HoVer map）自身构造分水岭地形。
- 做法: 核概率图二值化去小对象；对 h/v 回归图做 Sobel（ksize=21）提取边界梯度并归一化取反，与概率掩码相乘得地形；取整体梯度 >=0.4 为种子禁区，blb-marker 填洞+开运算+去小对象后得到分水岭标记点，最后 watershed(dist, markers, mask=blb) 分裂实例；逐实例提 bbox/矩心/轮廓并按像素多数投票定类型（背景占多数时取第二类兜底）。骨架：
```python
blb = (pred[..., 0] >= 0.5).astype(np.int32)          # 核概率
sobelh = 1 - normalize(cv2.Sobel(h_dir, cv2.CV_64F, 1, 0, ksize=21), ...)
overall = np.maximum(sobelh, sobelv); overall -= (1 - blb)
dist = -cv2.GaussianBlur((1.0 - overall) * blb, (3, 3), 0)   # 山谷反转
marker = measurements.label(binary_fill_holes(blb - (overall >= 0.4)))[0]
proced_pred = watershed(dist, markers=marker, mask=blb)      # 实例分离
```
- 搬运条件: 依赖 opencv/scipy/skimage；免费可搬（MIT）；改造点：ksize=21、阈值 0.4、min_size=10 均为 40x 组织学经验值，换成像尺度（如 Xenium DAPI）需重调；注意源码 `warnings.warn = noop` 静默警告不要照搬。
- 工程评价: 逻辑紧凑、注释清晰、边界情况（<3 点轮廓、异常形状）有防护；是本批分割组最值得直接复用的算法模块。
- 迭代记录: 2026-09-04 收录(一期精读批次B)
