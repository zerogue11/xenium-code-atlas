# 高级模块骨架（A 系）

> 与资源分类（P 系）的映射。一期每个模块只立骨架：技术路线占位 + 对应资源仓索引；二/三期由精读产出与实测填充。

| 模块 | 名称 | 资源来源 | 状态 |
|---|---|---|---|
| A1 | 细胞分割与重分割 | P1（mushroom、hover-net、iss_patcher…） | 骨架 |
| A2 | 注释与去卷积 | P2（SpatialEcotyper、crc-atlas、teichlab 系） | 骨架 |
| A3 | 空间域·邻域·生态位 | P3（niche/domain/community 系） | 骨架 |
| A4 | 细胞通讯 | P4 | 骨架 |
| A5 | 亚细胞·转录本定位 | P5（drug2cell、snp2cell…） | 骨架 |
| A6 | 空间统计与 SVG | P6 前半 | 骨架 |
| A7 | 多样本整合·配准·3D | P6 后半（3d-analysis、10xmapping） | 骨架 |
| A8 | 图像组学·多模态 | P7（H&E/成像整合） | 骨架 |
| A9 | 场景化应用范式 | P8（TME/纤维化/神经/发育，按场景归组） | 骨架 |

基础流程（读取→QC→归一化→降维聚类→注释→marker→基础空间图）由"候选流程池"承载，定版后移入 `整合pipeline/`。
