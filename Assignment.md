
Your task is to construct a component implementing the logic of board game AZUL. These are the [rules](https://www.wikihow.com/Play-Azul).

## Design

I prepared a [design](design.png) template for your implementation. The interaction with the game consists of a single `take` call that both specifies from where and which the tiles should be taken and where to put them. Incorrect tile description should yield false return value and do nothing. Incorrect destination description should result in tiles falling to the floor (Note that this simplifies the design a lot, otherwise TableArea needs to handle "undos" or something similar). To see how to use this component to create a working game see [this diagram](architecture.pdf) depicting possible such architecture.

Note that the design is by no means complete. Most notably
- You have to add appropriate constructors. Chose your constructors in a way that enables good testing. E.g., it is a good idea to allow creating WallLines that already have some stones on it.
- You have to add interfaces that separate classes that need to be separated.
- You probably want to do something with Bag class to handle the randomness involved better.
- FinalPointsCalculator is a good candidate to apply Composite pattern.
Also, it is highly likely, that I overlooked something.

I recommend to stick to the following timeline
- 11. 11. create teams, understand game rules, understand the design (so we can have a meaningful discussion on the lecture).
- 20. 11. the common part of the project is finished 
- 27. 11. you are done

## Implementation remarks

You should build your project either in Python or in Java. I started the projects for you, including several tools that might help you. See [pts1-23-python](https://github.com/relatko/pts1-23-python) and [pts1-23-java](https://github.com/relatko/pts1-23-java). Note that if you use Python, your code should be type annotated and mypy --strict should show no errors.

This is a fairly large project and it would take too long to implement. Thus you will collaborate while implementing the project.

* Create groups of, ideally, four to six people. and fork the repository you agree to use. Floor class is already implemented by me.
* Collaboratively implement the elements marked white (trivial) and red. For each red element create a PR, discuss it and merge it into the master. Red classes are not of particular interest to me. The amount of points given here is quite limited (up to 10 points), so do not overthink stuff. This also implies that the test coverage does not have to be great in these classes.
* After this, you should add your own implementation of the remaining classes (including unit tests) and prepare three integration tests, first covering TableArea with its collaborators, second covering Board with its collaborators (without UsedTiles class), and third covering the whole component. To reduce the amount of work necessary, it is sufficient to create one end to end scenario for each of these integration test. Unit tests for Game should be solitary. Do a sociable unit test of PatternLine that also uses Floor. You can discuss technical aspects of the implementation, but everybody should implement the blue classes and the integration tests on his own. You can either work on local machine or use a private repository for your effort.

You should use Git and produce a reasonable history of commits. Note that to work on the blue classes you do not need the red ones. You are also free to adjust the implementation of red classes according to the needs of your project (but, the changes, hopefully should not be large, a good example is changing interface name, adding a new interface, ...).

## Instructions for submitting your project

Send your solution to [lukotka.pts@gmail.com](lukotka.pts@gmail.com). The deadline is 29.11.2022 23:59:59. The solutions sent later will be accepted, however the number of points awarded may be reduced.

Send the solution to me either as compressed folders containing the whole repository (including the hidden git files) or as a link to private repository with read access granted (GitHub handle `relatko`). Attach a link to the public repository, where you and your team built the common part of the project. 


