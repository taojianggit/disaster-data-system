<!-- Legacy offline README retained for context.
# 灾害信息查询下载系统

这是一个离线静态网页系统，支持按灾害类型、发生时间、地点、受灾人口、直接经济损失和灾情描述进行组合查询，并将当前查询结果下载为 CSV 文件。

## 文件

- `index.html`：页面结构
- `styles.css`：页面样式
- `app.js`：示例数据、查询逻辑和 CSV 下载逻辑

## 下载字段

CSV 会导出以下字段：

- `disaster_type`：灾害类型
- `start_time`：发生时间
- `location`：发生地点
- `affected_population`：受灾人口
- `collapsed_houses`：倒塌房屋
- `crop_affected_area`：农作物受灾面积
- `direct_economic_loss`：直接经济损失
- `damage_description`：灾情描述

## 使用

直接打开 `index.html` 即可使用。下载按钮会导出当前筛选后的数据。

`app.js` 中的 `disasterRecords` 是示例数据。接入真实数据时，保持字段名一致即可复用查询和下载逻辑。
-->

# 灾害信息查询下载系统

开发人员：TAOJIANG

这是一个本地网页系统，服务端会从公开网页抓取真实灾害信息，前端支持组合查询并下载 CSV。

## 启动

在 PowerShell 中运行：

```powershell
cd E:\disaster-data-system
python server.py
```

然后打开：

```text
http://127.0.0.1:8765/
```

## 已接入来源

- 应急管理部-统计数据：https://www.mem.gov.cn/gk/tjsj/
- 应急管理部-灾害事故信息：https://www.mem.gov.cn/xw/zhsgxx/
- 国家地震科学数据中心：https://data.earthquake.cn/

当前服务会抓取应急管理部多个分页列表，不只读取最新首页。最近一次验证返回 241 条记录，覆盖 2018-2026 年。

说明：EM-DAT 公开表需要注册登录后下载 Excel，不能匿名直连抓取；水利部、自然资源部公开页面多为专题页、公告或动态数据，本版本优先通过应急管理部灾情通报抽取洪涝、地震、地质灾害的灾损字段。

## 查询

页面支持按以下条件组合查询：

- 数据来源
- 灾害类型
- 开始日期 / 结束日期
- 发生地点关键词
- 最小受灾人口
- 最小直接经济损失
- 灾情描述关键词

## 下载字段

CSV 会导出以下字段：

- `disaster_type`：灾害类型
- `start_time`：发生时间
- `location`：发生地点
- `affected_population`：受灾人口
- `deaths_missing`：死亡失踪
- `emergency_relocated`：紧急转移/救助
- `collapsed_houses`：倒塌房屋
- `crop_affected_area`：农作物受灾面积，单位为公顷
- `direct_economic_loss`：直接经济损失，单位为元
- `damage_description`：灾情描述
- `source_name`：数据来源
- `source_url`：来源链接

## 缓存

接口默认缓存 30 分钟。点击页面“刷新数据”按钮会重新抓取官方网站。
