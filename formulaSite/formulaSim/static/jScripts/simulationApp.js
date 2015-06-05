/*	Author: Alberto Scicali
	email: cicciobello00@gmail.com
*/

// The canvas and its context
var c = document.getElementById("c");
var ctx = c.getContext("2d");

// This Scales the canvas so it does not lose quality on 
// high resolution monitors
devicePixelRatio = window.devicePixelRatio || 1;
console.log("pixel ration " + devicePixelRatio);
if(devicePixelRatio > 1){
	console.log("HERE");
	backingStoreRatio = ctx.webkitBackingStorePixelRatio ||
                		ctx.mozBackingStorePixelRatio ||
                		ctx.msBackingStorePixelRatio ||
                		ctx.oBackingStorePixelRatio ||
                		ctx.backingStorePixelRatio || 1;
	var ratio = devicePixelRatio / backingStoreRatio;

	// resize canvas' logical size (ensure CSS maintains original size)//
	var w = ctx.canvas.width;
	var h = ctx.canvas.height;
	c.setAttribute('width', w*ratio);
	c.setAttribute('height', h*ratio);
	c.style.width = w + 'px';
	c.style.height = h + 'px';
}

// List of color variables for racers to choose from
var driverColorSpectrum = ['#F8C677', '#5F7BB7', '#F34A35', '#B81C46', '#2DD692', '#2D6F70', '#FFAC43', 
'#F36B76', '#FF005C', '#2DA570', '#FEBE18', '#FF6B00', '#D93445', '#FC000F', '#2DD070', '#7F89AE', '#F3427F', 
'#FF8943', '#FF6600', '#E91229', '#FFA300', '#00A9B5', '#F9E671' , '#7512A7', '#F35260'
];

