var express = require("express"),
    request = require("request"),
    fs      = require("fs"),
    bP      = require("body-parser");

var app = express();
app.set("view engine", "ejs");
// app.use(express.static(path.join(__dirname, 'scripts')));
app.set("views", __dirname + "/scripts");
app.use(bP.urlencoded({extended: true}));

app.get("/twitter", function(req, res) {
    var obj = {oauth_verifier: req.query.oauth_verifier};
    var status = req.query.status;
    var screen_name = req.query.name;
    fs.writeFile(__dirname + '/oauth_cred.json', JSON.stringify(obj), 'utf8', function(err) {
        if(err) {
            console.log(err);
        }
    });
    if(status == "completed") {
        function redirect() {
            res.redirect("https://twitter.com/"+screen_name);
        }
        setTimeout(redirect, 3000);
    } else {
        res.render("pending.ejs");
    }
});

app.get("/facebook", function(req, res) {
    console.log(req.query.status)
    if(req.query.status == "completed"){
        res.redirect("https://facebook.com/"+req.query.user);
    } else {
        res.render("fb");
    }
});

app.post("/facebook", function(req, res) {
    // console.log(req.body);
    fs.writeFile('oauth_cred.json', JSON.stringify(req.body), 'utf8', function(err) {
        if(err) {
            console.log(err);
        }
    });
    // res.render("pending");
});

app.listen(3000, process.env.IP, function() {
	console.log("Server started.....");
});
