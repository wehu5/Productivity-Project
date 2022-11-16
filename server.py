from flask import Flask, render_template, Response
from imutils.video import VideoStream
import threading
import os
from pathlib import Path
from GazeTracking.gaze_tracking import GazeTracking
import time
import cv2
parent_path = Path.cwd()
path_ = os.path.join(parent_path, "GazeTracking/example.py")
gaze = GazeTracking()

### start
start = False

def gen_frames():  # generate frame by frame from camera
    print('gen_frames')
    global start
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    frame_rate = 30
    frame_height = int(camera.get(4))
    frame_width = int(camera.get(3))
    frame_counter = 0
    while start:
        # Capture frame-by-frame
      success, frame = camera.read()  # read the camera frame
      if not success:
        continue
      else:
        gaze.refresh(frame)
        frame = gaze.annotated_frame()
        frame = cv2.flip(frame, 1)
        text = ""

      if gaze.is_right():
        print("Right")
        text = "Looking right"
      elif gaze.is_left():
        print("Left")
        text = "Looking left"
      elif gaze.is_up():
        print("Up")
        text = "Looking Up"
      elif gaze.is_down():
        print("Down")
        text = "Looking Down"
      elif gaze.is_center():
        print("Center")
        text = "Looking center"

      if gaze.is_blinking():
        text = "Blinking"

      cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

      left_pupil = gaze.pupil_left_coords()
      right_pupil = gaze.pupil_right_coords()
      cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
      cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
      ret, buffer = cv2.imencode('.jpg', frame)
      frame = buffer.tobytes()
      yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
    camera.release()

### end

app = Flask(__name__)

@app.route('/')
def index():
  global start
  start = False
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  #webcam = cv2.VideoCapture(0)
  #_, frame = webcam.read()
  global start
  start = True
  return render_template('my-link.html')

@app.route('/video_feed')
def video_feed():
  return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
  #print("Hello")
    # Video streaming route. Put this in the src attribute of an img tag
    #return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(debug=True)