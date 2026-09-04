# PATTERN-002 · 样本表驱动的批量 QC 编排（单指标失败隔离）

- 来源: Center-for-Spatial-OMICs/SpatialQM（LIT-028）R/utils.R:22-240（getAllMetrics）
- 场景: 批量样本进入质控模块时：一行一个样本的 manifest 表驱动全部指标批算，且要求任何一个样本/指标失败不拖垮整批（结果留 NA 继续算下一个），最后产出一张贴样本表直接可画箱线图。
- 做法: 样本表约定五列（sample_id/platform/expMat/tx_file/cell_meta），先做列校验，再按"指标块"组织：每块 set NA → mapply 批算 → tryCatch 捕获降级为 message。R 侧用 mapply，Python 侧对应写法是 DataFrame.iterrows + 逐指标 try/except 填 NaN。
  ```r
  getAllMetrics <- function(df_samples, features = NULL) {
    df_samples <- .validate_sample_metrics_df(df_samples)   # 列校验
    tryCatch({
      df_samples$nCells <- mapply(getNcells,
                                  expMat  = df_samples$expMat,   # 具名列，勿用 [,3]
                                  platform = df_samples$platform)
    }, error = function(e) message("ERROR: ", conditionMessage(e)))
    # ... 每个指标一个同构 tryCatch 块 ...
    return(df_samples)   # 指标作为新列写回样本表
  }
  ```
- 搬运条件: 无额外依赖（R base + tidyverse 或 pandas）；需改造点——①**必须用具名列**（SpatialQM 旧版 df_samples[,3] 位置索引是事故源）；②原实现错误仅 message 后留 NA，搬运时应把错误文本写入 `df_samples$<metric>_error` 列，失败可追溯；③块结构适合用指标函数名列表 for 循环压缩，避免 15 段复制。
- 工程评价: 思路（manifest 驱动 + 失败隔离 + 指标即列）非常值得搬；原实现是反面教材与正面思路的混合体——utils.R 新版已改具名列+校验，但 tryCatch 吞错不登记、15 个 tryCatch 块纯复制粘贴，且同包内旧版覆盖新版。
- 迭代记录: 2026-09-04 收录(一期精读批次A)
