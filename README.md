# Highway
A simple game created in Python with Pygame about driving a car, collecting coins, and dodging oncoming vehicles.

![Highway Gameplay](https://github.com/SlyFox2603/Highway/assets/101604309/10f1b799-0d6e-466b-8a0c-3c1993bb7296)

## Build Instructions
The code can be run directly from an IDE assuming you have Python and Pygame installed.
However, if you want to build an executable file, here is one way to do that:

1. In command prompt, install Pyinstaller using the command `pip install pyinstaller`
2. Navigate to the directory where you saved the source
3. In command prompt, run the command `pyinstaller --onefile Highway.py`

By following these steps, the executable file will appear in the "<ins>dist</ins>" folder within the main directory.
Once the file has been built, you can delete the "<ins>build</ins>" folder and "<ins>Highway.spec</ins>" file that's been created.
Make sure that you move the executable file out of the "<ins>dist</ins>" folder into the main directory with the "<ins>Sounds</ins>" and "<ins>Textures</ins>" folders.
Once you've done this, you can delete the "<ins>dist</ins>" folder as well.
