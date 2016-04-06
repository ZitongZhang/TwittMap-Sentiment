var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);

var es = require('elasticsearch');
var endpoint = 'https://search-twittmap-qtnxkqs26tfzc27letgg2blf5i.us-east-1.es.amazonaws.com';
var client = new es.Client({host: endpoint});

var bodyParser = require('body-parser');
var request = require("request");

app.use(express.static('public'));
app.use(bodyParser.json({type: 'text/plain'}));

app.get('/', function (req, res) {
    res.sendfile(__dirname + '/public/index.html');
});

app.post('/', function (req, res) {
    res.status(200).end();
    var type = req.get('x-amz-sns-message-type');
    if (type === 'SubscriptionConfirmation') {
        var url = req.body.SubscribeURL;
        request(url, function (error, response, body) {
            console.log(body);
        });
    }
    else if (type === 'Notification') {
        var id = req.body.MessageId;
        var message = req.body.Message;
        client.index({
            index: 'twittmap',
            type: 'tweets',
            id: id,
            body: message
        });
    }
});

server.listen(80);

io.on('connection', function (socket) {
    socket.on('clicked', function (data) {
        var key = data.key;
        client.search({
            q: key,
            size: 1000
        }, function (error, body) {
            var result = [];
            var hits = body.hits.hits;
            for (var i = 0; i < hits.length; i++) {
                result[i] = hits[i]._source;
            }
            var myObject = {
                "tweet": result
            };
            socket.emit('toggle', myObject);
        });
    });
});