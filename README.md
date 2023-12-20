# Image detecting and matching seat with custom Yolov5

---
I created a program that attempts to match spots using our own custom yolo model.

I use detect.py to find the location of the rounding box and move.py and calculate.py to compare it to seat.txt, which is the coordinates of the seat at the camera position I fixed. 
and compare it to seat.txt, which is the coordinates of the seats from our fixed camera position. 

Seat matching uses IoU and eclidean distance. Initially, I compare IoU. This will have a value of 1 for most overlaps because the rounding box is very small.
This is because the overlap is caused by the environment, such as seating arrangement, camera angle, and other location limitations.
Therefore, even if an object occupies two spots due to 

And finally, for the instance with the most overlapping instances, i.e. the most instances of people sitting down, 
I adopt the photo from the last hour. adopt the last time photo and provide the seat information for that photo.





<img src = "sampleImages/seat.png" width="300" height="300"/>

Labeling images for our own matching spots for artesian places

<img src = "sampleImages/example.jpg" width="300" height="300"/>

When I ran detect.py with our custom yolomodel, I got the following result

<br/>

<img src = "sampleImages/log.png" width="500" height="300"/>
<img src = "sampleImages/result.png" width="500" height="300"/>

The detect process and the resulting value
<br/>
<br/>
<br/>

### Additional Comment

---

I also thought of dynamism, but I did it statically with one transmission camera (Raspberry Pi) and to show the result close to completion quickly.
If it is dynamically allocated, the chair behind it will not be visible if a person is currently sitting in front of it. 
In the case of humans, it is recognized because of its large size, but in the case of chairs, it is difficult to recognize and match, 
so the position of the chair was statically designated.

So, like a bird eye view camera, it can be executed in a position where you can see the whole thing from above, or by using multiple cameras 
so that there are no overlapping parts, it recognizes the chair and human class, modifies the algorithm 
I implemented between the chair and the human class, matches it with the IoU value, and in certain exceptions, 
I think it will be possible to solve it by matching the closer one with euclidean distance or creating the desired algorithm.


