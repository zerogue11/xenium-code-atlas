# PATTERN-041 · 模块级容器工厂（每模块独立 Docker + WDL 内版本钉死）
- 来源: hisplan/sharp（LIT-078）相对路径:行号 `dockers/hto-demux-kmeans/(Dockerfile/build.sh/push.sh/config.sh/demux_kmeans.py)、modules/HtoDemuxKMeans.wdl:17(String dockerImage = dockerRegistry + "/hto-demux-kmeans:0.5.0")`
- 场景: 管线各步依赖冲突（python/R/tf 版本互斥）或需独立升级时，不建巨型一体化镜像，而是每个任务模块一个微容器，模块代码与容器版本同步演进。
- 做法: `dockers/<module>/` 五件套：任务源码 + Dockerfile（apt 装最小依赖 + COPY 源码到固定路径 /opt）+ build.sh + push.sh + config.sh（镜像名/registry 集中）。WDL task 里镜像引用永远走 `dockerRegistry` 参数 + 钉死 tag，registry 换云厂商/私有仓只改 inputs.json 一行；task 的 command 只调容器内固定路径脚本，输出文件名固定成契约（classification/stats/log）。
  ```dockerfile
  FROM ubuntu:20.04
  RUN apt-get install --yes python3 python3-pil... && pip3 install pandas numpy pyyaml scipy sklearn
  COPY demux_kmeans.py /opt/demux_kmeans.py
  ```
  ```wdl
  String dockerImage = dockerRegistry + "/hto-demux-kmeans:0.5.0"
  command <<< set -euo pipefail; python3 /opt/demux_kmeans.py --hto-umi-count-dir ./inputs ... >>>
  ```
- 搬运条件: 需容器 registry（quay/dockerhub/私有）+ docker build 流程；MIT 可自由搬；需改造点：Dockerfile 内 pip 依赖建议加版本钉（原实现未锁）；我们 WSL2 环境可直接沿用 build/push 两脚本节奏。
- 工程评价: 模块边界=容器边界=测试边界=升级边界，四方一致是 WDL 生态最干净的解法；微小代价是 7 个镜像的构建维护成本（sharp 总评 13/14）。
- 迭代记录: 2026-09-04 收录(一期精读批次D)
