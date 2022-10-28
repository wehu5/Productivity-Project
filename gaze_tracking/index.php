<html>
  <head>
    <link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css" />
    <script defer src="https://pyscript.net/alpha/pyscript.js"></script>
  </head>
  <input type="button" id='script' name="scriptbutton" value=" Run Script " onclick="exec('python /Users/jwong1209qaz/Desktop/IEEEQP/GazeTracking/example.py');">
    <?PHP
echo shell_exec("python /Users/jwong1209qaz/Desktop/IEEEQP/GazeTracking/example.py");
    ?>
      <form method="gaze">
        <input type="submit" name="button"
                class="button" value="Button1" />
      </form>
    
</html>