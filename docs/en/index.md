# Weather Service

Welcome to the Weather Service documentation. Our service provides current weather data for locations worldwide.

## Quick Start

### 1. Get API Key

1. Register at [OpenWeatherMap](https://openweathermap.org)
2. Confirm your email
3. Go to "API Keys" section
4. Copy your key (starts with `bd5e37...` or `123abc...`)

### 2. First Request

Use `curl` to get weather in London:

```bash
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=metric"