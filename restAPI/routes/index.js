/* global require,console */
var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function (req, res) {
	res.render('index', {title: 'Servo UI'});
});

router.post('/setSpeed', function (req, res) {	
});

module.exports = router;
