# ReMi: A Reservoir Computing MIDI Arpeggiator for Ableton

This project was developed during the [Hack'1'Robo hackathon](https://sites.google.com/view/hack1robo/projets) and received special recognition from the jury.

## Presentation

**ReMi** provides the following features:
* Generate arpeggios with a [Reservoir Computing](https://en.wikipedia.org/wiki/Reservoir_computing)  neural network
* Control reservoir hyperparameters in real time through MIDI
* Visualise reservoir states and processing steps in real time

## Usage

1. **Add**  _remi.amxd_ to a MIDI Ableton track
2. **Run** _app.py_ to start communication between Max for Live and Python
3. **Run** _liveplot.py_ to visualise reservoir states
4. **Run** _gui.py_ to visualise processing steps
5. **Press keys**, and enjoy riding the edge of chaos :)

## Future features

Here are some useful features that could be implemented in the future. Don't hesitate to either help us implementing them or propose some new ideas!

- [ ] Add a pulse as an extra input to the reservoir, control its gain and periodicity. A more sophisticated approach would be to add a step sequencer as input (multiple pulses with their own rhythmic pattern).
- [ ] Add a parameter that controls the probability of playing no note (silence). Currently, silence is represented in the same way as a note. Hence its probability of being selected for the beat cannot be differentially modulated.


## 

![image](https://github.com/HugoChateauLaurent/remi/assets/26091283/7dc9542b-a040-4572-b4d6-b8a20356d439)
