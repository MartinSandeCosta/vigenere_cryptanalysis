# Vigenère cryptanalysis

Python3 algorithm to break Vigenère cypher [[2]](##References) with a given hash of the plain text based on the Kasiski method [[1]](##References)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Usage
*vigenere.py* module accepts several flag inputs. 

We implemented several heuristics described by the following optional flags --word-length, --key-length--threshold, --occurrences-threshold. These flags establish thresholds to reduce the search space; receiving default values of 4, 4 and 3 respectively. There may exist several specific input samples where default thresholds are not enough to propose a key since they limit the search space excesively. In such cases, new values for these flags may need to be proposed.

| Short  flag |        Long flag        | Input  type | Default  value |                                                           Description                                                           |
|:-----------:|:-----------------------:|:-----------:|----------------|:-------------------------------------------------------------------------------------------------------------------------------:|
|      -i     |         --input         |     File    |                |                                                            Input file                                                           |
|      -d     |       --dictionary      |     File    |                |                                                      Dictionary to be used                                                      |
|             |          --hash         |     File    |                |                                                  Hash to be used for comparison                                                 |
|     -wl     |      --word-length      |     int     |        4       |                                Length of words for occurrence  count in length guessing (Kasiski)                                |
|     -klt    |  --key-length-threshold |     int     |        4       |                                      Number of key length candidates  to examine (Kasiski)                                      |
|     -ot     | --occurrences-threshold |     int     |        3       | Number of top letters to examine for each column (Kasiski)  This value greatly increases  execution time inversely proportional |
|      -v     |        --verbose        |     None    |      False     |                                                           Verbose mode                                                          |


To use this repo, follow these steps:

* Clone this repository:
    ```
    $ git clone https://github.com/MartinSandeCosta/vigenere_cryptanalysis.git
    ```

* Run the following command to execute:
    ```
    $ python3 vigenere.py -i input -d dictionary --hash hash
    ```
    > If something goes wrong try increasing the optional flags
## Running the tests

The repo includes a script to run tests automatically
* Run the following command to execute:
    ```
    $ chmod +x run_tests.sh
    $ ./run_tests.sh
    ```

## Contributing
Feel free to contribute! :)

## Documentation
This project has been developed as part of the MSc. in Computer Science at Universidade da Coruña. 
The software is accompanied by a technical [document](https://drive.google.com/file/d/1m_kkz9YrUavHHtwmuF-GolTvH78VfON6/view?usp=sharing) which details its development. 

## Authors

* [Javier Garea Cidre](https://github.com/javiergarea)
* [Martín Sande Costa](https://github.com/MartinSandeCosta)

See also the list of [contributors](https://github.com/MartinSandeCosta/vigenere_cryptanalysis/graphs/contributors) who participated in this project.

## License

This project is licensed under MIT License

## References

\[1\] Kasiski, F. W. 1863. Die Geheimschriften und die Dechiffrir-Kunst. Berlin: E. S. Mittler und Sohn

\[2\] Lyons, J. 2016. *pycipher*. GitHub repository: https://github.com/jameslyons/pycipher