// Initial variables
// Grabbing the WIDTH and HEIGHT from the canvas DOM
var WIDTH = c.width;
var HEIGHT = c.height;
// Creating lists of the necessary models drivers, laps, etc
	var json_drivers = {{ serialized_drivers|safe }};
	var json_laptimes = {{ serialized_laptimes|safe }};
	var json_results = "{{ serialized_results|safe }}";
	var json_status = "{{ serialized_status|safe }}";
	var json_pitstops = "{{ serialized_pitstops|safe }}";

	// Variables for the simulation
	var TRACK_RADIUS = (WIDTH - 45) / 2;
	var CAR_WIDTH = WIDTH / 70;
	var TOTAL_CIRCUIT_LAPS = 0;
	var LAP_ANGLE = 0;

	// Holder variables that are set for every race
	var simulation_drivers = [];
	var retiredDriverCount = 0;

	// Game stat variables
	var simulationCompleted = true;
	var simulationPaused = false;

	//Function to convert degrees to radians for when circles/arcs need to be drawn
	//More of a convenience tool
	//@param degrees
	//@return radians conversion
	function degToRad(deg){
		return (Math.PI / 180 * deg);
	}

	/*
	Driver prototype that holds the necessary function and variables
	The variables are set from the provided JSON files.
	@param lastname of the driver, driver codename, driverid/pk, 
			results construct, list of laptimes, list of pitstops
	*/
	function FormulaDriver(lastname, codeName, driverid, result, laptimes, pitstops){
	this.lastname = lastname;
	this.codeName = codeName
	this.driverid = driverid;
	this.results = result;
	this.pitstops = pitstops;
	this.curStatus = null;
	this.laptimes = laptimes;
	this.lapLength = 0;
	this.curPosition = 0;
	this.curLap = 1;
	this.totalLapCount = this.laptimes.length;
	//this.posX = 0;
	//this.posY = startY;
	this.curSpeed = 0;
	this.retired = false;
	// Variables for the circular positioning
	this.radiusPos = 0;
	this.posAngle = -90;
	this.circumSpeed = 0;
	this.driverCircum = (2 * Math.PI * this.radiusPos);

	// color variable for driver
	this.driverColor = 'rgb(0, 0, 0)';
	this.driverStatsSpan = null;
	this.driverPositionSpan = null;
	this.pitstop_laps_draw = [];

	/*
		Updates the speed variable of the driver based off of the avg laptime for the current
		lap they are currently on. Speed is calculated by taking length of the arc 
		of the lap angle for the driver's assigned circumfrence. Each driver has a different 
		circumfrence and radius so that they are position into the circle appropraitely.
	*/
	this.updateSpeed = function(){
		// speed is based off of the laptime of the current lap
		/*
		if(!this.retired && this.laptimes[this.curLap] != null){
			this.curSpeed = (this.lapLength / this.laptimes[this.curLap].milliseconds) * 1000;
		}
		*/
		if(!this.retired && this.laptimes[this.curLap - 1] != null){
			this.circumSpeed = ((this.driverCircum / TOTAL_CIRCUIT_LAPS) / this.laptimes[this.curLap - 1].milliseconds);
		}
	};

	/*
		Move function that uses the the driverSpeed to determine how many units along the driver's
		circumfrence the driver will move. Also checks if they are already retired or not.
	*/
	this.move = function(){
		//Check if driver is retired from race
		this.check_retired();


		//If the driver has not yet retired from the race
		if(!this.retired){
			if(this.curLap == 1){
				this.updateSpeed();
			}
			var speedBoost = document.querySelector('#sim-speed-slider').value;
			this.posAngle += ((this.circumSpeed * speedBoost) / this.driverCircum * 360);
			this.checkLapped();

		}
		//else do nothing, they're retired, silly!

	};

	/*
		Draw method for the pitstops. Loops the the driver list pitstops_laps_draw[] to check if any 
		pitstops need to be drawn/
	*/
	this.drawPitstops = function(){
		for(var i = 0; i < this.pitstop_laps_draw.length; i++){
			lap = this.pitstop_laps_draw[i];
			var x = WIDTH/2 + (this.radiusPos) * Math.cos( degToRad(( -90 + (lap * LAP_ANGLE - (LAP_ANGLE / 2)) )) );
			var y = HEIGHT/2 + (this.radiusPos) * Math.sin(degToRad(( -90 + (lap * LAP_ANGLE - (LAP_ANGLE / 2)) )));

			ctx.beginPath();
			ctx.fillStyle = this.driverColor;
			ctx.arc(x, y, (CAR_WIDTH / 2) + 1, 0, 2 * Math.PI, false);
			ctx.fill();
			ctx.lineWidth = 0.5;
		    ctx.strokeStyle = 'black';
		    ctx.stroke();
			ctx.fillStyle = '#FAFAFA';
			ctx.textAlign = 'center';
			ctx.font = 'bold ' + (CAR_WIDTH - 1) + 'px Helvetica';
			ctx.fillText('P', x, y + CAR_WIDTH / 3);
			ctx.closePath();
		}
	};

	/*
		Checks to see if any pitstops occured in the previous lap. If so, they are added to the
		pitstops_laps_draw[] list so that they will be drawn. The previous lap is checked, that way during the simulation the pitstop is drawn after the driver has passed it. It looks better this way.
	*/
	this.checkPitted = function(){
		for(var i = 0; i < this.pitstops.length; i++){
			if(pitstops[i].lap == (this.curLap - 1)){
				this.pitstop_laps_draw.push(this.curLap - 1);
			}
		}
	};

	/*
		Checks if the driver has finished the current lap, if so the proper variables are incremented.
		It also checks if the driver is retired within the upcoming lap.
	*/
	this.checkLapped = function(){
		//If the racer reaches the end of the track/canvas, move them to the start of the canvas
		if(this.posAngle >= (LAP_ANGLE * this.curLap) - 90 && !this.retired){
			this.curLap += 1;
			this.checkPitted();
			this.check_retired();
			this.updateSpeed();	
		}	
	};

	/*
		Draws the white circle for the driver. 
	*/
	this.drawRacerHead = function(){
		var x = WIDTH/2 + (this.radiusPos) * Math.cos(degToRad((this.posAngle)));
		var y = HEIGHT/2 + (this.radiusPos) * Math.sin(degToRad((this.posAngle)));
		

		ctx.beginPath();
		ctx.fillStyle = "#FAFAFA";
		ctx.arc(x, y, (CAR_WIDTH / 2) + 1, 0, 2 * Math.PI, false);
		ctx.fill();
		ctx.closePath();
	};

	/*
		Draws the final postion number when the driver has retired
	*/
	this.drawFinalPostion = function(){
		var x = WIDTH/2 + (this.radiusPos) * Math.cos(degToRad((this.posAngle)));
		var y = HEIGHT/2 + (this.radiusPos) * Math.sin(degToRad((this.posAngle)));
		ctx.beginPath();
		ctx.fillStyle = 'black';
		ctx.textAlign = 'center';
		ctx.font = 'bold ' + (CAR_WIDTH - 1) + 'px Helvetica';
		ctx.fillText(this.results.fields.positiontext, x, y + CAR_WIDTH / 4);
		ctx.closePath();
	};

	/*
		Draws the driver's arc path, indicating where along the race he is.
		If the driver is not retired, then he continues on as usual.
		Otherwise, his path is drawn as it was before he retired and his position
		is drawn on the white-circular driver indicator.
	*/
	this.drawRacer = function(){
		if(!this.retired){

			ctx.beginPath();
			ctx.arc(WIDTH / 2, HEIGHT / 2, this.radiusPos, degToRad(-90), degToRad(this.posAngle), false);
			ctx.lineWidth = CAR_WIDTH;
			ctx.strokeStyle = this.driverColor;
			ctx.stroke();
			ctx.closePath();
			this.drawPitstops();
			this.drawRacerHead();
		}
		else{

			ctx.beginPath();
			// if the driver retires immediately, then display an arc that is halfway
			// through the lap to better show the arc and its color
			if(this.totalLapCount == 0)
				ctx.arc(WIDTH / 2, HEIGHT / 2, this.radiusPos, degToRad(-90), degToRad(-87), false);
			else
				ctx.arc(WIDTH / 2, HEIGHT / 2, this.radiusPos, degToRad(-90), degToRad(this.posAngle), false);
			ctx.lineWidth = CAR_WIDTH;
			//ctx.strokeStyle = this.driverColor;
			ctx.strokeStyle = this.driverColor;
			ctx.stroke();
			ctx.closePath();
			this.drawPitstops();
			this.drawRacerHead();
			this.drawFinalPostion();
		}
	};
	
	/*
		Checks if the driver has finished the race. If so, various driver state variables are changed and DOM manipulation methods are called. The jQuery here is used to draw the statistics and driver position
		on the driver legend next to the simulation.
	*/	
		this.check_retired = function(){
		if(this.curLap > this.totalLapCount && this.retired == false){
			this.retired = true;
			retiredDriverCount += 1;
			$('#' + this.codeName + '_Status').html(this.curStatus);
			$('#' + this.codeName + '_Position').html(this.results.fields.positiontext);
			$('#' + this.codeName + '_Position').removeClass("hidden");
		}
	};
};

