# hope-autonomous-driving

#### Autonomous Driving project for Euro Truck Simulator 2

# Video:

[![working](thumbnail.png)](https://youtu.be/xuVT6097cig)

## How is it working ?

In this video, the program processes the image of the screen, gives it to the artificial intelligence model, turns the steering wheel according to the result.

![vision](1.png)
I drove the vehicle for 1 hour and also collected data and saved them in a CSV file. I trained the data in the CSV file using [the method and model in this link](https://vijayabhaskar96.medium.com/tutorial-on-keras-flow-from-dataframe-1fd4493d237c).   
The model gives us a pixel value equal to the steering angle of the steering wheel. Then the mouse is moved to this pixel value.

----

## I want to run this

There are things you need to do before running codes:
- You need to install Python ([I used version 3.7.9](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)),
- You have to install the components I use. If this is your first time using Python type in cmd:
```bash
python -m pip install -r requirements.txt
```
- Change the Windows cursor speed to 4
- ![cursor](cursor.jpg)
- Set the game to full screen and at 1280x720 resolution,
- Adjust your seat to be the same as in the picture,
- ![seat](2.png)
- Type in console ([enable console](https://forum.scssoft.com/viewtopic.php?t=61852)):
```bash
c_rsteersens 0.325500
```
- Align the steering wheel as centrally as possible,
- ![wheel](3.png)

Ready to go! Run the code and wait for the beep. (Press F1 to stop the code)

## Older Versions
They were driving the car using only the A and D keys. It was working with bunch of if-else' instead deep learning. 
  - [Version 1](https://www.instagram.com/p/CJ3B53Dp0hC/)
  - [Version 2](https://www.instagram.com/p/CJ_LCKqpxc_/)
  
## Limitations
Shadows can confuse the model [(for example this clip)](https://drive.google.com/file/d/1aLDsOZm6rvWgT6dJnb04MZIDKJk0hzMj/view?usp=sharing). To avoid this you can use high beams.  
The supervised learning model is powerful as dataset. If you use 5 or 10 hours of driving footage instead of 1 hour, the model performance will increase amazingly. If I do it before you do, I'll upload the model here ;)

## What's Next
  - :white_check_mark: Lane changing
  - :gear: Adaptive cruise control
  - Emergency brake
  - Export as exe file
  
## License
[MIT](LICENSE)
> Special thanks to r/trucksim subreddit. [You guys motivated me to improve this project.](https://www.reddit.com/r/trucksim/comments/kyiv2v/i_made_an_autosteering_project_with_python/)
