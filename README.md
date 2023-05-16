# Farmbot - An ML Farm Autoer

A simple take on the farm script but using CV to identify points of interest. It works, but it's clearly still in a conceptual phase that needs some fleshing out...

## Packages Used

* pyautogui
* opencv
* numpy
* pytesseract
* pillow
* pywin32

## TODO

* Generate necessary resources via proportional cropping
* Using OCR to identify a long chain of numbers was a horrible idea. Modify the usage from a line to single elements identified by their unique symbols.
    * If not using OCR, provide end user a way to provide the values without having the OCR package (Tesseract OCR isn't exactly small...)
* Identify why key-downs do not seem to work. I know using the Windows API directly will have the guaranteed response, but identifying why pyautogui doesn't properly generate key responses could be useful.
* Convert magic sleep numbers in the bot file into user-adjustable parameters (proabably through const.py).

And probably some more, that I'm currently forgetting... Point is, the program is very finnicky, and at the moment even a DPI change can break it. There are a lot of things that need some refactoring/adjustment.