\# Примеры культурной адаптации



\## Форматы дат и валют



\### Английская версия (en-US)



```javascript

const date = new Date();

console.log(date.toLocaleDateString('en-US')); // MM/DD/YYYY

console.log(new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(1000)); // $1,000.00

