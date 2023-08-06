<h1 align="center"> Domain-PaaS-SDK for Python </h1>
<div align="center">

 ![Python version](https://img.shields.io/pypi/pyversions/mikeio.svg)
[![PyPI version](https://badge.fury.io/py/domain_paas_sdk_python.svg)](https://badge.fury.io/py/domain_paas_sdk_python)
  
这是一个[DHI 中国 业务中台](https://online-products.dhichina.cn/) 的 Client SDK 开发辅助包，帮您快速通过我们的业务中台构建应用。

</div>

## 🔆 功能清单

- [x] identity-service 用户认证管理服务
- [x] scenario-manager-service 方案管理服务
- [x] message-service 消息服务
- [x] document-service 文档服务
- [x] scenario-compute-service 方案计算服务
- [ ] model-driver-service 模型计算服务
- [x] result-analysis-service 结果分析服务
- [x] model-information-service 模型分析服务
- [x] model-configuration-service 模型计算服务
- [ ] text-search-service 全文搜索服务
- [ ] device-management-service 资产设备服务
- [x] accident-management-service 事故管理服务
- [x] digital-twin-service 模型映射服务
- [x] iot-service IoT 服务
- [x] wwtp-domain-main-bus-service 污水业务中台基础服务
- [x] wwtp-domain-infrastructure-service 污水业务中台邻域服务
- [x] wd-domain-service 供水业务中台领域服务

## 适用平台
* Mac、Windows和Linux

## Installation

From PyPI: 

`pip install domain-paas-sdk-python`

## 使用

需要先联系我们获取的 [DHI 中国 业务中台](https://online-products.dhichina.cn/) 使用许可和认证信息。

### 基础使用
test.py
```
# coding: utf-8

// 引入需要使用的包
from wwtp_paas_main_bus_service import *
from wwtp_paas_main_bus_service import ApiClient
from wwtp_paas_main_bus_service import CalculateDosageApi
// 构建参数
configuration=Configuration.get_default_copy()
configuration.verify_ssl=False
configuration.host="http://172.23.21.60:61120"
// 初始化
client = ApiClient(configuration)
calculate = CalculateDosageApi(client)
// 调用接口
response = calculate.api_calculate_dosage_excute_plc_get()

```
