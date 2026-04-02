\# Интерактивные примеры



\## API погоды



Ниже представлен интерактивный пример работы с API OpenWeatherMap. Вы можете ввести название любого города и увидеть текущую погоду.



<iframe src="/interactive/weather-demo.html" width="100%" height="400" frameborder="0" style="border: 1px solid #ddd; border-radius: 8px;"></iframe>



\## Как это работает



Пример использует JavaScript для отправки асинхронного запроса к API:



```javascript

async function getWeather() {

&#x20;   const city = document.getElementById('city').value;

&#x20;   const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}\&appid=${API\_KEY}\&units=metric`;

&#x20;   const response = await fetch(url);

&#x20;   const data = await response.json();

&#x20;   displayWeather(data);

}

