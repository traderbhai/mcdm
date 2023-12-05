# Multi-Criteria Decision Making

[![building - Poetry](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/python-poetry/website/main/static/badge/v0.json)](https://python-poetry.org/)
[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![code style - Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![imports - isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![types - pyright](https://img.shields.io/badge/types-pyright-blue.svg)](https://github.com/microsoft/pyright)

## Overview

In today's complex world, inundated with countless choices, making informed decisions is more critical than ever. This project introduces a multi-criteria decision analysis tool powered by Python and Streamlit, harnessing the potential of the TOPSIS method.

**TOPSIS**, or the *Technique for Order of Preference by Similarity to Ideal Solution*, stands out as a prime method for multi-criteria decision analysis. It is designed to pinpoint the optimal solution among a range of alternatives, keeping multiple criteria or attributes in mind. The core philosophy of TOPSIS lies in spotting solutions that inch closest to the ideal solution while distancing themselves from the anti-ideal or negative-ideal solution.

## Features

- [x] Built with **🐍Python**.
- [x] Web interface powered by **Streamlit**.
- [x] Implements the **TOPSIS** method for decision making.

## Installation & Usage

### 1. **Clone the Repository:**

To get started, first clone the repository to your local machine:

```bash
git clone https://github.com/LuxF3rre/mcdm
```

### 2. Navigate to the Project Directory:
Change your directory to the cloned repository:

```console
cd mcdm
```

### 3. Install Dependencies:
Install all necessary dependencies using the following command:

```console
pip install -r requirements.txt
```

### 4. Run the App:
Launch the Streamlit app using:

```console
streamlit run ./src/mcdm_app/Home.py
```

### 5. Access the Webapp:
Upon successful execution, Streamlit will provide a local URL (http://localhost:8501/). Simply open this URL in your preferred browser and follow the on-screen instructions to use the app.

## References

For a deeper dive into the methodology and applications of TOPSIS:

- Hwang, C.L.; Lai, Y.J.; Liu, T.Y. (1993). "A new approach for multiple objective decision making". _Computers and Operational Research_. **20** (8): 889-899. [doi](https://en.wikipedia.org/wiki/Doi_(identifier) "Doi (identifier)"):[10.1016/0305-0548(93)90109-v](https://doi.org/10.1016%2F0305-0548%2893%2990109-v)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License
