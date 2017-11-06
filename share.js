var express = require("express"),
    request = require("request"),
    fs      = require("fs"),
    bP      = require("body-parser");

var app = express();
app.set("view engine", "ejs");
// app.use(express.static(path.join(__dirname, 'scripts')));
app.set("views", "./scripts");
app.use(bP.urlencoded({extended: true}));

app.get("/twitter", function(req, res) {
    var obj = {oauth_verifier: req.query.oauth_verifier};
    fs.writeFile('oauth_cred.json', JSON.stringify(obj), 'utf8', function(err) {
        if(err) {
            console.log(err);
        }
    });
});

app.get("/facebook", function(req, res) {
    res.render("fb");
});

app.post("/facebook", function(req, res) {
    // console.log(req.body);
    fs.writeFile('oauth_cred.json', JSON.stringify(req.body), 'utf8', function(err) {
        if(err) {
            console.log(err);
        }
    });
});

app.listen(3000, process.env.IP, function() {
	console.log("Server started.....");
});
