DataEase-Insights：开源项目活跃度与趋势预测

说明
-
本项目基于 DataEase 开源项目要求，主题选择：开源项目活跃度与趋势预测。目标是提供一个轻量级原型，展示如何用开源社区数据进行时序分析、活跃度监测与趋势预测，并通过简单 API 与静态前端展示结果。

快速开始
-
1. 安装依赖：
```
pip install -r requirements.txt
```
2. 运行服务：
```
python app.py
```
3. 打开浏览器访问： http://127.0.0.1:5000/

Docker（可选）
-
构建并运行容器：
```
docker build -t dataease-insights .
docker run -p 5000:5000 dataease-insights
```

项目结构
-
- PROPOSAL.md   项目提案与评分对照
- README.md
- requirements.txt
- app.py         简单 Flask 后端 API
- data_processing.py 数据加载与趋势计算逻辑
- data/sample_data.csv 示例数据
- static/index.html 简单前端展示

下一步
-
- 用真实开源社区数据替换示例 CSV（GitHub API / GHTorrent / BigQuery 等）
- 增加图表（Chart.js / ECharts）与交互筛选
- 添加模型改进（时间序列模型、异常检测、关键贡献者网络分析）
