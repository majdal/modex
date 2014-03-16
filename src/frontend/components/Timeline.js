Crafty.c('AddScenario', {
  scenarioCount: 1, // the total number of scenarios
  length: 10, // how many years is the scenario for?
  scenarios: [],

  init: function() {
    var self = this;
    // make sure that we have all the entities required
    this.requires('2D, Canvas, Mouse, plusButton');

    // position the button at the bottom of the page
    var positionY = Crafty.viewport.height-110;

    this.attr({x: 20, y: positionY, w: 100, h: 100})
        // to create a new scenario/timeline, press this button
        .bind('Click', function(e){
          var scenario = new Crafty.e('Timeline').timeline(self.scenarioCount);
          self.scenarioCount = self.scenarioCount+1;
          self.scenarios.push(scenario);
        });
  },

  yearInPixels: function(xCoord) {
    var year = 700/this.length;
    //         width in pixels / total number of years
    return Math.floor(xCoord/year);
  }, 

  serialize: function() {
    return $.map(this.scenarios, function(element){return element.serialize()} );
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
      var intervention = new Crafty.e('Tax').tax(taxYear, e.x, this.positionY); 
      this.interventions.push(intervention);
    });
  },

  timeline: function(scenarioCount) {
    this.scenarioCount = scenarioCount;
    this.interventions = [];
    var positionY = Crafty.viewport.height - this.scenarioCount*10 - this.scenarioCount*25;
    //              viewport height        - padding               - timeline height
    this.positionY = positionY-20; // align the bottom timeline with the plus button. 
    this.attr({x: 150, y: this.positionY, w: 700, h: 25});
    return this; 
  }, 

  serialize: function() {
    var interventions = $.map(this.interventions, function(element){return element.serialize()} )
    //this.interventions
    return {'scenarioCount': this.scenarioCount,
            'scenarioName': this.scenarioName,
            'interventions': interventions,
        }
  }
});


Crafty.c('Tax', {
  year: 0, // year that the tax is implemented 
  tax_value: 0, 

  init: function() {
    this.requires('2D, Canvas, Color, Mouse');
    this.bind('Click', function(e){
          Crafty.e('InterventionDialogue').interventionDialogue(this);
        });
  }, 

  tax: function(year, xCoord, yCoord) {
    this.year = year;
    this.attr({x: xCoord-2, y: yCoord, w: 4, h: 25}) // put a little red tick mark on the timeline wherever the click is. 
        .color('red');
    Crafty.e('InterventionDialogue').interventionDialogue(this);
    return this;
  },

  serialize: function() {
    return {'year': this.year,
            'tax_value': this.tax_value, 
            'activity': this.activity,
        }
  }
});

Crafty.c('InterventionDialogue', {
  init: function() {
    this.requires('2D, DOM, Color, Mouse');
  },

  interventionDialogue: function(intervention) {
    this.intervention = intervention;
    this.attr({x: 100, y:100, w: 300, h: 200})
        .css({'background-color': 'red',
              'color': 'black'
        });
    this.createDialogue(intervention, this);
    return this;
  },

  createDialogue: function(intervention, self) {
    $("#dialogue").dialog({
      width: 420,
      modal: true,
      buttons: [        
        {
          text: "Delete",
          click: function() {
            $(this).dialog("destroy");
            // TODO send code to backend to delete this particular intervention
            intervention.destroy();
          }
        },
        {
          text: "Save",
          click: function() {
            if (!$('#activity').val()) { // if the activity is not selected
              alert('Please select an activity first!');
            } else {
              intervention.tax_value = $('#tax_slider').slider('value');
              intervention.activity = $('#activity').val();
              //intervention.year = $('#year_slider').val();
              self.destroyDialogue();
              // TODO send code to backend to create an intervention
            }
          }
        }
      ]
    });
    $('#intervention_type').change(function(){
      var interventionType = $(this).val();
      if (interventionType == 'tax') {
        $('#intervention_unit').text('%');        
      } else if (interventionType == 'subsidy') {
        // TODO this should change to $ and change the slider to an <input> with numbers only 
        $('#intervention_unit').text('%');
      }
    });
    $('#tax_slider').slider({
      slide: function(event, ui) {
        $('#intervention_value').text(ui.value);
        // ui.value is a value between 0 and 100% - representing the possible tax value
      }
    });
/*
    $("#year_slider").slider({
      min: 0,
      max: plusButton.length,
      step: 1,
      slide: function(event, ui) {
        $('#year_value').text(ui.value);
        // ui.value is a value between 0 and 100% - representing the possible tax value
      }
    });
*/
  },

  destroyDialogue: function () {
    $('#activity').val('')
    $('#dialogue').dialog('destroy');
    $('#tax_slider').slider('destroy');
  }
});