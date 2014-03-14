This folder includes a number of simulations developed or used by our research group.

If Modex is successful, it will _usefully_ wrap all of these, even though they are diverse.

## Rough Taxonomy of Models

* Trivial: models with no meat to them, just to provide a baseline for input-output
  * beta.py
  * mlm.R
* Simple: for dynamics models, they should have less than 5 rules per step
  * EvilBankerSim
  * Dating (version 1) 
  * lightbulb
* Medium
  * Dating (version 2)
  * FarmSimulationModel (version 1)
* Large: models including a significant number of [lalala]
  * RegMAS
  * SLUCE
* Huge
  * farmsim (final modex version)

## Ideas

**mirror**
   a single image (eg a glowstick) projected onto a mirrored surface projecting into two eyes
     the controls are the orientation of a surface (so, theta, the horizontal angle, and rho, the vertical angle)
   output: one image (your sight) made of two images (your eyes) overlaid
     funny effects can happen! some angles have the image in sync and some have it split
       and the left eye's image can appear to the right of the right eye's image

Rating: medium 
  
Features:

 * Totally deterministic: (theta, rho) -> pixels (it doesn't even have complex feedback loops)
     but relatively high dimensional (2 real numbers) and difficult to sample automatically
      (though a human's intuition can move the mirror around a bit and get a feel for the rules: 'tilt this way when it's angled this way and it goes left, tilt the other way it goes right. tilt it out of its initial orientation and the image splits" etc)
 * A case for supporting 3d models (e.g. chemical structure, things that Modelica can do, laser-measured archeaology data)?
 * Should be relatively simple to write as a raytracer
 

model: SimIntrovert
 Agents
   Rules: people have a -1 to 1 introvert-extrovert scale
    people have a social network -- that is, people, and a level of closeness (comfortability?) with each person in that network
    there are Places: Work, School, Party, etc
    every tick people consider doing in this order:
      1) engage another person
      2) go to a different place
      3) nothing
    people prefer to engage people they already know, and in that set, they prefer to engage those they are close with
     people can not refuse to be engaged by someone on a single step (but they can leave next step)
     engagement is transitively closed: if A engages B and C engages A, then B and C are considered engaged for that step (=>cliques)
     engagement causes a social network link to be created
      (and maybe some rule that the sum of closeness for a single human has a maximum?)
      (and another rule that the closeness a human needs to be happy is the same for everyone, introverts and extroverts alike)
      (and another rule that each step subtracts closeness from everyone ; so, talking to someone is +1, not talking to them is -0.01)
   the more extroverted someone is, the more likely they are to decided to engage (+1 => 100% engage; -1 => P(Engage) = 1 - 100% ; 0 => P(Engage) = 50%)
     (TODO: the chance of engaging should depend on who is in the room)

Rating: simple

Features:
 * dynamic social network
 * simple

**Drug markets**

  * [NARCsim](http://staffwww.dcs.shef.ac.uk/people/D.Romano/Romano_NARCSim_ICE-GIC09.pdf)
  * [SimDrug](http://cormas.cirad.fr/en/applica/simDrug.htm) (2005) from the [DPMP](http://www.dpmp.unsw.edu.au/); see also their [up to date models](http://www.dpmp.unsw.edu.au/resource/model)
  * [Lee Hoffer](http://www.case.edu/artsci/anth/PublicationsPresentations.html) of the IDMS (e.g. see this [2009 paper](http://www.seiservices.com/nida/1014059/Materials/06%20Hoffer_Network_workshop.pdf)
    *  http://code.google.com/p/drug-market (in Repast)

**Dating**: a social network with utility functions determining "attractiveness", and some simple dynamics on that

**EvilBankerSim**

**SIR**


**Dumb random number generators**
**Dumb linear-model generators**
**Dumb non-linear model generators**
**Dumb multivariate random number generators with tunable cross-correlation**

**[SLUCE](http://sluce.wici.ca)**
**[FarmSimulationModel](https://github.com/n7wilson/FoodSimulationModel)**

**Conversion Events**: religious, tech, or other subculture
  * See the Lofland/Stark model, which is the dominant theory in Cult & New Religious Movement research
  * Related cite: Lorne L. Dawson. Comprehending Cults: The Sociology of New Religious Movements. Toronto: Oxford University Press. 1998
  * main mechanisms to test: a) internal strain, b) social networks c) 

**Thought Communities**: (related to the cult model)
  * the dynamics are driven (?) by the need to maintain ones own worldview
  * intution: the system dynamics when two thought communities bump up against each other are metastable (see "An explanation of 1/f noise" for def'n of _metastable_)
