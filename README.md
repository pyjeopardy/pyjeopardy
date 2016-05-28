Dependencies
============

* python3
* python3-pyqt5
* python3-pyqt5.qtmultimedia
* python3-serial

Start
=====

Simply execute ./run.sh on Linux.

On other systems you have to run the pyjeopardy module: python3 -m pyjeopardy

Creating rounds
===============

A round is defined in one JSON file with the following structure:

    {
        "name": "Example round",
        "categories": [
            {
                "name": "Test 1",
                "answers": [
                    {
                        "answer": "42",
                        "question": "Cool?",
                        "doublejeopardy": false
                    },
                    {
                        "answer": "43",
                        "question": "Uncool?",
                        "doublejeopardy": true
                    }
                ]
            },
            {
                "name": "Test 2",
                "answers": [
                    {
                        "image": "imgs/lol.png",
                        "question": "Foo bar?",
                        "doublejeopardy": false
                    },
                    {
                        "audio": "imgs/fanzy.mp3",
                        "question": "Baz?",
                        "doublejeopardy": true
                    },
                    ...
                ]
            },
        ]
    }

There can be as many categories as you wish, the limit is the width of your
monitor. The number of answers per category is also variable and can even vary
for each category.

This are the possible answer types:

 * answer (simple text)
 * image
 * audio

The path to the images or audio files must be relative to the JSON file.

An example can be found in answers/example.json.

**Note: the double jeopardy is not implemented at the moment.**

License
=======

pyjeopardy - jeopardy game
Copyright (C) 2015  Sven Hertle

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