/*
	Method that creates a list of the specified driver's laptimes.
	@param driver id/pk
	@return list of laptimes
*/
function get_laptimes(driverid){
	var laptimeslist = [];
	for(var i = 0; i < json_laptimes.length; i++){
		if(json_laptimes[i].fields.driverid == driverid)
			laptimeslist.push(json_laptimes[i].fields);
	}
	return laptimeslist;
}
/*
	Returns the specified driver's result json object.
	@param driver id/pk
	@return driver's result json,
			otherwise NULL
*/
function get_driver_results(driverid){
	for(var i = 0; i < json_results.length; i++){
		if(json_results[i].fields.driverid == driverid)
			return json_results[i];
	}
	// If there are no results, for some reason, return a null
	return null;
}

function get_pitstops(driverid){
	var pitstoplist = [];

	for(var i = 0; i < json_pitstops.length; i++){
		if(json_pitstops[i].fields.driverid == driverid){
			pitstoplist.push(json_pitstops[i].fields);
		}
	}
	return pitstoplist;
}

function set_lap_length(){
	return (WIDTH / TOTAL_CIRCUIT_LAPS);
}


function get_final_status(driver){
	for(var i = 0; i < json_status.length; i++){
		if(json_status[i].pk == driver.results.fields.statusid){
			if(json_status[i].pk == 1){
				//Taking advantage of access to the driver status to get the total lap count at a circuit
				if(TOTAL_CIRCUIT_LAPS == 0){
					TOTAL_CIRCUIT_LAPS = driver.totalLapCount;
					LAP_ANGLE = 360 / TOTAL_CIRCUIT_LAPS;
				}
			}
			return json_status[i].fields.status_name;
		}
	}
	return null;
}

