Crafty.c('AddScenario', {
  scenarioCount: 1, // the total number of scenarios
  length: 10, // how many years is the scenario for?

  init: function() {
    var self = this;
    // make sure that we have all the entities required
    this.requires('2D, Canvas, Mouse, plusButton');

    // position the button at the bottom of the page
    var positionY = Crafty.viewport.height-110;

    this.attr({x: 20, y: positionY, w: 100, h: 100})
        // to create a new scenario/timeline, press this button
        .bind('Click', function(e){
          new Crafty.e('Timeline,').timeline(self.scenarioCount);
          self.scenarioCount = self.scenarioCount+1;
        });
  },

  yearInPixels: function(xCoord) {
    var year = 700/this.length;
    //         width in pixels / total number of years
    return Math.floor(xCoord/year);
  }
});


Crafty.c('Timeline', {
  scenarioCount: 1, // the ordinal number of the scenario
  scenarioName: '',
  positionY: 0, // keeping track  of the y position of the timeline, for reference 

  init: function() {
    this.requires('2D, Canvas, Color, Mouse, timelineBackground');

    this.bind('Click', function(e) {
      var taxYear = plusButton.yearInPixels(e.x);
      var intervention = new Crafty.e('Tax').tax(e.x, this.positionY, taxYear); 
      this.interventions.push(intervention);
    });
  },

  timeline: function(scenarioCount) {
    this.scenarioCount = scenarioCount;
    this.interventions = [];
    var positionY = Crafty.viewport.height - this.scenarioCount*10 - this.scenarioCount*25;
    //              viewport height        - padding               - timeline height
    this.positionY = positionY;
    this.attr({x: 150, y: positionY, w: 700, h: 25});
  }
});


Crafty.c('Tax', {
  year: 0,

  init: function() {
    this.requires('2D, Canvas, Color, Mouse');
    this.bind('Click', function(e){
          console.log(e);
        });
  }, 

  tax: function(xCoord, yCoord, year) {
    this.year = year;
    this.attr({x: xCoord-2, y: yCoord, w: 4, h: 25})
        .color('red');
    Crafty.e('InterventionDialogue').interventionDialogue();
  }
});

Crafty.c('InterventionDialogue', {
  init: function() {
    this.requires('2D, DOM, Color, Mouse');
  },

  interventionDialogue: function(){
    this.attr({x: 100, y:100, w: 300, h: 200})
        .css({'background-color': 'red',
              'color': 'black'
        });
    this.createDialogue();
  },

  createDialogue: function() {
    $("#dialogue").dialog({
      buttons: [
        {
          text: "Save",
          click: function() {
            $(this).dialog("destroy");
            // TODO send code to backend to create an intervention
          }
        },        
        {
          text: "Delete",
          click: function() {
            $(this).dialog("destroy");
            // TODO send code to backend to delete this particular intervention
          }
        },
      ]
    });
    $('#intervention_type').change(function(){
      var interventionType = $(this).val();
      if (interventionType == 'tax') {
        $('#intervention_unit').text('%');        
      } else if (interventionType == 'subsidy') {
        // this should change to $ and change the slider to an <input> with numbers only 
        $('#intervention_unit').text('%');
      }
    });
    $("#tax_slider").slider({
      change: function(event, ui) {
        $('#intervention_value').text(ui.value);
        // ui.value is a value between 0 and 100% - representing the possible tax value
      }
    });
  },

  destroyDialogue: function () {
    $("#dialogue").dialog("destroy");
    $("#tax_slider").slider("destory");
  }
});