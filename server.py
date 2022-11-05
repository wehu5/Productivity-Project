from flask import Flask, render_template, Response
from imutils.video import VideoStream
import imutils
import os
from pathlib import Path
from GazeTracking import example
from GazeTracking.gaze_tracking import GazeTracking
import time
import cv2
parent_path = Path.cwd()
path_ = os.path.join(parent_path, "GazeTracking/example.py")
track = example.Video()
gaze = GazeTracking()

### start

# camera = cv2.VideoCapture('rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream')  # use 0 for web camera
camera = cv2.VideoCapture(0)  # use 0 for web camera
success, frame = camera.read()  # read the camera frame
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

frame_rate = 30
frame_height = int(camera.get(4))
frame_width = int(camera.get(3))
frame_counter = 0

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

def gen_frames():  # generate frame by frame from camera
    print('gen_frames')
    while True:
        # Capture frame-by-frame
        if not success:
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

### end

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/my-link/')
def my_link():
  webcam = cv2.VideoCapture(0)
  _, frame = webcam.read()
  return track.start(frame, webcam)

@app.route('/video_feed')
def video_feed():
    print('video_feed')
    while True:
      # We get a new frame from the webcam
      _, frame = camera.read()

      # We send this frame to GazeTracking to analyze it
      gaze.refresh(frame)

      frame = gaze.annotated_frame()
      frame = cv2.flip(frame, 1)
      text = ""

      if gaze.is_blinking():
        text = "Blinking"
      elif gaze.is_right():
        text = "Looking right"
      elif gaze.is_left():
        text = "Looking left"
      elif gaze.is_center():
        text = "Looking center"

      cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

      left_pupil = gaze.pupil_left_coords()
      right_pupil = gaze.pupil_right_coords()
      cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
      cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

      cv2.imshow("Demo", frame)

      k = cv2.waitKey(1) & 0xFF
      if not (cv2.getWindowProperty('Demo',cv2.WND_PROP_VISIBLE)):   
        break
      elif cv2.waitKey(1) == 27:
        break
        
      camera.release()
      cv2.destroyAllWindows()

    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  app.run(debug=True)