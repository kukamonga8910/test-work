// app.js
const http = require('http');

const requestHandler = (req, res) => {
    res.end('Hello from the Node.js application!');
};

const server = http.createServer(requestHandler);

server.listen(3000, () => {
    console.log('Server is listening on port 3000');
});
