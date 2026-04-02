# 天气服务

欢迎使用天气服务文档。我们的服务提供全球各地的实时天气数据。

## 快速开始

### 1. 获取API密钥

1. 在[OpenWeatherMap](https://openweathermap.org)注册
2. 确认您的电子邮件
3. 转到"API Keys"部分
4. 复制您的密钥（以`bd5e37...`或`123abc...`开头）

### 2. 第一个请求

使用`curl`获取北京的天气：

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=Beijing&appid=YOUR_API_KEY&units=metric"