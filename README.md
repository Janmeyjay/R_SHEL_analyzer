# R_SHEL Analyzer

## Description

R_SHEL Analyzer is a powerful application designed for Retro SHEL beam analysis. It processes images captured in Retro reflected SHEL experiments, extracts the region of interest, and calculates the center of mass and intensity. The application provides real-time plotting and visualization of the results, enabling users to track changes in the beam's position and strength. With customizable settings and the ability to export processed data to file_name.dat, R_SHEL Analyzer offers a comprehensive solution for researchers and scientists in the field of beam analysis.

Additionally, R_SHEL Analyzer allows users to create an executable file for convenient and easy distribution. By using the provided setup.py script and the cx_Freeze library, users can package the application as an executable, making it accessible and executable on Windows systems without the need for Python or additional dependencies. This feature enables users to share the application with others, even those without Python or the required libraries installed, providing a seamless experience for analyzing Retro SHEL beam experiments.

## Features

- Image processing and analysis
- Real time interaction
- Center of mass calculation
- Intensity measurement
- Plotting and visualization
- Customizable settings
- Exporting results to file_name.dat

## Getting Started

To use R_SHEL Analyzer, follow these steps:

1. Clone the repository: `git clone [**https://github.com/Janmeyjay/R_SHEL_Analyzer.git**](https://github.com/Janmeyjay/R_SHEL_Analyzer.git)'
2. Install the required dependencies: `**pip install -r requirements.txt**`
3. Run the application: `**python R_SHEL_Analyzer.py**`

## Creating an Executable (Windows Only)

To create an executable of the R_SHEL Analyzer application, you can use the `cx_Freeze` library along with the provided `setup.py` script. Follow the steps below:

1. Make sure you have `cx_Freeze` installed. If not, you can install it using `pip`:
2. Create a `setup.py` file in the same directory as your `R_SHEL_Analyzer.py` script. Use the following code in the `setup.py` file (see the provided setup.py in the repository).
3. Open a command prompt or terminal, navigate to the directory containing the `setup.py` file and the `R_SHEL_Analyzer.py` script.
4. Run the following command to build the executable.
5. After the build is complete, you will find a new directory named `build` in the same location. Inside the `build` directory, there will be another directory with the name of the target platform (e.g., `win-amd64` for 64-bit Windows).
6. Inside the platform-specific directory, you will find the `R_SHEL_Analyzer.exe` executable.

## Caution
- R_SHEL Analyzer requires the input images to be in a specific format. Make sure the image names follow the format '**img0_0_*.png**', where '*' represents any characters after the specified format.

## Dependencies
The following dependencies are required to run the R_SHEL Analyzer:

- Python 3.x
- PyQt5
- OpenCV
- NumPy
- SciPy
- Matplotlib

## Usage

1. Launch the application by running the '**R_SHEL_Analyzer.py**' script or double clicking the '**R_SHEL_Analyzer.exe**'.
2. Browse and select a folder containing images and data files by clicking the "Browse Folder" button.
3. Enter the central image number, x and y center, region of interest, shift in region of interest, and angle of rotation.
4. Click the "Process Images" button to start the image processing.
5. The processed data will be saved in a file with the given name

## How to Contribute

Contributions to R_SHEL Analyzer are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE.txt) file for details.

## Contact

For any questions or inquiries, please contact the project creator:
- Name:  Janmey Jay Panda
- Email: [janmeyjay12@gmail.com](mailto:janmeyjay12@gmail.com)

## Please Don't Forget to Cite!
If you find R_SHEL Analyzer helpful for your research or work, we kindly request that you cite the project's GitHub repository: [R_SHEL Analyzer on GitHub](https://github.com/Janmeyjay/R_SHEL_analyzer)

We appreciate your support and contribution to the project!
