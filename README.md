# Thype
A tenkey-style layout analyser

## What is tenkey
For those unaware, tenkey is a type of keyboard layout (originally) for typing japanese text on mobile. 
The motivation for tenkey was originally to fit all 4X hirigana characters onto a small phone keyboard,
but AKL saw potential for it for typing english and have created several layouts that make use of this
technology.

## The analyser
This analyser has no frontend, and you will have to directly alter the python code to add layouts.
The comments should be self-explanatory, if not, talk to @5quidwyrm on the AKL server.

## Stat definitions
- Taps -> Number of letters typed
- Swipes -> Number of swipe motions made
- Total squared distance & distance -> Self-explanatory
- Average distance (per bigram) -> Self-explanatory
- Standard deviation (per bigram) -> Self-explanatory
- Average inness:
  - Inness is defined as follows:
    - Down -> 0.5
    - In -> 0.5
    - Up -> -0.5
    - Out -> -0.5
  The innesses are added up and divided by how many bigrams there are
- Easy and hard bigrams:
  - These are bigrams with travel distance of 2 standard deviations below and above the mean respectively.