function set_driver_color(){
	var r = Math.floor(Math.random() * (255));
	var g = Math.floor(Math.random() * (255 - 100) + 100);
	var b = Math.floor(255);
	return 'rgb(' + r + ', ' + g + ', ' + b + ')';
}


// Creates all the driver  objects based on the json file given at the start
function create_drivers(){
	for(var i = 0; i < json_drivers.length; i++){
		var driverFields = json_drivers[i].fields;
		var newDriver = new FormulaDriver(driverFields.surname, driverFields.code, json_drivers[i].pk, get_driver_results(json_drivers[i].pk), get_laptimes(json_drivers[i].pk), get_pitstops(json_drivers[i].pk));
		newDriver.radiusPos = (TRACK_RADIUS * 0.99) - ((CAR_WIDTH + 4)*(i + 1));
		newDriver.driverCircum = (2 * Math.PI * newDriver.radiusPos);
		newDriver.curStatus = get_final_status( newDriver );
		newDriver.lapLength = set_lap_length();
		//newDriver.driverColor = set_driver_color();
		newDriver.driverColor = driverColorSpectrum[i];

		// NULL check in place for when the race is first loaded/ this prevents 
		// breaking when restarting the same race
		if(document.getElementById(newDriver.codeName) == null){
			// DOM manipulation to assgign the colors to the drivers
			document.getElementById('Drivers_List').querySelector('#Driver_Color_Legend').id = newDriver.codeName;
			document.getElementById(newDriver.codeName).style.background = newDriver.driverColor;

			// DOM manipulation to assign status spans to drivers
			document.getElementById('Drivers_List').querySelector('#Driver_Status_Legend').id = newDriver.codeName + "_Status";
			// DOM manipulation to assign position spans to drivers
			document.getElementById('Drivers_List').querySelector('#Driver_Position_Legend').id = newDriver.codeName + "_Position";
		}
		newDriver.driverStatsSpan = document.getElementById(newDriver.codeName + "_Status");
		newDriver.driverPositionSpan = document.getElementById(newDriver.codeName + "_Position");
		simulation_drivers.push( newDriver );
		
	}
	//simulation_drivers = orderOnGridPos(simulation_drivers);
}


