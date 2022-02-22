const echoDisplay = document.querySelector('#echo')
// const url = 'https://postman-echo.com/get?foo1=bar1&foo2=bar2'

fetch('http://localhost:8000/echo')
    .then(res => res.json())
    .then(data => {
        console.log(data)
        let html = '';
        Object.keys(data.args).forEach(key =>{ let htmlSegment = `<div>
                                               <h2>${key} ${data.args[key]}</h2>
                                               <div>  API Requested: <a href="apiRequest:${data['url']}">${data['url']}</a></div></div>`
        html += htmlSegment;});
        echoDisplay.insertAdjacentHTML("beforeend", html)
    })
    .catch(err => console.log(err))



// axios.get(url)
//   .then(function (response) {
//     console.log(response.data);
//     res.json(response.data);
//     const title  = '<h3>' + 'test' + '<h3/>';
//     echoDisplay.insertAdjacentHTML("beforeend", title);
//   }).catch(function (error) {
//     console.log(error);
//   })()