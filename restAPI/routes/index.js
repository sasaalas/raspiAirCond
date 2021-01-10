/* global require,console */
var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res) {
	res.render('index', {title: 'raspiAirCondRestAPI'});
});

router.post('/setSpeed', function (req, res) {	
	var selectedTime = 0;
	var selectedSpeed = 0;
	if (req.body.speed == 1) {
		selectedSpeed = 0;
	}
	else if (req.body.speed == 2) {
		selectedSpeed = 30;
	}
	else if (req.body.speed == 3) {
		selectedSpeed = 60;
	}
	else if (req.body.speed == 4) {
		selectedSpeed = 60;
		selectedTime = 900;
	}

	/* var exec = require('child_process').exec;
	execString = 'sudo python3 /your/absolute/path/to/servoWrapper.py' + ' ' + selectedSpeed + ' ' + selectedTime;

	exec(execString, function (error, stdout, stderr) {
		if (error !== null) {
			console.log('exec error: ', error);
			res.send("There was a problem invoking child process.");
		}
	}); */

	res.location("/");
	res.redirect("/");
});

module.exports = router;
