//Set up web server
const express = require('express');
const app = express();
var async = require('async');

//Set view engine and allow access to public/css
app.set('view engine', 'ejs');
app.use(express.static('public/css'));

//Start server
app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
})

//Connect to database
const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('fishtank.db');

//Home page
app.get('/', function(req, res) {

	//Temps variables
	var currentAmbientTemp = '18.2';
	var lightStatus = 'OFF';
	var airPumpStatus = 'OFF';
	var currentWaterTemp = '25.5';


	//Get temps from database
	var tempHistoryQuery = "SELECT * FROM watertemp ORDER BY id DESC LIMIT 50";
	var currentWaterTempQuery = "SELECT temp FROM watertemp ORDER BY id DESC LIMIT 1";

	async.series({
		tempHistory: cb => db.all(tempHistoryQuery, cb),
		currentWaterTemp: cb => db.all(currentWaterTempQuery, cb)
		}, (err, results) => {
			res.render('index', { 
			tempHistory: results['tempHistory'],
			currentWaterTemp: results['currentWaterTemp'][0]['temp'],
        	currentAmbientTemp: currentAmbientTemp,
        	lightStatus: lightStatus,
        	airPumpStatus: airPumpStatus
		})
		console.log(results);
	});
});
