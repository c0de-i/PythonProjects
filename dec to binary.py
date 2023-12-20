def minMaxTime(inputTime):
  # Extract the hour, minute, and second from the input time
  hour, minute, second = map(int, inputTime.split(':'))

  # Initialize the minimum and maximum times
  minTime = 24 * 60 * 60
  maxTime = 0

  # Loop through all possible values for the blank space
  for i in range(10):
    for j in range(6):
      # Compute the new time
      newTime = (hour * 60 + i * 10 + minute % 10) * 60 + j * 10 + second % 10

      # Update the minimum and maximum times
      if newTime < minTime and newTime >= 0:
        minTime = newTime
      if newTime > maxTime and newTime <= 24 * 60 * 60:
        maxTime = newTime

  # Convert the minimum and maximum times back to hh:mm:ss format
  minTime = '{:02d}:{:02d}:{:02d}'.format(minTime // 3600, minTime % 3600 // 60, minTime % 60)
  maxTime = '{:02d}:{:02d}:{:02d}'.format(maxTime // 3600, maxTime % 3600 // 60, maxTime % 60)

  # Print the output
  print('Minimum possible time: {}'.format(minTime))
  print('Maximum possible time: {}'.format(maxTime))

# Example usage
inputTime = '11:22:33'
minMaxTime(inputTime)