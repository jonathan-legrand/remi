# ReMi: A Reservoir Computing MIDI Arpeggiator for Ableton

This project was developed during the [Hack'1'Robo hackathon](https://sites.google.com/view/hack1robo/projets) and received special recognition from the jury.

## Presentation

**ReMi** provides the following features:
* Generate arpeggios with a [Reservoir Computing](https://en.wikipedia.org/wiki/Reservoir_computing)  neural network
* Control reservoir hyperparameters in real time through MIDI
* Visualise reservoir states and processing steps in real time

## Usage

1. Add ```remi.amxd``` to a MIDI Ableton track
2. Run ```app.py``` to start communication between Max for Live and Python
3. Run ```liveplot.py``` to visualise reservoir states
4. Run ```gui.py``` to visualise processing steps
5. Press keys, and enjoy riding the edge of chaos :)

## Future features

Here are some useful features that could be implemented in the future. Don't hesitate to either help us implementing them or propose some new ideas!

- [ ] Add a pulse as an extra input to the reservoir, control its gain and periodicity. A more sophisticated approach would be to add a step sequencer as input (multiple pulses with their own rhythmic pattern).
- [ ] Add a parameter that controls the probability of playing no note (silence). Currently, silence is represented in the same way as a note. Hence its probability of being selected for the beat cannot be differentially modulated.

## Demo

This quick preliminary demo is just meant for you to hear what ReMi can sound like. Four keys were pressed constantly and the order of the notes was chosen by ReMi. Drums were not played by ReMi (although it could have).

_NB: Keep in mind that this is just an example. A Reservoir is a universal dynamical system approximator. ReMi could therefore generate any possible melody._

https://github.com/HugoChateauLaurent/remi/assets/26091283/ecacce90-4ec1-4b0d-9ea5-cdc79b8106c3

## 

![image](https://github.com/HugoChateauLaurent/remi/assets/26091283/7dc9542b-a040-4572-b4d6-b8a20356d439)