// Checks if all drivers have retired/finished
// if finished, return true
// else return false
function isRaceFinished(){
	if(retiredDriverCount >= simulation_drivers.length){
		simulationCompleted = true;
		return true;
	}
	else{
		return false;	
	}
}

	

	function drawCircleTrack(){
		ctx.fillStyle = "rgba(82, 82, 82, .1)";

	ctx.beginPath();
	ctx.arc(WIDTH / 2, HEIGHT / 2, TRACK_RADIUS, 0, 2 * Math.PI, false);
	ctx.fill();
	ctx.closePath();
	}

	function drawLapLines(){
		for(var i = 0; i < TOTAL_CIRCUIT_LAPS; i++){
			var x = WIDTH/2 + (TRACK_RADIUS + 10) * Math.cos(degToRad(-90 + (LAP_ANGLE * i)));
		var y = HEIGHT/2 + (TRACK_RADIUS + 10) * Math.sin(degToRad(-90 + (LAP_ANGLE * i)));
		ctx.beginPath();              
		ctx.lineWidth = 1;
		ctx.strokeStyle = "#6D6E63";  
		ctx.moveTo(WIDTH / 2, HEIGHT / 2);
		ctx.lineTo(x, y);
		ctx.stroke();  
		
		ctx.fillStyle = '#DADADA';
		ctx.textAlign = 'center';
		ctx.font = '' + (CAR_WIDTH) + 'px Helvetica';

		ctx.fillText(i + 1, x, y + CAR_WIDTH / 4);
		ctx.closePath();
	}
	}

	function drawCheckeredLine(){
		for(var i = 0; i < TRACK_RADIUS; i+=3){
			ctx.beginPath();
			if( i % 2 == 0){
				ctx.fillStyle = '#fafafa';
				ctx.fillRect(WIDTH/2 - 1, HEIGHT/2 - i, 1,3);
				ctx.fillStyle = 'black';
				ctx.fillRect(WIDTH/2, HEIGHT/2 - i, 1,3);
			}
			else{
				ctx.fillStyle = 'black';
				ctx.fillRect(WIDTH/2 - 1, HEIGHT/2 - i, 1,3);
				ctx.fillStyle = '#FAFAFA';
				ctx.fillRect(WIDTH/2, HEIGHT/2 - i, 1,3);
			}
			ctx.closePath();
		}
	}


	// Var to hold animation ID so that it can be cancelled when simulation
	// is complete or paused
	var animationID = null;
	var raceInterval = null;

	function draw(){
	// Clears the canvas so that old stuff doesn't remain
	ctx.clearRect(0,0, WIDTH, HEIGHT);

	// Draws the background track
	drawCircleTrack();

	// Draws the track lap lines
	drawLapLines();
	drawCheckeredLine();
	

	// Loop through drivers to draw them
	for(var i = 0; i < simulation_drivers.length; i++){
		simulation_drivers[i].drawRacer();	
	}

	// Checks to see if the racr is finished, if so stop all animations
	// and calculations
	if(isRaceFinished()){
		window.cancelAnimationFrame(animationID);
		clearInterval(raceInterval);
	}
	else{
		animationID = requestAnimationFrame(draw);
	}
	
}

// Move logic loop
function simulate(){
	for(var i = 0; i < simulation_drivers.length; i++){
		simulation_drivers[i].move();
	}
}


function startSimulation(){
	//Creates drivers for simulation
	if(simulationCompleted){
		simulationCompleted = false;
		simulationPaused = false;
		if(simulation_drivers.length == 0)
			create_drivers();
		animationID = window.requestAnimationFrame(draw);
		raceInterval = setInterval(function(){simulate();}, 1);
		document.getElementById('Start_Pause_Btn').innerHTML = 'Pause';
	}
	else if(simulationPaused){
		//Resume if paused
		simulationPaused = false;
		animationID = window.requestAnimationFrame(draw);
		raceInterval = setInterval(function(){simulate();}, 1);
		document.getElementById('Start_Pause_Btn').innerHTML = 'Pause';

	}	
	else{
		pauseSimulation();
	}
}

function pauseSimulation(){
	if(animationID != null || raceInterval != null){
		simulationPaused = true;
		window.cancelAnimationFrame(animationID);
		clearInterval(raceInterval);
		animationID = null;
		raceInterval = null;
		document.getElementById('Start_Pause_Btn').innerHTML = 'Resume';

	}
}


function restartSimulation(){
	//Stop simulation and animation loops
	simulationCompleted = true;
	simulationPaused = false;
	
		window.cancelAnimationFrame(animationID);
		clearInterval(raceInterval);
	
	//Clear the canvas
	ctx.clearRect(0,0, WIDTH, HEIGHT);
	//Clearing status text from relavent DOM elements
	$('.driver-status').html("");
	$('.driver-position-circles').html(" ");
	$('.driver-position-circles').addClass('hidden');

	//Clear Drivers list
	simulation_drivers.length = 0;
	retiredDriverCount = 0;
	//Restart
	startSimulation();
}

$( window ).ready(startSimulation());
